from flask import Blueprint, request, redirect
from app.controllers.auth_controller import github_callback, verify_user, logout
from app.config import settings

auth_bp = Blueprint('auth', __name__)


@auth_bp.get('/github')
async def github_login():
    url = (
        'https://github.com/login/oauth/authorize'
        f'?client_id={settings.github_client_id}&scope=user:email'
    )
    return redirect(url)


@auth_bp.get('/github/callback')
async def github_callback_route():
    return await github_callback(request.args.get('code'))


@auth_bp.post('/verifyUser')
async def verify_user_route():
    return await verify_user(request.args.get('token'))


@auth_bp.post('/logout')
async def logout_route():
    return await logout()
