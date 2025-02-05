from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

async def start(message: types.Message, state: FSMContext):
    """Запускает настройку профиля через команду /set_profile."""
    await message.answer("Привет! Чтобы настроить профиль, отправьте команду /set_profile.")
 
    await state.set_state(None)

def register_start_handlers(router: Router):
    router.message.register(start, Command("start"))



