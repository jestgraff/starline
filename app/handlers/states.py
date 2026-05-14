from aiogram.fsm.state import StatesGroup, State


class MaintenanceStates(StatesGroup):
    waiting_service_type = State()
    waiting_comment = State()
    waiting_next_mileage = State()