from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.api.starline import StarLineAPI

router = Router()

api = StarLineAPI()


@router.message(Command("status"))
async def status_handler(message: Message):

    try:
        data = await api.get_user_data()

        devices = (
            data["user_data"].get("devices", [])
            + data["user_data"].get("shared_devices", [])
        )

        if not devices:
            await message.answer("Машины не найдены")
            return

        car = devices[0]

        alias = car.get("alias", "Автомобиль")

        obd = car.get("obd", {})
        common = car.get("common", {})
        state = car.get("state", {})
        position = car.get("position", {})
        balance = car.get("balance", [])

        mileage = obd.get("mileage", "—")
        fuel = obd.get("fuel_litres", "—")

        battery = common.get("battery", "—")
        engine_temp = common.get("etemp", "—")

        armed = "Да" if state.get("arm") else "Нет"
        engine = "Запущен" if state.get("run") else "Остановлен"

        lat = position.get("y")
        lon = position.get("x")

        sim_balance = "—"

        if balance:
            sim_balance = f'{balance[0].get("value")} ₽'

        text = f"""
🚗 <b>{alias}</b>

🛡 Охрана: <b>{armed}</b>
🔧 Двигатель: <b>{engine}</b>

📍 Пробег: <b>{mileage} км</b>
⛽ Топливо: <b>{fuel} л</b>

🔋 АКБ: <b>{battery}V</b>
🌡 Температура: <b>{engine_temp}°C</b>

💰 Баланс SIM: <b>{sim_balance}</b>

📌 Координаты:
<code>{lat}, {lon}</code>
"""

        await message.answer(
            text,
            parse_mode="HTML"
        )

    except Exception as e:
        await message.answer(str(e))
        raise