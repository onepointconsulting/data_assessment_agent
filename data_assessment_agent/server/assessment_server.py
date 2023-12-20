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
async def connect(sid, environ):
    logger.info("connect %s ", sid)
    agent_session = AgentSession(sid, None)
    session_id = agent_session.session_id
    await sio.emit(Commands.START_SESSION, session_id, room=sid)


@sio.event
def disconnect(sid, environ):
    logger.info("disconnect %s ", sid)


if __name__ == "__main__":
    web.run_app(app, host=cfg.websocket_server, port=cfg.websocket_port)
