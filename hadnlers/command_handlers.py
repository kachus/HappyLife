# Все хэндлеры с командами тут
# ______________________________________________
import logging
import os
from datetime import datetime
import logging

from aiogram.filters import CommandStart

from aiogram.fsm.context import FSMContext

from aiogram.filters.state import State, StatesGroup
from BD.MongoDB.datat_enteties import Belief
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile

from BD.DBinterface import MongoDataBaseRepositoryInterface

from keyboards.callback_fabric import CategoryBeliefsCallbackFactory, CommonBeliefsCallbackFactory
from keyboards.inline_keyboards import \
    create_define_way, create_start_practice_kb, choose_gender_kb, \
    create_keyboard_chose_belief, crete_category_keyboard, back_to_menu, own_struggle_next_step

from aiogram import Bot, F, Router, html

from services.services import save_user_if_not_exist, load_voice_messages
# загрузка сценария шагов по сценарию "Определить убедждение"
from BD.MongoDB.mongo_enteties import Client
from services.speach_to_text import voice_to_text

router = Router()


class FSMCommonCommands(StatesGroup):
    gender = State()
    own_struggle = State()
    own_struggle_next_step = State()



@router.message(CommandStart())
async def initial_keyboard(message: Message, bot: Bot, data_base: MongoDataBaseRepositoryInterface):
    await save_user_if_not_exist(message, data_base)
    # Клавиатура принимает id чата для того чтобы определить был он или нет в базе
    keyboard = choose_gender_kb()
    await bot.send_message(chat_id=message.chat.id,
                           text='Привет! Этот бот поможет разобраться тебе с твоими загонами! ⚡\nВыбери свой пол',
                           reply_markup=keyboard)

@router.callback_query(F.data.contains('male'))
async def process_gender_chose_command(callback: CallbackQuery, bot: Bot,
                                       data_base: MongoDataBaseRepositoryInterface, state: FSMContext):

    logging.info(f'пол юзера: {callback.data}')
    choose_command_kb = create_define_way(database=data_base,
                                        user_telegram_id=callback.message.chat.id)

    if callback.data == 'female':
        data_base.client_repository.update_gender(user_id=callback.message.chat.id, gender='female')
    elif callback.data == 'male':
        data_base.client_repository.update_gender(user_id=callback.message.chat.id, gender='male')

    await state.update_data(gender=callback.data)
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text='Выбери подходящую команду',
                                reply_markup=choose_command_kb)


@router.callback_query(F.data == 'chose_beliefs')
async def process_chose_beliefs_category(callback: CallbackQuery,
                                         bot: Bot,
                                         data_base,
                                         state: FSMContext):
    kb = crete_category_keyboard(user_id=callback.message.chat.id, data_base_controller=data_base)
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text="Выбери категорию",
                                reply_markup=kb)



@router.callback_query(F.data == 'tell_beliefs')
async def process_tell_beliefs_command(callback: CallbackQuery,
                                       bot: Bot,
                                       data_base,
                                       state: FSMContext):
    await bot.send_message(chat_id=callback.message.chat.id,
                           text='Расскажи свой загон! Ты можешь сделать это текстом, а также можешь записать'
                                'аудио сообщение.')
    await state.set_state(FSMCommonCommands.own_struggle)


@router.callback_query(CategoryBeliefsCallbackFactory.filter())
async def process_chose_belief(callback: CallbackQuery,
                               callback_data: CategoryBeliefsCallbackFactory,
                               bot: Bot,
                               data_base):
    keyboard = create_keyboard_chose_belief(data_base_controller=data_base, user_id=callback.message.chat.id,
                                            category=callback_data.category_id, )
    # тут нужно отобразить категорию в коллбэе  полностью и не нужен пол
    logging.info(f'Выбрана категория {callback_data.category_name_ru}')
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text=f"Категория: <b>{callback_data.category_name_ru}</b>"
                                     f"\n\nВыбери загон", reply_markup=keyboard)


# Если пользователь выбирает загон в этом сценарии то это новый загон
@router.callback_query(CommonBeliefsCallbackFactory.filter())
async def process_start_with_belief(callback: CallbackQuery,
                                    callback_data: CommonBeliefsCallbackFactory,
                                    bot: Bot,
                                    state: FSMContext,
                                    data_base):
    # получаем загон по его id
    logging.info(f'belief_id :{callback_data.belief_id}')
    belief = data_base.problem_repository.get_problem_by_problem_id(belief_id=callback_data.belief_id)
    await state.update_data(category=callback_data.category_name_ru)
    # Передаем в клавиатуру id загона
    keyboard = create_start_practice_kb(callback_data.belief_id)
    # сохраняем загон в базу данных для пользователя
    new_belief = Belief(
        belief=belief,
        first_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        last_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        dialogs=[]
    )
    data_base.client_repository.save_new_belief_to_user(user_telegram_id=callback.message.chat.id,
                                                        belief=new_belief.to_dict())  # конвертация в словарь для записи в базу

    await bot.send_message(chat_id=callback.message.chat.id,
                           text=f"Ты выбрал(а) загон: <b>{belief.belief}</b>"
                                f"\n\nНачнем работу?", reply_markup=keyboard)
    # TODO: Сделать передачу данных с ID загона


@router.message(FSMCommonCommands.own_struggle, F.content_type.in_({ContentType.VOICE}))
async def process_personal_struggle_voice(message: Message,
                                          bot: Bot,
                                          state: FSMContext,
                                          data_base):
    await state.set_state(FSMCommonCommands.own_struggle)
    file_on_disk = await load_voice_messages(message=message, bot=bot)
    user_answer = voice_to_text(voice_message_path=file_on_disk)
    gender = data_base.client_repository.get_user_gender(user_telegram_id=message.chat.id)
    new_belief_id = data_base.problem_repository.create_own_problem(telegram_id=message.chat.id, belief=user_answer,
                                                                    gender=gender)

    belief = data_base.problem_repository.get_problem_by_problem_id(belief_id=new_belief_id)
    new_belief_in_user = Belief(
        belief=belief,
        first_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        last_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        dialogs=[]
    )
    data_base.client_repository.save_new_belief_to_user(user_telegram_id=message.chat.id,
                                                        belief=new_belief_in_user.to_dict())
    next_step_kb = own_struggle_next_step(belief_id=new_belief_id)
    await message.answer(text='Что ты хочешь сделать дальше?', reply_markup=next_step_kb)
    os.remove(path=file_on_disk)


@router.message(FSMCommonCommands.own_struggle, F.content_type.in_({ContentType.TEXT}))
async def process_personal_struggle_text(message: Message,
                                    bot: Bot,
                                    state: FSMContext,
                                    data_base):
    user_answer = message.text
    gender = data_base.client_repository.get_user_gender(user_telegram_id=message.chat.id)
    new_belief_id = data_base.problem_repository.create_own_problem(telegram_id=message.chat.id, belief=user_answer,
                                                                    gender=gender)
    belief = data_base.problem_repository.get_problem_by_problem_id(belief_id=new_belief_id)
    new_belief_in_user = Belief(
        belief=belief,
        first_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        last_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        dialogs=[]
    )
    data_base.client_repository.save_new_belief_to_user(user_telegram_id=message.chat.id,
                                                        belief=new_belief_in_user.to_dict())
    next_step_kb = own_struggle_next_step(belief_id=new_belief_id)
    await message.answer(text='Что ты хочешь сделать дальше?', reply_markup=next_step_kb)