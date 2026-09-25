import uuid
from datetime import datetime
from app.database import get_db

def create_conversation(user_id: str, repository_id: str, title: str = "New Conversation"):
    conversation = {
        "_id": str(uuid.uuid4()),
        "user_id": user_id,
        "repository_id": repository_id,
        "title": title,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    get_db().conversations.insert_one(conversation)
    return conversation

def get_conversations_by_repo(user_id: str, repository_id: str):
    return list(get_db().conversations.find({
        "user_id": user_id,
        "repository_id": repository_id
    }).sort("updated_at", -1))

def get_conversation(conversation_id: str, user_id: str):
    return get_db().conversations.find_one({
        "_id": conversation_id,
        "user_id": user_id
    })

def add_message(conversation_id: str, role: str, content: str, model: str = None, provider: str = None, token_usage: dict = None, context_metadata: dict = None):
    message = {
        "_id": str(uuid.uuid4()),
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "model": model,
        "provider": provider,
        "created_at": datetime.utcnow(),
        "token_usage": token_usage or {},
        "context_metadata": context_metadata or {}
    }
    get_db().messages.insert_one(message)
    
    # Update conversation updated_at
    get_db().conversations.update_one(
        {"_id": conversation_id},
        {"$set": {"updated_at": datetime.utcnow()}}
    )
    return message

def get_messages(conversation_id: str):
    return list(get_db().messages.find({"conversation_id": conversation_id}).sort("created_at", 1))

def log_ai_request(user_id: str, repository_id: str, conversation_id: str, provider: str, model: str, latency_ms: int, success: bool, error_category: str = None, token_usage: dict = None):
    telemetry = {
        "_id": str(uuid.uuid4()),
        "user_id": user_id,
        "repository_id": repository_id,
        "conversation_id": conversation_id,
        "provider": provider,
        "model": model,
        "completed_at": datetime.utcnow(),
        "latency_ms": latency_ms,
        "success": success,
        "error_category": error_category,
        "token_usage": token_usage or {}
    }
    get_db().ai_requests.insert_one(telemetry)
    return telemetry
