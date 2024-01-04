from typing import Union, Any

import asyncio
import sys
from typing import Callable

from psycopg_pool import AsyncConnectionPool
from data_assessment_agent.config.config import db_cfg
from data_assessment_agent.model.db_model import QuestionnaireStatus


def create_pool():
    async_pool = AsyncConnectionPool(conninfo=db_cfg.db_conn_str, open=False)
    print("Using", db_cfg.db_conn_str)
    return async_pool


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asynch_pool = create_pool()


async def open_pool():
    await asynch_pool.open()
    await asynch_pool.wait()
    print("Connection Pool Opened")

asyncio.run(open_pool())


async def create_cursor(func: Callable) -> Any:
    async with asynch_pool.connection() as conn:
        async with conn.cursor() as cur:
            print("Cursor type: ", type(cur))
            return await func(cur)


async def select_last_question(session_id: str) -> Union[QuestionnaireStatus, None]:
    async def handle_select(cur):
        await cur.execute(
            """
SELECT S.ID,
	S.SESSION_ID,
	S.TOPIC,
	S.QUESTION,
	S.ANSWER,
	S.SCORE,
	S.CREATED_AT,

	(SELECT COUNT(DISTINCT(QS1.QUESTION))
		FROM PUBLIC.TB_QUESTIONNAIRE_STATUS QS1
		WHERE QS1.SESSION_ID = %(session_id)s
			AND QS1.TOPIC = S.TOPIC
			AND ANSWER IS NOT NULL) TOPIC_COUNT,

	(SELECT T.QUESTION_AMOUNT - COUNT(DISTINCT(QS1.QUESTION))
		FROM PUBLIC.TB_QUESTIONNAIRE_STATUS QS1
		WHERE QS1.SESSION_ID = %(session_id)s
			AND QS1.TOPIC = S.TOPIC
			AND QS1.ANSWER IS NOT NULL) TOPIC_MISSING,

    (SELECT COUNT(*) FROM PUBLIC.TB_QUESTIONNAIRE_STATUS QS2
		WHERE QS2.QUESTION = S.QUESTION AND QS2.SESSION_ID = S.SESSION_ID 
	 		AND QS2.ANSWER IS NOT NULL) PREVIOUS_ANSWER_COUNT
FROM PUBLIC.TB_QUESTIONNAIRE_STATUS S
INNER JOIN TB_TOPIC T ON T.NAME = S.TOPIC
WHERE SESSION_ID = %(session_id)s
ORDER BY ID DESC
LIMIT 1""",
            {"session_id": session_id},
        )
        return list(await cur.fetchall())

    statuses: list = await create_cursor(handle_select)
    if len(statuses) == 0:
        return None
    (
        id,
        db_session_id,
        topic,
        question,
        answer,
        score,
        created_at,
        topic_count,
        topic_missing,
        previous_answer_count,
    ) = statuses[0]
    return QuestionnaireStatus(
        id=id,
        session_id=db_session_id,
        topic=topic,
        question=question,
        answer=answer,
        score=score,
        created_at=created_at,
        topic_count=topic_count,
        topic_missing=topic_missing,
        previous_answer_count=previous_answer_count,
    )


async def select_random_session() -> Union[str, None]:
    async def handle_select(cur):
        await cur.execute(
            """
select session_id from public.tb_questionnaire_status order by random() limit 1
"""
        )
        return list(await cur.fetchall())

    session_ids: list = await create_cursor(handle_select)
    if len(session_ids) > 0:
        return session_ids[0][0]
    return None


if __name__ == "__main__":

    async def test_select_last_session():
        session_id = await select_random_session()
        print(session_id)
        last_question = await select_last_question(session_id)
        print(last_question)
    # if session_id is not None:
    #     print(session_id)
        
    asyncio.run(test_select_last_session())

    
