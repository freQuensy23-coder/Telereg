import aiogram

import asyncio
import logging

from aiogram.utils import exceptions

from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentTypes
from aiogram.utils import executor

from config import token

from requests_database import session

from Classes.request import Request

from status import status_decode, status_encode

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive callвы
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


@dp.message_handler(commands=["code"])
async def code_event_listener(message: types.Message):
    """When user send code to telegram"""
    code = message.get_args().strip()
    user_id = message.from_user.id
    if code is not None and len(code) >= 4: # if sendet msg consist some code
        req = session.query(Request).filter_by(code=code).first()
        if req is None:
            await send_message(user_id=user_id, text="Такой код не найден. Возможно вы ошиблись при копировании или "
                                                     "создавали его раньше 15 минут назад")
        else:
            # If code is right change it's status
            req.status = status_encode("accepted")
            await send_message(user_id=user_id, text="Код принят. Мы сообщили вашему сервису об этом.")
            session.commit()
    else:
        await send_message(user_id=user_id, text="Неправильный формат кода")
    session.query()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)