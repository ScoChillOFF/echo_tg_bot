from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command


API_TOKEN: str = '6266775802:AAEh9pNqqdW-4_NVQp5ygtDB-j6ErZkEOSo'


bot: Bot = Bot(API_TOKEN)
dp: Dispatcher = Dispatcher()


async def process_start_command(message: Message):
    await message.answer(text=f'Привет, {message.from_user.first_name}!\nЯ Эхо-бот! Отправь мне любое сообщение.')

async def process_help_command(message: Message):
    await message.answer(text='Данный бот повторит любое ваше сообщение.')

async def send_echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)


dp.message.register(process_start_command, Command(commands=['start']))
dp.message.register(process_help_command, Command(commands=['help']))
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)
