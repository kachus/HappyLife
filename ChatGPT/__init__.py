from .gpt_options import GPTOptions
from .gpt_message import GPTMessage

from . import openai_chat_complete


class GPT:

    async def complete(self, messages: list[GPTMessage], system_message: GPTMessage, temperature: float) -> str:
        return await self.__openai_chat_complete.complete(messages, system_message, temperature)

    async def complete_one(self, message: GPTMessage, system_message: GPTMessage, temperature: float) -> str:
        return await self.__openai_chat_complete.complete([message], system_message, temperature)

    def __init__(self, api_key: str, user_dir: str):
        print(user_dir)
        self.__openai_chat_complete = openai_chat_complete.GPTClient(options=GPTOptions(
                api_key=api_key,
                model_name='gpt-3.5-turbo-16k',
                max_message_count=25,
                max_token_count=16000,))

        # can add other models

        # self.__openai_instruct = openai_instruct.GPTClient(options=GPTOptions(
        #        api_key=api_key,
        #        model_name='gpt-3.5-turbo-instruct',
        #        max_token_count=4000,
        #        tokens_log_filename=user_dir + "tokens.txt"))


    async def close(self):
        await self.__openai_chat_complete.close()
