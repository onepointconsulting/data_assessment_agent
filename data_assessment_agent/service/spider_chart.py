from typing import List
from pathlib import Path
from data_assessment_agent.model.db_model import TopicScoreResult
from data_assessment_agent.config.config import cfg
from data_assessment_agent.service.persistence_service_async import select_topic_scores

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

plt.style.use("ggplot")


def generate_spider_chart(
    topic_score_result: TopicScoreResult, output_format="png", size=8, legend_size=16
) -> Path:
    topic_scores = topic_score_result.topic_scores
    topic_names = [score.topic_name for score in topic_scores]
    scores = [score.score for score in topic_scores]
    max_scores = [score.max_score for score in topic_scores]
    # Obtain Angles
    angles = np.linspace(0, 2 * np.pi, len(topic_names), endpoint=False)
    # angles = np.concatenate((angles, [angles[0]]))

    # Draw the Chart
    fig = plt.figure(figsize=(size, size))
    ax = fig.add_subplot(polar=True)
    # Basic plot

    ax.plot(
        np.concatenate((angles, [angles[0]])),
        np.concatenate((scores, [scores[0]])),
        "o--",
        color="g",
    )

    label_position = ax.get_rlabel_position()
    ax.text(
        np.radians(label_position + 10),
        ax.get_rmax() / 2.0,
        "Score points",
        rotation=label_position,
        ha="center",
        va="center",
    )

    # fill plot
    ax.fill(angles, scores, alpha=0.25, color="g")
    # Add labels
    ax.set_thetagrids(angles * 180 / np.pi, topic_names)

    ax.tick_params(axis="both", which="major", pad=25, labelsize=legend_size - 3)

    ax.set_title(
        "Topic Scores",
        weight="bold",
        size=legend_size,
        position=(0.5, 1.1),
        horizontalalignment="center",
        verticalalignment="center",
    )

    ax.legend(
        ["Assessment scores perimeter", "Assessment score area"],
        loc="lower left",
        bbox_to_anchor=(-0.1, -0.1),
    )

    # Font size
    matplotlib.rcParams.update({"font.size": legend_size - 2})

    plt.grid(True)
    plt.tight_layout()

    chart_file = (
        cfg.chart_tmp_folder / f"{topic_score_result.session_id}.{output_format}"
    )
    plt.savefig(chart_file)
    return chart_file


async def generate_spider_chart_for(session_id: str, size=8, legend_size=16) -> Path:
    topic_scores = await select_topic_scores(session_id)
    scores_result = TopicScoreResult(topic_scores=topic_scores, session_id=session_id)
    return generate_spider_chart(scores_result, size=size, legend_size=legend_size)


if __name__ == "__main__":
    import asyncio
    from data_assessment_agent.service.persistence_service_async import (
        select_random_session,
    )
    from data_assessment_agent.config.log_factory import logger

    session_id = asyncio.run(select_random_session())
    graph_path = asyncio.run(generate_spider_chart_for(session_id, size=12))
    logger.info("graph path: %s", graph_path)
