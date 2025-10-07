from unittest.mock import AsyncMock

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from bot import CalcState, calc_choice, cmd_start, credit_calc, show_main_menu


@pytest.mark.asyncio
async def test_show_main_menu():
    message = AsyncMock()
    await show_main_menu(message)
    message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_cmd_start():
    message = AsyncMock()
    await cmd_start(message)
    message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_calc_choice_credit():
    message = AsyncMock(text="Кредитный калькулятор")
    state = FSMContext(storage=MemoryStorage(), key="test")
    await calc_choice(message, state)
    assert await state.get_state() == CalcState.waiting_credit.state


@pytest.mark.asyncio
async def test_credit_calc_success():
    message = AsyncMock(text="100000 12 15")
    state = FSMContext(storage=MemoryStorage(), key="test")
    await state.set_state(CalcState.waiting_credit)
    await credit_calc(message, state)
    assert "Ежемесячный платеж" in message.answer.call_args_list[0][0][0]
