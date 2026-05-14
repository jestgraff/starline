from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.api.starline import StarLineAPI

router = Router()

api = StarLineAPI()


@router.message(Command("status"))
async def status_handler(message: Message):

    devices = await api.get_devices()

    if not devices:
        await message.answer("Устройства не найдены")
        return

    device = devices[0]

    device_id = device["device_id"]
    device_name = device.get("alias", "Автомобиль")

    data = await api.get_device_data(device_id)

    mileage = data.get("mileage", "—")
    fuel = data.get("fuel", "—")
    balance = data.get("balance", "—")
    battery = data.get("battery", "—")

    text = f"""
🚗 {device_name}

📍 Пробег: {mileage} км
⛽ Топливо: {fuel}%
💰 Баланс SIM: {balance} ₽
🔋 АКБ: {battery}V
"""

    await message.answer(text)