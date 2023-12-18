from openai.types.chat.chat_completion_message import ChatCompletion

from data_assessment_agent.config.toml_support import prompts
from data_assessment_agent.config.config import cfg
from data_assessment_agent.model.ranking import question_ranking_spec


async def rank_questions(topic: str, question_answers: str, ranking_questions: str) -> ChatCompletion:
    user_prompt = prompts['ranking']['user_message']
    user_message = user_prompt.format(topic=topic, question_answers=question_answers, ranking_questions=ranking_questions)
    system_message = prompts['ranking']['system_message']
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    kwargs = {"function_call": "auto"}
    completion = await cfg.open_ai_client.chat.completions.create(
        model=cfg.openai_model,
        temperature=cfg.open_ai_temperature,
        messages=messages,
        functions=[question_ranking_spec],
        stream=True,
        **kwargs,
    )
    return completion