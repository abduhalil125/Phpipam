from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import env_vars

bot = Bot(token=env_vars.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)