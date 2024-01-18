async def session_id_provider() -> str:
    from data_assessment_agent.service.persistence_service_async import (
        select_random_session,
    )

    return await select_random_session()
