import socketio
import json
from aiohttp import web
import asyncer

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.server.agent_session import AgentSession
from data_assessment_agent.config.config import cfg
from data_assessment_agent.service.data_assessment_service import (
    initial_question,
    select_next_question,
)
from data_assessment_agent.service.persistence_service import save_questionnaire_status
from data_assessment_agent.model.db_model import create_questionnaire_status
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
        next_question = select_next_question(session_id)
    # Before you emit, store the next question without the answer and score in tb_questionnaire_status
    questionnaire_status = create_questionnaire_status(session_id, next_question)
    await asyncer.asyncify(save_questionnaire_status)(
        questionnaire_status=questionnaire_status
    )
    await sio.emit(
        Commands.SERVER_MESSAGE,
        ServerMessage(
            response=next_question.question, sources=None, sessionId=session_id
        ).model_dump_json(),
        room=sid,
    )


@sio.event
async def client_message(sid, message):
    (id, _, message) = json.loads(message)
    session_id = id
    


@sio.event
def disconnect(sid, environ):
    logger.info("disconnect %s ", sid)


if __name__ == "__main__":
    web.run_app(app, host=cfg.websocket_server, port=cfg.websocket_port)
