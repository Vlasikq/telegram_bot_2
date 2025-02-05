from .start import register_start_handlers
from tracking import register_tracking_handlers
from .handlers import register_profile_handlers
from aiogram import Router

router = Router()

register_start_handlers(router)
register_profile_handlers(router)
register_tracking_handlers(router)
