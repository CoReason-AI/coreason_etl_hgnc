from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore[misc]
    hgnc_json_url: HttpUrl = HttpUrl(
        "https://storage.googleapis.com/public-download-files/hgnc/json/json/hgnc_complete_set.json"
    )

    model_config = SettingsConfigDict(env_prefix="COREASON_ETL_HGNC_")


settings = Settings()
