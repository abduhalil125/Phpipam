from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
import requests
import env_vars
from states import Holat

async def start_command(message: Message):
    hi = KeyboardButton(text="Hi")
    bye = KeyboardButton(text="Bye")
    markup = ReplyKeyboardMarkup(keyboard=[[hi, bye]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Bot has been started", reply_markup=markup)
    # await bot.send_message(text="Test", chat_id=message.from_user.id)

async def remove_button_command(message: Message):
    await message.answer("Buttons removed", reply_markup=ReplyKeyboardRemove())
    # await bot.send_message(text="Test", chat_id=message.from_user.id)

async def register_command(message: Message, state: FSMContext):
    await message.answer("Enter your first name")
    await state.set_state(Holat.get_firstname)

async def unregister_command(message: Message):
    try:
        body_data = {
            "chat_id": message.from_user.id,
        }
        response = requests.delete(url=f"{env_vars.FLASK_API}/api/v1/users/delete", json=body_data)
        response_data = response.json()
        if (response_data["status"] == "error"):
            await message.answer("You are not registered")
            return "OK"
        await message.answer("Your user has been deleted")
    except Exception as e:
        await message.answer("Error")

async def userlist_command(message: Message):
    try:
        response = requests.get(url=f"{env_vars.FLASK_API}/api/v1/users/list")
        response_data = response.json()
        if (response_data["status"] == "error"):
            await message.answer("There is error")
            return "OK"
        if (len(response_data["users"]) == 0):
            await message.answer("There are no users")
            return "OK"
        message_text = "Users list:\n"
        for user in response_data["users"]:
            message_text = f"{message_text}\n{user['id']}: {user['name']} {user['username']} - {user['created_at']}"
        await message.answer(message_text)
    except Exception as e:
        await message.answer("Error")

async def receive_first_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(firstname=name) # {"firstname": "Zafar"}
    await message.answer("Enter your last name")
    await state.set_state(Holat.get_lastname)

async def receive_last_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(lastname=name)
    data = await state.get_data()
    button_yes = InlineKeyboardButton(text="Yes", callback_data="confirm_data_yes")
    button_no = InlineKeyboardButton(text="No", callback_data="confirm_data_no")
    check_data_markup = InlineKeyboardMarkup(inline_keyboard=[[button_yes, button_no]])
    await message.answer(text=f"I have got your data. \n\nFirstname: {data['firstname']}\nLastname: {data['lastname']}\n\nClick \"Yes\" to confirm or \"No\" to edit", reply_markup=check_data_markup)
    await state.set_state(Holat.check_data)

async def confirm_data(callback: CallbackQuery, state: FSMContext):
    c_data = callback.data
    if c_data == "confirm_data_yes":
        data = await state.get_data()
        try:
            body_data = {
                "chat_id": callback.from_user.id,
                "name": f"{data['firstname']} {data['lastname']}",
                "username": f"@{callback.from_user.username}"
            }
            response = requests.post(url=f"{env_vars.FLASK_API}/api/v1/users/register", json=body_data)
            response_data = response.json()
            if (response_data["status"] == "error"):
                await callback.message.answer("Error")
                await state.clear()
                return "OK"
        except Exception as e:
            await callback.message.answer("Error")
        
        await callback.message.answer("Your data has been saved")
        await state.clear()
    elif c_data == "confirm_data_no":
        await callback.message.answer("Enter your first name")
        await state.set_state(Holat.get_firstname)
    else:
        return "OK"