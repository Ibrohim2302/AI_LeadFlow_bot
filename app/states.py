"""FSM states used by the bot."""

from aiogram.fsm.state import State, StatesGroup


class LeadForm(StatesGroup):
    """Collect name, phone, and request for leads and orders."""

    waiting_name = State()
    waiting_phone = State()
    waiting_request = State()


class AIChat(StatesGroup):
    """Keep the user inside AI chat mode."""

    active = State()
