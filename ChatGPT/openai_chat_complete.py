import asyncio
import logging

from aiohttp import ClientSession
from typing import cast

import openai
from .gpt_options import GPTOptions
from .gpt_message import GPTMessage


class GPTClient:
    def __init__(self, *, options: GPTOptions):
        self.__model_name = options.model_name
        self.__max_message_count = options.max_message_count
        self.__max_tokens = options.max_token_count

        openai.api_key = options.api_key

        self.__session = ClientSession(trust_env=True)
        openai.aiosession.set(self.__session)

        self.__lock = asyncio.Lock()

    async def close(self):
        if self.__session:
            await self.__session.close()
            self.__session = None

    async def complete(self, messages: list[GPTMessage],
                       system_message: GPTMessage,
                       temperature: float) -> str:
        if self.__max_message_count is None:
            msg_list = [system_message] if system_message else [] + messages
        elif len(messages) > self.__max_message_count:
            msg_list = ([system_message] if system_message else []) + messages[-self.__max_message_count:]
        else:
            msg_list = ([system_message] if system_message else []) + messages

        gpt_args = {
            'model':
                self.__model_name,
            'messages': [{
                'role': message.role,
                'content': message.content}
                for message in msg_list],
            'temperature': temperature,
        }
        print('gpt args:', gpt_args)
        print('msg list', msg_list)

        response = await self.__request(gpt_args)
        return response

    async def __request(self, gpt_args: dict) -> str:
        task = openai.ChatCompletion.acreate(**gpt_args)

        if task is None:
            raise ValueError("Task is None!")

        response = await asyncio.wait_for(task, 60)
        response_choice = cast(dict, response)['choices'][0]
        response_text = response_choice['message']['content']
        print('response_test:', response_text)

        return response_text



