from typing import Union
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.model.db_model import TopicScoreResult
from data_assessment_agent.service.chart.common import (
    generate_topic_scores_result,
    save_figure,
)


def generate_bar_chart(
    scores_result: TopicScoreResult, width: float = 6, output_format="png", size=8
) -> Union[Path, None]:
    if len(scores_result.topic_scores) == 0:
        logger.error(f"No results to print for {scores_result.session_id}")
        return None
    topics = [topic_score.topic_name for topic_score in scores_result.topic_scores]
    scores = {
        "Actual Score": np.array(
            [topic_score.score for topic_score in scores_result.topic_scores]
        ),
        "Max score": np.array(
            [topic_score.max_score - topic_score.score for topic_score in scores_result.topic_scores]
        ),
    }

    _, ax = plt.subplots(figsize=[int(size * 1.5), size])
    bottom = np.zeros(len(topics))
    for scores_type, score_counts in scores.items():
        p = ax.bar(topics, score_counts, width, label=scores_type, bottom=bottom)
        bottom += score_counts
        ax.bar_label(p, label_type="center")

    ax.set_title("Topic scores")
    ax.legend()

    return save_figure(
        scores_result.session_id, output_format=output_format, prefix="barchart"
    )


async def generate_bar_chart_for(session_id: str, width: float = 0.6, size: int = 8) -> Path:
    scores_result = await generate_topic_scores_result(session_id)
    return generate_bar_chart(scores_result, width=width, size=size)


if __name__ == "__main__":
    import asyncio
    from data_assessment_agent.test.provider.session_id_provider import (
        session_id_provider,
    )
    from data_assessment_agent.config.log_factory import logger

    for i in range(20):
        session_id = asyncio.run(session_id_provider())
        graph_path = asyncio.run(generate_bar_chart_for(session_id, width=0.6))
        logger.info("graph path: %s", graph_path)
