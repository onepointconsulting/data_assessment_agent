import asyncio

from aiohttp import web
from data_assessment_agent.config.config import cfg
from data_assessment_agent.server.assessment_server import app, routes


if __name__ == "__main__":
    app.add_routes(routes)
    app.router.add_static("/", path=cfg.ui_folder.as_posix(), name="ui")
    loop = asyncio.new_event_loop()

    web.run_app(app, host=cfg.websocket_server, port=cfg.websocket_port, loop=loop)
