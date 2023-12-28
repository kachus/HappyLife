from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery

from BD.DBinterface import MongoDataBaseRepositoryInterface

from keyboards.inline_keyboards import \
    create_define_way

from aiogram import Bot, F, Router

router = Router()

# @router.callback_query(F.data.contains('male'))
# async def process_gender_chose_command(callback: CallbackQuery, bot: Bot,
#                                        data_base: MongoDataBaseRepositoryInterface, state: FSMContext):
#
#
#     choose_command_kb = create_define_way(database=data_base,
#                                         user_telegram_id=callback.message.chat.id)
#
#     if callback.data == 'female':
#         data_base.client_repository.update_gender(user_id=callback.message.chat.id, gender='female')
#     elif callback.data == 'male':
#         data_base.client_repository.update_gender(user_id=callback.message.chat.id, gender='male')
#
#     await state.update_data(gender=callback.data)
#     await bot.edit_message_text(chat_id=callback.message.chat.id,
#                                 message_id=callback.message.message_id,
#                                 text='Выбери подходящую команду',
#                                 reply_markup=choose_command_kb)
