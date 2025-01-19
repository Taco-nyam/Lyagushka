import logging
import os

from dotenv import load_dotenv

load_dotenv()
from email.policy import default

from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

payload1 = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content="Ты бот, который генерирует текст по запросу"
        )
    ],
    temperature=0.7,
)
payload2 = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content="Общение обо всём и обо всём"
        )
    ],
    temperature=0.7,
)
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
async def gigachat(message: Message, payload, wait):
    # Отправляем запрос в GigaChat
    with GigaChat(credentials=os.getenv("GIGA_TOKEN"), verify_ssl_certs=False) as giga:
        payload.messages.append(Messages(role=MessagesRole.USER, content=message.text))
        response = giga.chat(payload)
        payload.messages.append(response.choices[0].message)
        response_text = response.choices[0].message.content
        await bot.edit_message_text(message_id=wait.message_id, chat_id=message.from_user.id,text=response_text)
async def animate_message(msg, chat_id):
    while True:
        sand_clock_states = ["️⌛", "⏳"]
        for state in sand_clock_states:
            await bot.edit_message_text(f" Ожидайте ответ генерируется!{state}", chat_id, msg.message_id)
            await asyncio.sleep(0.7)
@dp.message(lambda message:"изображение" in message.text.lower())
@dp.message(lambda message:" текст" in message.text.lower())
@dp.message(lambda message:"анекдот" in message.text.lower())
@dp.message(lambda message:"факт" in message.text.lower())
async def RandomText(message: Message):
    iks = await bot.send_message(chat_id=message.from_user.id, text='<b>Ожидайте ответ генерируется!⌛</b>',parse_mode="HTML")
    sand_clock_states = ["️⌛", "⏳"]
    animation_task = asyncio.create_task(animate_message(iks, message.from_user.id))
    response_text = await gigachat(message, payload1, iks)
    animation_task.cancel()
    # await bot.delete_message(chat_id=message.from_user.id, message_id=iks.message_id)
@dp.message(lambda message:"изображен" in message.text.lower())
@dp.message(Command("photo"))
async def Photo(message: Message):
    photo = FSInputFile("арбуз.jpg")
    await bot.send_photo(chat_id=message.from_user.id,photo=photo)
@dp.message(Command("sticker"))
async def Sticker(message: Message):
    sticker = FSInputFile("AnimatedSticker.tgs")
    await bot.send_sticker(chat_id=message.from_user.id,sticker="CAACAgIAAxkDAAMsZ35TC6ZPdGjZM0iqcAuesjW8QIYAAnVgAAJ_D_FLa1heJ1-6WwU2BA")
@dp.message(Command("voice"))
async def Voice(message: Message):
    await bot.send_voice(chat_id=message.from_user.id, voice="AwACAgIAAxkBAAMwZ35VfQxg2KlVrq3dbPPOrme7nesAAsFgAAJB0fFLzLTOhIUttK82BA")
@dp.message(Command("video"))
async def Video(message: Message):
    await bot.send_video(chat_id=message.from_user.id, video="CgACAgIAAxkBAAM1Z35WyBBIkFQL3N2Kfz--Mgr4buMAAn9iAAIW3_hLYATXveUOkjo2BA")
@dp.message(Command("dice"))
async def Dice(message: Message):
    await bot.send_dice(chat_id=message.chat.id, emoji="🎰")
@dp.message(Command("gps"))
async def GPS(message: Message):
    await bot.send_location(chat_id=message.chat.id, latitude=53.900514, longitude=27.559049)
@dp.message(Command("txt"))
async def TXT(message: Message):
    await bot.send_document(chat_id=message.from_user.id, document="BQACAgIAAxkBAANKZ4O7f7Vy3PHS2zKdHRv4jR0R4rYAAg9oAALoXSFIHNHwgMIySEo2BA")
@dp.message(Command("start"))
async def start(message: Message):
    KB = ReplyKeyboardMarkup(keyboard = [
        [KeyboardButton (text = "Сгенирируй Изображение📷"),KeyboardButton (text = "Сгенирируй Текст🖊️")],
        [KeyboardButton (text = "Напиши рандомный факт❓️"),KeyboardButton (text = "Напиши любой Анекдот😂")]
    ],resize_keyboard=True)
    await bot.send_message(chat_id=message.from_user.id, text="Привет! Меня зовут ЛягушонокБОТ я функциональный помощник для тебя!",reply_markup=KB)
async def main():
    await dp.start_polling(bot)
@dp.message()
async def function(message: Message):
    iks = await bot.send_message(chat_id=message.from_user.id, text='<b>Ожидайте ответ генерируется!⌛</b>',parse_mode="HTML")
    # sand_clock_states = ["️⌛", "⏳"]
    # animation_task = asyncio.create_task(animate_message(iks, message.from_user.id))
    response_text = await gigachat(message, payload2, iks)
    # animation_task.cancel()
    # await bot.delete_message(chat_id=message.from_user.id, message_id=iks.message_id)
asyncio.run(main())