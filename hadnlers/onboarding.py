from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery

from BD.DBinterface import MongoDataBaseRepositoryInterface

from keyboards.inline_keyboards import \
    create_define_way

from aiogram import Bot, F, Router

router = Router()


@router.callback_query(F.data == 'male')
async def process_male_gender(callback: CallbackQuery, bot: Bot, data_base: MongoDataBaseRepositoryInterface,
                              state: FSMContext):
    inline_keyboard = create_define_way(database=data_base,
                                        user_telegram_id=callback.message.chat.id)

    await state.update_data(gender=callback.data)

    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text='Выбери подходящую команду',
                                reply_markup=inline_keyboard)


@router.callback_query(F.data == 'female')
async def process_female_gender(callback: CallbackQuery, bot: Bot, data_base: MongoDataBaseRepositoryInterface,
                                state: FSMContext):
    inline_keyboard = create_define_way(database=data_base,
                                        user_telegram_id=callback.message.chat.id)
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text='Выбери подходящую команду',
                                reply_markup=inline_keyboard)

#Показать виде , посмотерл дальше в сценарий выбора загона
