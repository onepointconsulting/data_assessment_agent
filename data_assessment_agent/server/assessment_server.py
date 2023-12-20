import socketio
from aiohttp import web

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.server.agent_session import AgentSession
from data_assessment_agent.config.config import cfg

from enum import StrEnum

sio = socketio.AsyncServer(cors_allowed_origins=cfg.websocket_cors_allowed_origins)
app = web.Application()
sio.attach(app)


class Commands(StrEnum):
    START_SESSION = "start_session"


@sio.event
async def connect(sid: str, environ):
    logger.info("connect %s %s", sid, environ)


@sio.event
async def start_session(sid, client_session):
    logger.info("start_session client_session %s", client_session)
    agent_session = AgentSession(sid, client_session)
    session_id = agent_session.session_id
    await sio.emit(Commands.START_SESSION, session_id, room=sid)


@sio.event
def disconnect(sid, environ):
    logger.info("disconnect %s ", sid)


if __name__ == "__main__":
    web.run_app(app, host=cfg.websocket_server, port=cfg.websocket_port)
