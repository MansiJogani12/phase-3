from flask import Blueprint
from app.controllers.stats_controller import get_user_count

stats_bp = Blueprint('stats', __name__)


@stats_bp.get('/user-count')
async def stats_user_count():
    return await get_user_count()
