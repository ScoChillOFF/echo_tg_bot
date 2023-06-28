from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
import requests
from random import randint
from bot_token import BOT_TOKEN


CAT_API_URL: str = 'https://api.thecatapi.com/v1/images/search'
DOG_API_URL: str = 'https://dog.ceo/api/breeds/image/random'


bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()
animal_response: requests.Response
animal_choice: int


def generate_number() -> int:
    return randint(1, 2)


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(text=f'Привет, {message.from_user.first_name}!\nЯ Эхо-бот! Отправь мне любое сообщение.')


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text='Данный бот повторит любое ваше сообщение.')


@dp.message(Command(commands=['animal']))
async def process_animal_command(message: Message):
    animal_choice = generate_number()
    if animal_choice == 1:
        animal_response = requests.get(DOG_API_URL)
        dog_img = animal_response.json()['message']
        await message.answer_photo(photo=dog_img)
        # Добавить обработку исключения
    else:
        animal_response = requests.get(CAT_API_URL)
        cat_img = animal_response.json()[0]['url']
        await message.answer_photo(photo=cat_img)
        # Добавить обработку исключения


@dp.message()
async def send_echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)


if __name__ == '__main__':
    dp.run_polling(bot)
