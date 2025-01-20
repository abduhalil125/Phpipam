from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from handlers import message as message_handler
from aiogram.types import BotCommand
from aiogram import Bot
from aiohttp import web
import env_vars

from bot_init import dp, bot
from states import Holat

@dp.message(Command("start"))
async def start_command(message: Message):
    await message_handler.start_command(message)

@dp.message(Command("remove_button"))
async def remove_button_command(message: Message):
    await message_handler.remove_button_command(message)

@dp.message(Command("register"))
async def register_command(message: Message, state: FSMContext):
    await message_handler.register_command(message, state)

@dp.message(Command("unregister"))
async def unregister_command(message: Message):
    await message_handler.unregister_command(message)

@dp.message(Command("userlist"))
async def userlist_command(message: Message):
    await message_handler.userlist_command(message)

@dp.message(Holat.get_firstname)
async def get_message(message: Message, state: FSMContext):
    await message_handler.receive_first_name(message, state)

@dp.message(Holat.get_lastname)
async def get_message(message: Message, state: FSMContext):
    await message_handler.receive_last_name(message, state)

@dp.callback_query(Holat.check_data)
async def check_callback_query(callback: CallbackQuery, state: FSMContext):
    await message_handler.confirm_data(callback, state)

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Show help information"),
        BotCommand(command="register", description="Register for the bot"),
        BotCommand(command="unregister", description="Unregister from the bot"),
        BotCommand(command="userlist", description="List of users"),
        BotCommand(command="remove_button", description="Remove buttons"),
    ]
    await bot.set_my_commands(commands)

async def handle_webhook(request):
    update = await request.json()
    dp.feed_update(update)
    return web.Response()

async def on_startup_webhook():
    await bot.set_webhook(env_vars.WEBHOOK_URL)

async def on_shutdown_webhook():
    await bot.delete_webhook()
    await bot.session.close()

async def main():
    await set_bot_commands(bot)
    if env_vars.USE_WEBHOOK == 1:
        app = web.Application()
        app.router.add_post(f"/webhook/{env_vars.BOT_TOKEN}", handle_webhook)

        app.on_startup.append(lambda _: on_startup_webhook())
        app.on_shutdown.append(lambda _: on_shutdown_webhook())
        web.run_app(app, host=env_vars.WEBAPP_HOST, port=env_vars.WEBAPP_PORT)
    else:   
        await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

