from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from app.handlers.states import MaintenanceStates

from app.api.starline import StarLineAPI
from app.db.crud import create_maintenance_record

router = Router()

api = StarLineAPI()


@router.message(Command("service"))
async def start_service(
    message: Message,
    state: FSMContext
):
    await state.set_state(
        MaintenanceStates.waiting_service_type
    )

    await message.answer(
        "🔧 Введите тип ТО\n\nНапример:\n- Замена масла\n- Замена фильтров"
    )


@router.message(MaintenanceStates.waiting_service_type)
async def service_type(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        service_type=message.text
    )

    await state.set_state(
        MaintenanceStates.waiting_comment
    )

    await message.answer(
        "📝 Введите комментарий\n\nИли отправьте '-'"
    )


@router.message(MaintenanceStates.waiting_comment)
async def service_comment(
    message: Message,
    state: FSMContext
):
    comment = None

    if message.text != "-":
        comment = message.text

    await state.update_data(
        comment=comment
    )

    await state.set_state(
        MaintenanceStates.waiting_next_mileage
    )

    await message.answer(
        "📍 Через сколько км следующее ТО?\n\nНапример: 10000"
    )


@router.message(MaintenanceStates.waiting_next_mileage)
async def service_next_mileage(
    message: Message,
    state: FSMContext
):
    try:
        interval = int(message.text)

    except ValueError:
        await message.answer("Введите число")
        return

    data = await state.get_data()

    user_data = await api.get_user_data()

    devices = (
        user_data["user_data"].get("devices", [])
        + user_data["user_data"].get("shared_devices", [])
    )

    car = devices[0]

    device_id = car["device_id"]

    current_mileage = (
        car.get("obd", {})
        .get("mileage", 0)
    )

    next_service_mileage = (
        current_mileage + interval
    )

    await create_maintenance_record(
        device_id=device_id,
        service_type=data["service_type"],
        mileage=current_mileage,
        comment=data.get("comment"),
        next_service_mileage=next_service_mileage,
    )

    await state.clear()

    await message.answer(
        f"""
✅ ТО сохранено

🔧 {data["service_type"]}

📍 Текущий пробег:
{current_mileage} км

⏭ Следующее ТО:
{next_service_mileage} км
"""
    )

    
from app.db.crud import get_maintenance_history


@router.message(Command("history"))
async def history_handler(message: Message):

    user_data = await api.get_user_data()

    devices = (
        user_data["user_data"].get("devices", [])
        + user_data["user_data"].get("shared_devices", [])
    )

    if not devices:
        await message.answer("Машины не найдены")
        return

    car = devices[0]

    device_id = car["device_id"]

    history = await get_maintenance_history(device_id)

    if not history:
        await message.answer(
            "История ТО пуста"
        )
        return

    text = "📚 История ТО\n"

    for item in history:

        text += f"""

🔧 <b>{item.service_type}</b>

📍 Пробег: {item.mileage} км
📅 Дата: {item.service_date}

"""

        if item.comment:
            text += f"📝 {item.comment}\n"

        if item.next_service_mileage:
            text += (
                f"⏭ Следующее ТО: "
                f"{item.next_service_mileage} км\n"
            )

    await message.answer(
        text,
        parse_mode="HTML"
    )