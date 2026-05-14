import traceback
import json

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

        print("\n=== USER DATA ===")
        print(json.dumps(user_data, indent=2, ensure_ascii=False))

        devices = user_data.get("devices", [])

        if not devices:
            await message.answer(
                f"devices пустой\n\n<pre>{json.dumps(user_data, indent=2, ensure_ascii=False)}</pre>",
                parse_mode="HTML"
            )
            return

        device = devices[0]

        device_id = device["device_id"]

        data = await api.get_device_data(device_id)

        print("\n=== DEVICE DATA ===")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        await message.answer(
            f"<pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>",
            parse_mode="HTML"
        )

    except Exception as e:

        error_text = traceback.format_exc()

        print(error_text)

        await message.answer(
            f"<pre>{error_text}</pre>",
            parse_mode="HTML"
        )