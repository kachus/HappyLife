import os

import datetime
from asyncio import sleep

from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import (
    Message,
    CallbackQuery, FSInputFile
)

from ChatGPT import GPT
from keyboards.callback_fabric import StartBeliefsFactory

from BD.MongoDB.datat_enteties import Dialog, DialogMessage, PassingPeriod
from aiogram.enums import ContentType
from aiogram import Bot, F, Router

from services.services import add_dialog_data, get_audio_duration, load_voice_messages
# from services.speech_processer import speech_to_voice_with_path
from keyboards.inline_keyboards import create_futher_kb, leave_feedback_or_end_kb, \
    create_define_way
from config_data.config import load_config

# загрузка сценария шагов по сценарию "Определить убедждение \ загон"
from states.main_process import FSMQMainProcess
from lexicon.lexicon_ru import LEXICON_RU
from voice.match_key_file import get_file_path
from ChatGPT.gpt_options import GPTOptions
from ChatGPT.gpt_message import GPTMessage, GPTRole
from models import SystemMessage, UserMessage, AssistantMessage
router = Router()

from ChatGPT import GPT

@router.callback_query(StartBeliefsFactory.filter())
async def start_practise(callback: CallbackQuery,
                         bot: Bot,
                         callback_data: StartBeliefsFactory,
                         data_base,
                         state: FSMContext):

    await bot.send_message(chat_id=callback.message.chat.id,
                           text='Начинаем!')

    await GPT.complete(system_message=SystemMessage(content='Ты в роли психолога, а я твой клиент. проведи сеанс и говори дружелюбно'),
                       messages=[
                                AssistantMessage(content='Привет!'),
                                UserMessage(id=0, content='Привет, меня зовут Женя') ],
                       temperature=0.25)



# получаем пол пользователя из базы данных
# получаем загон пользователя


@router.callback_query(FSMQMainProcess.first)
async def relax_command(callback: CallbackQuery,
                        bot: Bot,
                        data_base,
                        state: FSMContext):
    ...


