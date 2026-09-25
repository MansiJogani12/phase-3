import json
from app.http_compat import JSONResponse
from app.database import get_db
from app import extensions

async def get_user_count():
    cache_key = "stats:user_count"
    
    try:
        # Check Redis Cache
        if extensions.redis_client:
            cached_count = extensions.redis_client.get(cache_key)
            if cached_count:
                print("Cache hit for user count.")
                return json.loads(cached_count)
        
        # Query Database
        print("Cache miss for user count. Querying database.")
        db = get_db()
        count = db["users"].count_documents({})
        data = {"count": count}
        
        # Store in Redis
        if extensions.redis_client:
            extensions.redis_client.setex(cache_key, 3600, json.dumps(data))
            
        return JSONResponse(content=data)
    except Exception as e:
        print(f"Failed to fetch user count: {e}")
        return JSONResponse(status_code=500, content={"message": "Error fetching user count."})
