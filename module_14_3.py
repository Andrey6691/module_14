from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['Рассчитать', 'Информация', 'Купить']
kb.add(*buttons)

kb2 = InlineKeyboardMarkup(row_width=2)
kb2.add(InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories'),
        InlineKeyboardButton(text = 'Формула расчета', callback_data = 'formulas'))

kb3 = InlineKeyboardMarkup(row_width = 4)
kb3.add(InlineKeyboardMarkup(text = 'Product1', callback_data = 'product_buying'),
        InlineKeyboardMarkup(text = 'Product2', callback_data="product_buying"),
        InlineKeyboardMarkup(text = 'Product3', callback_data="product_buying"),
        InlineKeyboardMarkup(text = 'Product4', callback_data="product_buying"))





class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()




@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        await message.answer(f'Название: Product{i} | Описание: описание {i} | Цена:  {i*100}')
        with open(f"files/{i}.jpg", 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup = kb3)



@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10*int(data.get('weight'))+6.25*int(data.get('growth'))-5*int(data.get('age'))+5
    await message.answer(f'Ваша норма калорий {calories}')



@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5')
    await call.answer()

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup = kb2)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
