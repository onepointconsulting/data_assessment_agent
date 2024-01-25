from data_assessment_agent.config.toml_support import prompts


def create_user_message(question: str, answer: str, topic: str) -> str:
    user_prompt = prompts["answer-quality"]["user_message"]
    return user_prompt.format(question=question, answer=answer, topic=topic)


if __name__ == "__main__":
    pass
