import jwt
from bson.objectid import ObjectId
from flask import request
from app.config import settings
from app.database import get_db


async def require_auth():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None

    try:
        decoded = jwt.decode(
            auth_header.removeprefix('Bearer ').strip(),
            settings.token_secret,
            algorithms=['HS256'],
        )
        user_id = decoded.get('userId')
        user = get_db()['users'].find_one({'_id': ObjectId(user_id)})
        return str(user['_id']) if user else None
    except Exception:
        return None
