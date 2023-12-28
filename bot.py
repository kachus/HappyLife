import asyncio


from aiogram import Bot, Dispatcher
import logging

from redis import Redis
from container import data_base_controller, config, logger
from hadnlers import command_handlers,\
    chose_existing_belief_handlers, onboarding, main_process

from aiogram.fsm.storage.redis import RedisStorage



async def main():
    # logging config
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    # info about starting the bot
    logger.info('Starting bot')
    # redis = Redis(host=config.redis_storage.local_host,
    #               port=config.redis_storage.docker_port)
    # redis = Redis(host=config.redis_storage.docker_host,
    #               port=config.redis_storage.docker_port)
    # storage: RedisStorage = RedisStorage(redis=redis)

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    dp = Dispatcher(data_base=data_base_controller,)
    #
    # dp.include_router(onboarding.router)
    dp.include_router(command_handlers.router)
    # dp.include_router(deep_process_new.router)

    dp.include_router(chose_existing_belief_handlers.router)
    dp.include_router(main_process.router)



    try:
        await dp.start_polling(bot)
    finally:
        bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
