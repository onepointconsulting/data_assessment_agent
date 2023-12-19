import os
from pathlib import Path
from dotenv import load_dotenv

from openai import AsyncOpenAI

load_dotenv()


def create_if_not_exists(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


class Config:
    # OpenAI related
    openai_api_key = os.getenv("OPENAI_API_KEY")
    assert openai_api_key is not None
    open_ai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0."))
    openai_model = os.getenv("OPENAI_MODEL")
    assert openai_model is not None
    openai_timeout = float(os.getenv("OPENAI_TIMEOUT", 30.0))
    open_ai_client = AsyncOpenAI(api_key=openai_api_key, timeout=openai_timeout)
    project_root = Path(os.getenv("PROJECT_ROOT"))
    framework_questionnaire_yaml = Path(os.getenv("FRAMEWORK_QUESTIONNAIRE_YAML"))
    assert framework_questionnaire_yaml.exists()
    assert framework_questionnaire_yaml.is_file()


cfg = Config()
