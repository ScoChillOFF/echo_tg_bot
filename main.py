from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram import F


API_TOKEN: str = '6266775802:AAEh9pNqqdW-4_NVQp5ygtDB-j6ErZkEOSo'


bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')


async def send_echo(message: Message):
    await message.answer(text=message.text)


async def send_photo_echo(message: Message):
    print(message)
    await message.answer_photo(message.photo[0].file_id)


dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=['help']))
dp.message.register(send_photo_echo, F.content_type == ContentType.PHOTO)
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)