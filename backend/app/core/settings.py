from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str = ""
    jira_domain: str = ""
    jira_email: str = ""
    jira_api_token: str = ""

    class Config:
        env_file = ".env"

settings = Settings()