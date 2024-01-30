import socketio
import json
from aiohttp import web
from enum import StrEnum
from typing import Callable

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.server.agent_session import AgentSession
from data_assessment_agent.config.config import cfg
from data_assessment_agent.config.db_config import config_parameters, DBConfigKeys
from data_assessment_agent.service.data_assessment_service import (
    select_next_question,
)
from data_assessment_agent.model.assessment_framework import Question, SessionMessage
from data_assessment_agent.model.transport import ServerMessage, ConfigMessage
from data_assessment_agent.model.db_model import (
    create_questionnaire_status,
    QuestionnaireStatus,
    SelectedConfiguration,
)
from data_assessment_agent.service.sentiment_service import get_answer_sentiment
from data_assessment_agent.service.reporting_service import generate_combined_report
from data_assessment_agent.service.persistence_service_async import (
    select_last_empty_question,
    calculate_simple_total_score,
    select_suggestions,
    select_topics,
    has_selected_topics,
    select_quiz_modes,
    insert_selected_configuration,
    save_questionnaire_status,
    select_questionnaire_counts,
    find_question,
    score_on_suggested_response,
    fetch_all_suggestions,
    update_questionnaire_status_score,
)
from data_assessment_agent.service.chart.spider_chart import generate_spider_chart_for
from data_assessment_agent.service.chart.barchart import generate_bar_chart_for
from data_assessment_agent.service.suggestion_proximity_service import (
    closest_suggestion,
)

sio = socketio.AsyncServer(cors_allowed_origins=cfg.websocket_cors_allowed_origins)
app = web.Application()
sio.attach(app)

routes = web.RouteTableDef()


class Commands(StrEnum):
    START_SESSION = "start_session"
    SERVER_MESSAGE = "server_message"
    QUIZ_CONFIGURATION = "quiz_configuration"
    QUIZ_CONFIGURATION_SAVE_OK = "quiz_configuration_save_ok"
    QUIZ_CONFIGURATION_SAVE_ERROR = "quiz_configuration_save_error"


@sio.event
async def connect(sid: str, environ):
    logger.info("connect %s %s", sid, environ)


async def send_internal_error(sid: str):
    await send_error(sid, "Internal error. Please refresh the page and try again.")


async def send_error(sid: str, msg: str):
    await sio.emit(
        Commands.SERVER_MESSAGE,
        ServerMessage(response=msg, sources=None, sessionId="").model_dump_json(),
        room=sid,
    )


@sio.event
async def start_session(sid: str, client_session):
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
    # This will save the session on the client
    already_selected_topics = await has_selected_topics(session_id)
    await sio.emit(Commands.START_SESSION, session_id, room=sid)
    if not already_selected_topics:
        await init_config(sid)
    else:
        try:
            next_question = await select_next_question(session_id)
            if next_question is None:
                await send_internal_error(sid)
                return
            session_message = SessionMessage(
                next_question=next_question, sid=sid, session_id=session_id
            )
            if next_question.final:
                await handle_final_question(session_message)
            else:
                await handle_initial_question(session_message)
                await handle_next_question(session_message)
        except:
            logger.exception("Could not start session")
            await send_internal_error(sid)


@sio.event
async def client_message(sid: str, message: str):
    try:
        message_dict = json.loads(message)
        session_id = message_dict.get("id", None)
        if session_id is None:
            await send_error(
                sid, "No session id. Please refresh the page and try again."
            )
            return
        questionnaire_status = await select_last_empty_question(session_id)
        if questionnaire_status is None:
            logger.warn("There is no empty question")
            await send_internal_error(sid)
            return
        answer = message_dict.get("message", None)
        if answer is None or answer.strip() == "":
            await send_error(sid, "No message. Please refresh the page and try again.")
            return
        questionnaire_status.answer = answer
        questionnaire_status.score = 0
        await score_and_save_questionnaire_status(questionnaire_status)
        next_question = await select_next_question(session_id)
        if next_question is None:
            await send_internal_error(sid)
            return
        elif next_question.final:
            await handle_final_question(
                SessionMessage(
                    next_question=next_question, sid=sid, session_id=session_id
                )
            )
        else:
            await handle_next_question(
                SessionMessage(
                    next_question=next_question, sid=sid, session_id=session_id
                )
            )
    except:
        logger.exception("Could not process user message")
        await send_internal_error(sid)


@sio.event
async def save_configuration(sid: str, config_message: str):
    async def send_error_message(session_id: str, msg: str):
        await sio.emit(
            Commands.QUIZ_CONFIGURATION_SAVE_ERROR,
            ServerMessage(
                response=f"Error: {msg}", sessionId=session_id
            ).model_dump_json(),
            room=sid,
        )

    try:
        message_dict = json.loads(config_message)
        session_id = message_dict.get("session_id")
        if session_id is None:
            await send_error_message("", "No session id available")
            return
        topic_list = message_dict.get("topic_list")
        minimum_topics = config_parameters.get(DBConfigKeys.MINIMUM_TOPICS, "2")
        if session_id is None or len(topic_list) < int(minimum_topics):
            await send_error_message(
                session_id,
                f"At least {minimum_topics} topics are required. Please select a minimum of {minimum_topics} topics",
            )
            return
        quiz_mode_name = message_dict.get("quiz_mode_name")
        if quiz_mode_name is None:
            await send_error_message(
                session_id, "No quiz mode selected. Please select one."
            )
            return
        await insert_selected_configuration(
            SelectedConfiguration(
                session_id=session_id,
                topic_list=topic_list,
                quiz_mode_name=quiz_mode_name,
            )
        )
        await sio.emit(
            Commands.QUIZ_CONFIGURATION_SAVE_OK,
            ServerMessage(response="OK", sessionId=session_id).model_dump_json(),
            room=sid,
        )
    except:
        logger.exception("Could not save configuration")
        await send_error_message(
            "An internal error has occured. Please try again later."
        )


async def handle_next_question(session_message: SessionMessage):
    next_question, sid, session_id = (
        session_message.next_question,
        session_message.sid,
        session_message.session_id,
    )
    if next_question is None:
        await handle_missing_question(sid, session_id)
        return
    await save_incomplete_answer(session_id, next_question)
    questionnaire_counts = await select_questionnaire_counts(session_id)
    next_question.question_count = questionnaire_counts.question_count
    next_question.total_questions_in_topic = questionnaire_counts.question_total
    next_question.finished_topic_count = questionnaire_counts.finished_topic_count + 1
    next_question.topic_total = questionnaire_counts.topic_total
    next_question.suggestions = await select_suggestions(
        session_message.next_question.question, session_message.next_question.category
    )
    await send_question_to_client(sid, session_id, next_question)


async def send_question_to_client(sid: str, session_id: str, next_question: Question):
    response = f"""Topic: {next_question.category} ({next_question.finished_topic_count} out of {next_question.topic_total} topics)

Question {next_question.question_count} out of {next_question.total_questions_in_topic} in this topic

**{next_question.question}**
"""
    await sio.emit(
        Commands.SERVER_MESSAGE,
        ServerMessage(
            response=response,
            sources=None,
            sessionId=session_id,
            suggestions=next_question.suggestions,
        ).model_dump_json(),
        room=sid,
    )


async def handle_missing_question(sid: str, session_id: str):
    await sio.emit(
        Commands.SERVER_MESSAGE,
        ServerMessage(
            response="No question available. Please refresh the page and try again.",
            sessionId=session_id,
        ).model_dump_json(),
        room=sid,
    )


async def handle_initial_question(session_message: SessionMessage):
    next_question, sid, session_id = (
        session_message.next_question,
        session_message.sid,
        session_message.session_id,
    )
    topics = await select_topics()
    topics_str = ", ".join(topics)
    if next_question.initial:
        await sio.emit(
            Commands.SERVER_MESSAGE,
            ServerMessage(
                response=f"""
### Welcome to the {cfg.product_name}
The data assessment framework chatbot will now guide you through a set of questions about the following topics:

{topics_str}
""",
                sessionId=session_id,
            ).model_dump_json(),
            room=sid,
        )


async def handle_final_question(session_message: SessionMessage):
    next_question, sid, session_id = (
        session_message.next_question,
        session_message.sid,
        session_message.session_id,
    )
    if next_question.final:
        report_url = f"{cfg.report_url_base}/{session_id}"
        # Get the final score
        total_score = await calculate_simple_total_score(session_id)
        await sio.emit(
            Commands.SERVER_MESSAGE,
            ServerMessage(
                response=f"""
### Thank you for finishing the {cfg.product_name} quizz

You can download the report from [{report_url}]({report_url}).


| Result      | Score                         |
|-------------|-------------------------------|
| total score | {total_score.total_score}     |
| max score   | {total_score.max_score}       |
| percentage  | {total_score.pct_score:.2f} % |

""",
                sessionId=session_id,
            ).model_dump_json(),
            room=sid,
        )


async def score_and_save_questionnaire_status(
    questionnaire_status: QuestionnaireStatus,
):
    question = questionnaire_status.question
    answer = questionnaire_status.answer
    if answer is not None and len(answer) > 0:
        question = await find_question(
            questionnaire_status.question, questionnaire_status.topic
        )
        if question.yes_no_question:
            questionnaire_status.sentiment = await get_answer_sentiment(
                question, answer
            )
            await save_questionnaire_status(questionnaire_status)
        else:
            # Different scoring method
            questionnaire_status.score = await score_on_suggested_response(
                question.id, answer
            )
            if questionnaire_status.score is None:
                suggestions = await fetch_all_suggestions(question.id)
                # Ask ChatGPT to get the most appropriate answer for scoring.
                closest = closest_suggestion(answer, suggestions)
                questionnaire_status.score = await score_on_suggested_response(
                    question.id, closest
                )
            # Save the score into the questionnaire status
            await update_questionnaire_status_score(questionnaire_status)


async def init_config(sid: str):
    # Tell the client to select topics
    topics = await select_topics()
    quizz_modes = await select_quiz_modes()
    await sio.emit(
        Commands.QUIZ_CONFIGURATION,
        ConfigMessage(topics=topics, quizz_modes=quizz_modes).model_dump_json(),
        room=sid,
    )


async def save_incomplete_answer(session_id, next_question):
    """Before you emit, store the next question without the answer and score in tb_questionnaire_status"""
    questionnaire_status = create_questionnaire_status(session_id, next_question)
    await save_questionnaire_status(questionnaire_status=questionnaire_status)


@sio.event
def disconnect(sid, _environ):
    logger.info("disconnect %s ", sid)


# HTTP part
@routes.get("/report/{session_id}")
async def get_handler(request: web.Request) -> web.Response:
    session_id = request.match_info.get("session_id", None)
    if session_id is None:
        raise web.HTTPNotFound(text="No session id specified")
    report_path = await generate_combined_report(session_id)
    return web.FileResponse(
        report_path,
        headers={"CONTENT-DISPOSITION": f'attachment; filename="{report_path.name}"'},
    )


@routes.get("/spider_chart/{session_id}")
async def generate_spider_chart(request: web.Request) -> web.Response:
    async def chart_func(session_id: str):
        return await generate_spider_chart_for(session_id, size=12, legend_size=20)

    return await generate_chart(request, chart_func)


@routes.get("/barchart/{session_id}")
async def generate_spider_chart(request: web.Request) -> web.Response:
    async def chart_func(session_id: str):
        return await generate_bar_chart_for(session_id, size=12, width=0.6)

    return await generate_chart(request, chart_func)


async def generate_chart(request: web.Request, chart_func: Callable) -> web.Response:
    session_id = request.match_info.get("session_id", None)
    if session_id is None:
        raise web.HTTPNotFound(text="No session id specified")
    chart_path = await chart_func(session_id)
    return web.FileResponse(chart_path)


@routes.get("/topics/all")
async def topics_all(_):
    topics = await select_topics()
    return web.json_response(topics)


@routes.get("/")
async def get_handler(_):
    raise web.HTTPFound("/index.html")
