import os
from pathlib import Path
from dotenv import load_dotenv

from openai import AsyncOpenAI

load_dotenv()


def create_if_not_exists(path: Path):
    """
    Creates the directory at the given path if it does not already exist.

    This function checks if the provided path exists, and if not, creates the directory
    at that path along with any necessary parent directories.

    :param path: The path of the directory to be created.
    :type path: Path
    """
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


class Config:
    """
    Class to store and manage configuration settings.

    This class loads configuration settings from environment variables and provides
    properties to access these settings. It also initializes an AsyncOpenAI client
    with the loaded settings.

    """

    # OpenAI related
    openai_api_key = os.getenv("OPENAI_API_KEY")
    assert openai_api_key is not None
    open_ai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0."))
    openai_model = os.getenv("OPENAI_MODEL")
    assert openai_model is not None
    openai_timeout = float(os.getenv("OPENAI_TIMEOUT", 30.0))

    # Project related
    project_root = Path(os.getenv("PROJECT_ROOT"))
    framework_questionnaire_yaml = Path(os.getenv("FRAMEWORK_QUESTIONNAIRE_YAML"))
    assert framework_questionnaire_yaml.exists()
    assert framework_questionnaire_yaml.is_file()

    # Initialize the OpenAI client
    open_ai_client = AsyncOpenAI(api_key=openai_api_key, timeout=openai_timeout)

    # Websocket related
    websocket_server = os.getenv("WEBSOCKET_SERVER", "0.0.0.0")
    websocket_port = int(os.getenv("WEBSOCKET_PORT", 8080))
    websocket_cors_allowed_origins = os.getenv("WEBSOCKET_CORS_ALLOWED_ORIGINS", "*")


cfg = Config()
