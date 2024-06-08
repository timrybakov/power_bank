from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str
    redis_host: str
    redis_port: int
    redis_db: int
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    secret_key: str
    algorithm: str

    model_config = SettingsConfigDict(env_file='.env')
