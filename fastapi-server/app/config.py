from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env_name: str = "development"
    port: int = 3000
    dev_frontend_url: str = "http://localhost:5173"
    dev_backend_url: str = "http://localhost:3000"
    
    redis_url: str = "redis://localhost:6379"
    mongo_url: str = "mongodb://localhost:27017/gitforme-dev"
    
    session_secret: str = "your-dev-session-secret"
    token_secret: str = "your-dev-token-secret"
    github_client_id: str = "your-dev-github-client-id"
    github_client_secret: str = "your-dev-github-client-secret"
    
    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
