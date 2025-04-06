from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    
    cerebras_api_key : str = Field(..., validate_alias="CEREBRAS_API_KEY")
    cerebras_base_url : str = Field(..., validate_alias="CEREBRAS_BASE_URL")
    
    class Config:
        env_file = ".env"

