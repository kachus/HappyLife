from .interview import Interview

import os
import logging
from datetime import datetime

from ChatGPT import GPT


from models import Message, UserMessage, SystemMessage, AssistantMessage, Role, Conversation



class Dialog:
    def __init__(self):
        api_key = os.environ.get('OPENAI_API_KEY')
        data_dir = os.environ.get('DATA_DIR')

        logging.info(f"Initializing GPT module")  # fixme add another module and rewrite modules
        self.__gpt = GPT(api_key, data_dir)

        logging.info("Initializing interview module")
        self.__interview = Conversation()

    async def reply_last_message(self, conversation: Conversation) -> AssistantMessage:
        user_message = conversation.last_message
        print('reply_last_message, coneversation.message', conversation.messages, conversation.chat_system_message)

        reply_text = await self.__gpt.complete(conversation.messages, conversation.chat_system_message,
                                               temperature=0.25)

        assistant_message = AssistantMessage(0, reply_text, user_message.id)

        # updated in v0.3.1 - ending conversation
        # assistant_message.is_final = self.__check_if_final(reply_text.lower())

        return assistant_message

    async def create_new_conversation(self) -> Conversation:
        system_prompt, evaluation_prompt = self.__interview.get_prompts_for_new_conversation()

        chat_system_message = SystemMessage(system_prompt)
        evaluation_system_message = SystemMessage(evaluation_prompt)

        result = Conversation(
            started_at=datetime.now(),
            messages=[],
            chat_system_message=chat_system_message,)

        logging.info(
            f"Created new Conversation. System prompt is: \n{system_prompt}."
        )

        return result

    @staticmethod
    def __get_last_assistant_message(conversation: Conversation):
        assistant_message = None
        for message in reversed(conversation.messages):
            if message.role == Role.ASSISTANT:
                assistant_message = message
                break

        return assistant_message