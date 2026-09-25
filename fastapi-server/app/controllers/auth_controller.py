import httpx
import jwt
from datetime import datetime, timedelta
from app.http_compat import RedirectResponse, JSONResponse
from bson.objectid import ObjectId
from app.config import settings
from app.database import get_db

async def github_callback(code: str):
    print('[GitHub OAuth] Callback initiated...')
    if not code:
        return JSONResponse(status_code=400, content={"error": "No authorization code received."})
        
    try:
        async with httpx.AsyncClient() as client:
            # 1. Exchange code for access token from GitHub
            print('[GitHub OAuth] Step 1: Exchanging code for access token...')
            token_res = await client.post(
                'https://github.com/login/oauth/access_token',
                json={
                    'client_id': settings.github_client_id,
                    'client_secret': settings.github_client_secret,
                    'code': code
                },
                headers={'Accept': 'application/json'}
            )
            
            token_data = token_res.json()
            access_token = token_data.get('access_token')
            if not access_token:
                print('[GitHub OAuth] ❌ Failure: Could not retrieve access token from GitHub.')
                return JSONResponse(status_code=500, content={"error": "Could not retrieve access token."})
                
            print('[GitHub OAuth] ✅ Access token received.')
            
            # 2. Get user info from GitHub
            print('[GitHub OAuth] Step 2: Fetching user info from GitHub...')
            user_res = await client.get(
                'https://api.github.com/user',
                headers={'Authorization': f'token {access_token}'}
            )
            github_user = user_res.json()
            github_id = str(github_user.get('id'))
            print(f'[GitHub OAuth] ✅ User fetched: {github_user.get("login")} (ID: {github_id})')
            
            # 3. Find or create the user in your database
            db = get_db()
            print('[GitHub OAuth] Step 3: Checking if user exists in DB...')
            user = db["users"].find_one({"githubId": github_id})
            
            if not user:
                print('[GitHub OAuth] New user. Creating entry...')
                new_user = {
                    "githubId": github_id,
                    "username": github_user.get("login"),
                    "email": github_user.get("email") or f"{github_user.get('login')}@users.noreply.github.com",
                    "githubAccessToken": access_token,
                    "createdAt": datetime.utcnow()
                }
                result = db["users"].insert_one(new_user)
                user_id = str(result.inserted_id)
                print('[GitHub OAuth] ✅ New user created.')
            else:
                print('[GitHub OAuth] Existing user found. Updating access token...')
                user_id = str(user["_id"])
                db["users"].update_one(
                    {"_id": user["_id"]},
                    {"$set": {
                        "githubAccessToken": access_token,
                        "username": github_user.get("login")
                    }}
                )
                print('[GitHub OAuth] ✅ User updated.')

            # 5. Create the JWT token for the fallback system
            print('[GitHub OAuth] Step 5: Creating fallback JWT token...')
            payload = {
                "userId": user_id,
                "exp": datetime.utcnow() + timedelta(days=1)
            }
            fallback_token = jwt.encode(payload, settings.token_secret, algorithm="HS256")
            print('[GitHub OAuth] ✅ JWT created.')
            
            # 6. Redirect to the frontend, passing the token in the URL
            print('[GitHub OAuth] Step 6: Redirecting user to frontend...')
            return RedirectResponse(url=f"{settings.dev_frontend_url}?success=true&token={fallback_token}")
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f'Error during GitHub authentication: {e}', flush=True)
        return RedirectResponse(url=f"{settings.dev_frontend_url}/login?error=auth_failed")


async def verify_user(token: str):
    print('[VerifyUser] Checking token...')
    if not token:
        return JSONResponse(status_code=401, content={"status": False, "message": "No token provided"})
        
    try:
        decoded = jwt.decode(token, settings.token_secret, algorithms=["HS256"])
        user_id = decoded.get("userId")
        
        db = get_db()
        user = db["users"].find_one({"_id": ObjectId(user_id)})
        
        if not user:
            return JSONResponse(status_code=401, content={"status": False, "message": "Invalid token"})
            
        # Remove sensitive data
        user.pop("password", None)
        user.pop("githubAccessToken", None)
        user["_id"] = str(user["_id"])
        
        print(f"[VerifyUser] ✅ Token valid for user: {user.get('username')}")
        return JSONResponse(content={"status": True, "user": user})
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f'[VerifyUser] ❌ Token verification failed: {e}', flush=True)
        return JSONResponse(status_code=401, content={"status": False, "message": "Invalid token"})

async def logout():
    return JSONResponse(content={"status": True, "message": "Logged out Successfully."})
