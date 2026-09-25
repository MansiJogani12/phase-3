import asyncio

import redis
from flask import Flask, jsonify
from flask_cors import CORS

from app.config import settings
from app.database import close_mongo_connection, connect_to_mongo, db_manager
from app import extensions
from app.routes.auth_routes import auth_bp
from app.routes.repo_routes import repo_bp
from app.routes.stats_routes import stats_bp

async def initialize_services():
    await connect_to_mongo()

    if not settings.redis_url:
        print('⚠️ REDIS_URL is not set; using in-memory session fallback.')
        return

    try:
        extensions.redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
        extensions.redis_client.ping()
        print('✅ Connected to Redis')
    except Exception as error:
        print(f'⚠️ Redis unavailable: {error}')
        extensions.redis_client = None


def create_app():
    app = Flask(__name__)
    CORS(
        app,
        origins=[
            settings.dev_frontend_url,
            'https://www.gitforme.tech',
            'https://gitforme.tech',
            'https://gitforme-jbsp.vercel.app',
            'https://gitforme-bot.onrender.com',
            'http://localhost:5173',
        ],
        supports_credentials=True,
        allow_headers=[
            'Content-Type', 'Authorization', 'X-Requested-With',
            'X-Forwarded-Proto', 'x-application',
        ],
        expose_headers=['Set-Cookie'],
    )

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(stats_bp, url_prefix='/api/stats')
    app.register_blueprint(repo_bp, url_prefix='/api/github')

    @app.get('/api/health')
    def health_check():
        mongo_status = 'ok' if db_manager.client else 'unavailable'
        redis_status = 'ok' if extensions.redis_client else 'disabled'
        healthy = mongo_status == 'ok' and redis_status in {'ok', 'disabled'}
        return jsonify({
            'status': 'ok' if healthy else 'degraded',
            'mongo': mongo_status,
            'redis': redis_status,
        }), 200 if healthy else 503

    return app


app = create_app()

if __name__ == '__main__':
    asyncio.run(initialize_services())
    try:
        app.run(host='0.0.0.0', port=settings.port, debug=False)
    finally:
        asyncio.run(close_mongo_connection())
