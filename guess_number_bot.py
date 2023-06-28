from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import Text, Command
from bot_token import BOT_TOKEN

import random


ATTEMPTS: int = 5

bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()

users: dict = {}


def get_secret_number() -> int:
    return random.randint(1, 100)


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                    'secret_number': None,
                                    'attempts': None,
                                    'total_games': 0,
                                    'wins': 0}
    if users[message.from_user.id]['in_game'] == False:
        await message.answer(text='Привет!\nДавай сыграем в игру "Угадай число"?\n'
                        'Чтобы прочитать подробные правила, введите команду /help')
    else:
        await message.answer(text='Пока мы играем, я не могу реагировать ни на что, кроме чисел от 1 до 100 и команд /cancel и /stat')
    

@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=
                         f'Доступные команды:\n'
                         f'/start - Начать\n/help - Список команд и правила игры\n/stat - Показать статистику\n/cancel - Закончить игру\n\n'
                         f'Правила игры:\nЯ загадываю число от 1 до 100.\n'
                         f'Есть {ATTEMPTS} попыток чтобы его отгадать.\n'
                         f'Я буду сравнивать введенное число с заданным и говорить, больше оно или меньше.')
    

@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(text=f'Количество сыгранных партий: {users[message.from_user.id]["total_games"]}\n'
                         f'Количество выигранных партий: {users[message.from_user.id]["wins"]}')
    

@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game'] == True:
        users[message.from_user.id]['in_game'] = False
        await message.answer(text='Очень жаль!\n'
                             'Если захотите сыграть снова, напишите "Игра"')
    else:
        await message.answer(text='А мы и так не играем!\n'
                             'Но если захотите сыграть, напишите "Игра"')
        

@dp.message(Text(text=['Да', 'Давай', 'Игра'], ignore_case=True))
async def process_positive_answer(message: Message):
    if users[message.from_user.id]['in_game'] == False:
        await message.answer(text=f'Ура!\nЯ загадал число от 1 до 100\nУ тебя есть {ATTEMPTS} попыток, чтобы его угадать')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_secret_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        print(users[message.from_user.id]['secret_number'])
    else:
        await message.answer(text='Пока мы играем, я не могу реагировать ни на что, кроме чисел от 1 до 100\nи команд /cancel и /stat')


@dp.message(Text(text=['Нет', 'Не хочу'], ignore_case=True))
async def process_negative_answer(message: Message):
    if users[message.from_user.id]['in_game'] == False:
        await message.answer(text='Очень жаль!\n'
                             'Если захотите сыграть, напишите "Игра"')
    else:
        await message.answer(text='Пока мы играем, я не могу реагировать ни на что, кроме чисел от 1 до 100\nи команд /cancel и /stat')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number_answers(message: Message):
    if users[message.from_user.id]['in_game'] == True:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer(text='Ура! Поздравляю!\nВы угадали загаданное мной число!\nХотите ли сыграть еще?')
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            users[message.from_user.id]['in_game'] = False
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer(text='Мое число больше!')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer(text='Мое число меньше!')
            users[message.from_user.id]['attempts'] -= 1
        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(text='Я выиграл! У вас закончились попытки, и вы не угадали число.\nХотите сыграть еще?')
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['in_game'] = False
    else:
        await message.answer(text='Мы сейчас не играем.\nЧтобы начать игру, напишите "Игра"\nНу что, хотите сыграть?')


@dp.message()
async def process_error_messages(message: Message):
    if users[message.from_user.id]['in_game'] == True:
        await message.answer(text='Пожалуйста, вводите числа от 1 до 100\n'
                             'либо команды /stat и /cancel')
    else:
        await message.answer('Извините, я ограниченный бот и не понимаю вашу команду\nДавайте просто сыграем?')


if __name__ == '__main__':
    dp.run_polling(bot)
