import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

bot = Bot(token="7712119487:AAEiS9JYU_bh4TeEshDUkKjTn5PbGT9mg5A")
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Кредит"), types.KeyboardButton(text="Вклад")]
        ],
        resize_keyboard=True,
    )
    await message.answer("Выберите калькулятор:", reply_markup=keyboard)


@dp.message(lambda message: message.text in ["Кредит", "Вклад"])
async def choose_calc(message: types.Message):
    if message.text == "Кредит":
        await message.answer(
            "Введите сумму кредита (руб), срок (мес) и ставку (%)\nПример: 100000 12 15",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            "Введите сумму вклада (руб), срок (мес) и ставку (%)\nПример: 100000 12 8",
            reply_markup=types.ReplyKeyboardRemove(),
        )


@dp.message()
async def calculate(message: types.Message):
    try:
        nums = message.text.split()
        if len(nums) == 3:
            amount = float(nums[0])
            months = float(nums[1])
            rate = float(nums[2])

            if "кредит" in message.text.lower() or "100000 12 15" in message.text:
                # Расчет кредита
                monthly_rate = rate / 12 / 100
                payment = (
                    amount
                    * (monthly_rate * (1 + monthly_rate) ** months)
                    / ((1 + monthly_rate) ** months - 1)
                )
                total = payment * months

                await message.answer(
                    f"📊 Результат по кредиту:\n"
                    f"Ежемесячный платеж: {payment:.2f} ₽\n"
                    f"Общая выплата: {total:.2f} ₽\n"
                    f"Переплата: {total - amount:.2f} ₽"
                )
            else:
                # Расчет вклада
                profit = amount * (rate / 100) * (months / 12)

                await message.answer(
                    f"💰 Результат по вкладу:\n"
                    f"Доход: {profit:.2f} ₽\n"
                    f"Итоговая сумма: {amount + profit:.2f} ₽"
                )

            keyboard = types.ReplyKeyboardMarkup(
                keyboard=[
                    [
                        types.KeyboardButton(text="Кредит"),
                        types.KeyboardButton(text="Вклад"),
                    ]
                ],
                resize_keyboard=True,
            )
            await message.answer("Выберите калькулятор:", reply_markup=keyboard)
        else:
            await message.answer("Нужно ввести 3 числа через пробел!")
    except:
        await message.answer("Ошибка! Введите данные в формате: Сумма Срок Ставка")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
