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
    assert path.exists(), f"Path {path} does not exist."


def create_folder_property(key: str) -> Path:
    prop_str = os.getenv(key)
    assert prop_str is not None, f"Make sure you have defined the {key} property"
    prop_folder = Path(prop_str)
    create_if_not_exists(prop_folder)
    return prop_folder


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
    product_name = os.getenv("PRODUCT_NAME")
    assert product_name is not None

    # Initialize the OpenAI client
    open_ai_client = AsyncOpenAI(api_key=openai_api_key, timeout=openai_timeout)

    # Websocket related
    websocket_server = os.getenv("WEBSOCKET_SERVER", "0.0.0.0")
    websocket_port = int(os.getenv("WEBSOCKET_PORT", 8080))
    websocket_cors_allowed_origins = os.getenv("WEBSOCKET_CORS_ALLOWED_ORIGINS", "*")

    # Reporting
    report_tmp_path_str = os.getenv("REPORT_TMP_PATH")
    assert report_tmp_path_str is not None
    report_tmp_path = Path(report_tmp_path_str)
    create_if_not_exists(report_tmp_path)
    report_url_base = os.getenv("REPORT_URL_BASE")
    assert report_url_base is not None

    # UI
    ui_folder = create_folder_property("UI_FOLDER")

    # Charts
    chart_tmp_folder = create_folder_property("CHART_TMP_FOLDER")


class DBConfig:
    db_name = os.getenv("DB_NAME")
    assert db_name is not None
    db_user = os.getenv("DB_USER")
    assert db_user is not None
    db_host = os.getenv("DB_HOST")
    assert db_host is not None
    db_port = os.getenv("DB_PORT")
    assert db_port is not None
    db_port = int(db_port)
    db_password = os.getenv("DB_PASSWORD")
    assert db_password is not None

    db_conn_str = f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"


cfg = Config()

db_cfg = DBConfig()
