def create_sentiment_qa():
    question = "What is the strength and composition of the analytics team?"
    answer = "We have 10 data analystis, 5 reporting exports, 5 ML experts and 1 deep learning expert"
    return question, answer


def create_sentiment_negative_qa():
    question = "What is the strength and composition of the analytics team?"
    answer = "Right now we are still building our analytics team."
    return question, answer


def create_positive_intention():
    question = "Are there gaps or misalignments to address between your data strategy and your business strategy?"
    answer = (
        "Yes, there are large gaps available between our data and business strategy."
    )
    return question, answer
