import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Состояния бота
class CalcState(StatesGroup):
    waiting_credit = State()
    waiting_deposit = State()


# Инициализация бота
bot = Bot(token="7712119487:AAEiS9JYU_bh4TeEshDUkKjTn5PbGT9mg5A")
dp = Dispatcher()


# Главное меню
async def show_main_menu(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Кредитный калькулятор"))
    builder.add(types.KeyboardButton(text="Вкладной калькулятор"))
    await message.answer(
        "Выберите тип расчета:", reply_markup=builder.as_markup(resize_keyboard=True)
    )


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await show_main_menu(message)


# Обработчик выбора калькулятора
@dp.message(
    lambda message: message.text in ["Кредитный калькулятор", "Вкладной калькулятор"]
)
async def calc_choice(message: types.Message, state: FSMContext):
    if message.text == "Кредитный калькулятор":
        await state.set_state(CalcState.waiting_credit)
        await message.answer(
            "Введите через пробел:\nСумма кредита (руб)\nСрок (мес)\nПроцентная ставка\nПример: 100000 12 15",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    else:
        await state.set_state(CalcState.waiting_deposit)
        await message.answer(
            "Введите через пробел:\nСумма вклада (руб)\nСрок (мес)\nПроцентная ставка\nПример: 100000 12 8",
            reply_markup=types.ReplyKeyboardRemove(),
        )


# Обработчик кредитного калькулятора
@dp.message(CalcState.waiting_credit)
async def credit_calc(message: types.Message, state: FSMContext):
    try:
        amount, months, rate = map(float, message.text.split())
        monthly_rate = rate / 12 / 100
        payment = (amount * monthly_rate * (1 + monthly_rate) ** months) / (
            (1 + monthly_rate) ** months - 1
        )
        total = payment * months

        await message.answer(
            f"📊 Результаты расчета кредита:\n\n"
            f"• Ежемесячный платеж: {payment:.2f} ₽\n"
            f"• Общая сумма выплат: {total:.2f} ₽\n"
            f"• Переплата: {total - amount:.2f} ₽"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}\nПопробуйте еще раз")
    finally:
        await show_main_menu(message)
        await state.clear()


# Обработчик вкладного калькулятора
@dp.message(CalcState.waiting_deposit)
async def deposit_calc(message: types.Message, state: FSMContext):
    try:
        amount, months, rate = map(float, message.text.split())
        profit = amount * (rate / 100) * (months / 12)

        await message.answer(
            f"💰 Результаты расчета вклада:\n\n"
            f"• Доход: {profit:.2f} ₽\n"
            f"• Итоговая сумма: {amount + profit:.2f} ₽"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}\nПопробуйте еще раз")
    finally:
        await show_main_menu(message)
        await state.clear()


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
