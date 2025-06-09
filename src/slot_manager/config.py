import os
from pathlib import Path
from dotenv import load_dotenv


def load_env(env_file: str = ".env"):
    if Path(env_file).exists():
        load_dotenv(env_file)


def get_env(name: str, default=None, required: bool = False):
    value = os.getenv(name, default)
    if required and value is None:
        raise RuntimeError(f"Environment variable {name} is required")
    return value
