from pydantic import BaseSettings
from functools import lru_cache


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    hospital_info_csv_file_name: str = ""
    hospital_treatment_csv_file_name: str = ""