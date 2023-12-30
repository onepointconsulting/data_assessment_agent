import socketio
import json
from aiohttp import web

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.server.agent_session import AgentSession
from data_assessment_agent.config.config import cfg
from data_assessment_agent.service.data_assessment_service import (
    initial_question,
    select_next_question,
)
from data_assessment_agent.service.persistence_service import (
    save_questionnaire_status,
    select_last_empty_question,
)
from data_assessment_agent.model.db_model import create_questionnaire_status
from data_assessment_agent.model.assessment_framework import Question
from data_assessment_agent.model.transport import ServerMessage

from enum import StrEnum

sio = socketio.AsyncServer(cors_allowed_origins=cfg.websocket_cors_allowed_origins)
app = web.Application()
sio.attach(app)


class Commands(StrEnum):
    START_SESSION = "start_session"
    SERVER_MESSAGE = "server_message"


@sio.event
async def connect(sid: str, environ):
    logger.info("connect %s %s", sid, environ)


async def send_error(sid: str, msg: str):
    await sio.emit(
        Commands.SERVER_MESSAGE,
        ServerMessage(response=msg, sources=None, sessionId="").model_dump_json(),
        room=sid,
    )


@sio.event
async def start_session(sid, client_session):
    """
    Start the session.

    Query by session id and try to get the current topic and how many items were processed in it.
        if there is a current topic, then check the count and verify if it is less than the total amount of quetions we want to ask.
            If there are less question that the the threshold, use ChatGPt to generate a ranking and then pick the top question and send it
            Else if you need another topic, ask ChatGPT to choose the next topic, then pick a question in that topic and send it
        if there is no topic, select the first question in the database and send it

    """
    logger.info("start_session client_session %s", client_session)
    agent_session = AgentSession(sid, client_session)
    session_id = agent_session.session_id
    await sio.emit(Commands.START_SESSION, session_id, room=sid)
    no_session_available = client_session is None or client_session == ""
    if no_session_available:
        next_question = initial_question()
    else:
        next_question = await select_next_question(session_id)
    if next_question is None:
        await handle_missing_question(sid, session_id)
        return
    save_incomplete_answer(session_id, next_question)
    await send_question_to_client(sid, session_id, next_question)


@sio.event
async def client_message(sid: str, message):
    message_dict = json.loads(message)
    session_id = message_dict.get("id", None)
    if session_id is None:
        await send_error(sid, "No session id. Please refresh the page and try again.")
        return
    questionnaire_status = select_last_empty_question(session_id)
    if questionnaire_status is None:
        await send_error(sid, "Internal error. Please refresh the page and try again.")
        return
    answer = message_dict.get("message", None)
    if answer is None or answer.strip() == "":
        await send_error(sid, "No message. Please refresh the page and try again.")
        return
    questionnaire_status.answer = answer
    # TODO: Scoring will be defined later.
    questionnaire_status.score = 0
    save_questionnaire_status(questionnaire_status)
    next_question = await select_next_question(session_id)
    if next_question is None:
        await handle_missing_question(sid, session_id)
        return
    save_incomplete_answer(session_id, next_question)
    await send_question_to_client(sid, session_id, next_question)


async def send_question_to_client(sid: str, session_id: str, next_question: Question):
    response = f"""Topic: {next_question.category}

**{next_question.question}**
"""
    await sio.emit(
        Commands.SERVER_MESSAGE,
        ServerMessage(
            response=response, sources=None, sessionId=session_id
        ).model_dump_json(),
        room=sid,
    )

async def handle_missing_question(sid: str, session_id: str):
    await sio.emit(
        Commands.SERVER_MESSAGE,
        ServerMessage(
            response="No question available. Please refresh the page and try again.", sources=None, sessionId=session_id
        ).model_dump_json(),
        room=sid,
    )


def save_incomplete_answer(session_id, next_question):
    """Before you emit, store the next question without the answer and score in tb_questionnaire_status"""
    questionnaire_status = create_questionnaire_status(session_id, next_question)
    save_questionnaire_status(questionnaire_status=questionnaire_status)


@sio.event
def disconnect(sid, environ):
    logger.info("disconnect %s ", sid)


if __name__ == "__main__":
    web.run_app(app, host=cfg.websocket_server, port=cfg.websocket_port)
