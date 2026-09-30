import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    ReplyKeyboardRemove
)
from geopy.distance import geodesic
import sqlite3
from datetime import datetime
import asyncio
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID = os.getenv("ADMIN_ID", "").strip()
if not BOT_TOKEN or not ADMIN_ID.isdigit():
    raise RuntimeError("Set BOT_TOKEN and numeric ADMIN_ID in .env before starting the bot.")

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Координаты городов Крыма (широта, долгота)
CITIES = {
    "Симферополь": (44.952116, 34.102411),
    "Севастополь": (44.616650, 33.525366),
    "Ялта": (44.495194, 34.166302),
    "Алушта": (44.676383, 34.410038),
    "Евпатория": (45.190629, 33.367634),
    "Керчь": (45.356985, 36.467428),
    "Феодосия": (45.031878, 35.382435),
    "Саки": (45.133693, 33.577239),
    "Бахчисарай": (44.755135, 33.857862),
    "Джанкой": (45.709146, 34.388665)
}

# Состояния FSM
class DeliveryForm(StatesGroup):
    from_city = State()
    to_city = State()
    weight = State()
    temperature = State()
    urgency = State()
    phone = State()

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('delivery_orders.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        phone TEXT,
        from_city TEXT,
        to_city TEXT,
        weight REAL,
        temperature TEXT,
        urgency TEXT,
        price REAL,
        created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# Клавиатуры
def get_cities_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=city) for city in list(CITIES.keys())[i:i+2]] 
            for i in range(0, len(CITIES), 2)
        ],
        resize_keyboard=True
    )

def get_temperature_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Охлаждение"), KeyboardButton(text="Заморозка")],
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )

def get_urgency_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Стандартная"), KeyboardButton(text="Срочная")],
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )

def get_phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )

def get_confirmation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Подтвердить заказ")],
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )

# Функция расчета стоимости
def calculate_price(from_city: str, to_city: str, weight: float, temperature: str, urgency: str) -> float:
    # Базовый тариф
    price = 500
    
    # Расчет расстояния
    distance = geodesic(CITIES[from_city], CITIES[to_city]).km
    price += distance * 30
    
    # Надбавки
    if weight > 10:
        price += 100
    if temperature == "Заморозка":
        price += 500
    if urgency == "Срочная":
        price += 1000
    
    return round(price, 2)

# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "❄️ Добро пожаловать в GoFROST - сервис холодной доставки по Крыму!\n\n"
        "Давайте рассчитаем стоимость доставки. Выберите город отправления:",
        reply_markup=get_cities_keyboard()
    )
    await state.set_state(DeliveryForm.from_city)

@dp.message(DeliveryForm.from_city, F.text.in_(CITIES.keys()))
async def process_from_city(message: types.Message, state: FSMContext):
    await state.update_data(from_city=message.text)
    await message.answer(
        "Теперь выберите город назначения:",
        reply_markup=get_cities_keyboard()
    )
    await state.set_state(DeliveryForm.to_city)

@dp.message(DeliveryForm.to_city, F.text.in_(CITIES.keys()))
async def process_to_city(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == data['from_city']:
        await message.answer("Город отправления и назначения не могут совпадать. Выберите другой город:")
        return
    
    await state.update_data(to_city=message.text)
    await message.answer(
        "Введите вес груза в кг (например: 5.5):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(DeliveryForm.weight)

@dp.message(DeliveryForm.weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        if weight <= 0:
            raise ValueError
        await state.update_data(weight=weight)
        await message.answer(
            "Выберите температурный режим:",
            reply_markup=get_temperature_keyboard()
        )
        await state.set_state(DeliveryForm.temperature)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный вес (число больше 0):")

@dp.message(DeliveryForm.temperature, F.text.in_(["Охлаждение", "Заморозка"]))
async def process_temperature(message: types.Message, state: FSMContext):
    await state.update_data(temperature=message.text)
    await message.answer(
        "Выберите срочность доставки:",
        reply_markup=get_urgency_keyboard()
    )
    await state.set_state(DeliveryForm.urgency)

@dp.message(DeliveryForm.urgency, F.text.in_(["Стандартная", "Срочная"]))
async def process_urgency(message: types.Message, state: FSMContext):
    await state.update_data(urgency=message.text)
    data = await state.get_data()
    
    # Расчет стоимости
    price = calculate_price(
        data['from_city'],
        data['to_city'],
        data['weight'],
        data['temperature'],
        data['urgency']
    )
    
    await state.update_data(price=price)
    
    # Формируем сообщение с расчетом
    calculation_message = (
        f"📊 Расчет стоимости доставки:\n\n"
        f"📍 Из: {data['from_city']} → В: {data['to_city']}\n"
        f"⚖️ Вес: {data['weight']} кг\n"
        f"🌡 Температура: {data['temperature']}\n"
        f"⏱ Срочность: {data['urgency']}\n\n"
        f"💰 Итоговая стоимость: {price} ₽\n\n"
        f"Введите ваш номер телефона или любой контакт для связи:"
    )
    
    await message.answer(
        calculation_message,
        reply_markup=get_phone_keyboard()
    )
    await state.set_state(DeliveryForm.phone)

@dp.message(DeliveryForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    # Принимаем любой текст как контактные данные
    await state.update_data(phone=message.text)
    data = await state.get_data()
    
    order_summary = (
        f"📋 Подтвердите заказ:\n\n"
        f"👤 Имя: {message.from_user.full_name}\n"
        f"📞 Контакт: {data['phone']}\n"
        f"📍 Из: {data['from_city']} → В: {data['to_city']}\n"
        f"⚖️ Вес: {data['weight']} кг\n"
        f"🌡 Температура: {data['temperature']}\n"
        f"⏱ Срочность: {data['urgency']}\n"
        f"💰 Стоимость: {data['price']} ₽"
    )
    
    await message.answer(
        order_summary,
        reply_markup=get_confirmation_keyboard()
    )

@dp.message(F.text == "✅ Подтвердить заказ", DeliveryForm.phone)  # Фильтр: только в состоянии "phone"
async def confirm_order(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name

    # Проверка наличия всех данных (на всякий случай)
    required_fields = ['phone', 'from_city', 'to_city', 'weight', 'temperature', 'urgency', 'price']
    if not all(field in data for field in required_fields):
        await message.answer("❌ Ошибка: данные неполные. Начните заново: /start")
        await state.clear()
        return

    # Сохранение в БД
    conn = sqlite3.connect('delivery_orders.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (user_id, username, phone, from_city, to_city, weight, temperature, urgency, price, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            user_id,
            username,
            data['phone'],
            data['from_city'],
            data['to_city'],
            data['weight'],
            data['temperature'],
            data['urgency'],
            data['price'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Отправка админу
    order_message = (
        f"📬 **Новый заказ #{order_id}**\n"
        f"👤 Клиент: {username} (ID: {user_id})\n"
        f"📞 Телефон: {data['phone']}\n"
        f"📍 Маршрут: {data['from_city']} → {data['to_city']}\n"
        f"⚖️ Вес: {data['weight']} кг\n"
        f"🌡 Режим: {data['temperature']}\n"
        f"⏱ Срочность: {data['urgency']}\n"
        f"💰 **Итого: {data['price']} ₽**"
    )

    try:
        await bot.send_message(ADMIN_ID, order_message, parse_mode="Markdown")
        await message.answer(
            "✅ Заказ оформлен! С вами свяжутся в ближайшее время.",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        logger.error(f"Ошибка отправки админу: {e}")
        await message.answer(
            "❌ Ошибка при отправке заказа. Попробуйте позже или свяжитесь с поддержкой.",
            reply_markup=ReplyKeyboardRemove()
        )

    await state.clear()  # Важно: очистка состояния после успешного подтверждения
@dp.message(F.text == "❌ Отмена")
async def cancel_order(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Заказ отменен. Если хотите начать заново, нажмите /start",
        reply_markup=ReplyKeyboardRemove()
    )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())