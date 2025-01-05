from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio



api = ""
bot = Bot(token= api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text= "Рассчитать")
button2 = KeyboardButton(text= "Информация")
kb.row(button, button2)

class UserState(StatesGroup):
    start = State()
    age = State()
    growth = State()
    weight =State()


@dp.message_handler(commands = ['start'])
async def start_(message):
    await message.answer(text='Привет, я бот помогающий твоему здоровью', reply_markup=kb)


@dp.message_handler(text= ['Информация'])
async def inform(message):
    await message.answer('Информация о боте!')


@dp.message_handler(text= ['Рассчитать'])
async def set_age(message):
    await message.answer("Введите свой возраст: ")
    await UserState.age.set()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(first= message.text)
    await message.answer("Введите свой рост: ")
    await UserState.growth.set()


@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(second= message.text)
    await message.answer("Введите свой вес: ")
    await UserState.weight.set()


@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(third= message.text)
    data = await state.get_data()
    norma = 10 * int(data['third']) + 6.25 * int(data['second']) - 5 * int(data['first']) - 161
    await message.answer(f"Ваша норма калорий {norma} ккал")
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates= True)