import asyncio

from aiogram import Dispatcher, Bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from creds import TOKEN
router = Router()
dp = Dispatcher()
bot = Bot(token=TOKEN)


class OrderCredit(StatesGroup):
    wait_credit_sum = State()
    first_part_payment = State()


@router.message(Command("start"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Приветствуем в сервисе ДомКлик!"
             "Мы рады предложить наши условия для любых клиентов. "
             "Чтобы изучить предложения, введите предполагаемую сумму кредита: "
    )
    await state.set_state(OrderCredit.wait_credit_sum)


@router.message(OrderCredit.wait_credit_sum, F)
async def part_payment_chosen(message: Message, state: FSMContext):
    await state.update_data(all_sum=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите сумму первоначального взноса:",
    )
    await state.set_state(OrderCredit.first_part_payment)


@router.message(OrderCredit.first_part_payment)
async def part_pay_process(message: Message, state: FSMContext):
    try:
        int(message.text)
    except Exception as e:
        await message.answer(text='Введите только числовое значение первоначального взноса')
    user_data = await state.get_data()
    if int(message.text) < (int(user_data['all_sum']) * 15) / 100:
        await message.answer(text='Сумма первоначального взноса меньше 15%. '
                                  'К сожалению, этого недостаточно :(.')
    await message.answer(
        text="Готовы выслать вам предложения!"
    )


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
