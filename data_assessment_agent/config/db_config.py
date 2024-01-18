import asyncio
from enum import StrEnum

from data_assessment_agent.service.persistence_service_async import (
    select_config_parameters,
)


config_parameters = asyncio.run(select_config_parameters())


class DBConfigKeys(StrEnum):
    MINIMUM_TOPICS = "minimum topics"


if __name__ == "__main__":
    print(config_parameters)
