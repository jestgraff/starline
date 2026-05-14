from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.api.starline import StarLineAPI

router = Router()

api = StarLineAPI()


@router.message(Command("status"))
async def status_handler(message: Message):

    try:
        user_data = await api.get_user_data()

        devices = user_data.get("devices", [])

        if not devices:
            await message.answer("Устройства не найдены")
            return

        device = devices[0]

        device_id = device["device_id"]
        device_name = device.get("alias", "Автомобиль")

        data = await api.get_device_data(device_id)

        # Тут структура может отличаться
        # поэтому пока просто выводим JSON

        await message.answer(
            f"🚗 {device_name}\n\n"
            f"<pre>{data}</pre>",
            parse_mode="HTML"
        )

    except Exception as e:
        await message.answer(f"Ошибка:\n<pre>{str(e)}</pre>", parse_mode="HTML")