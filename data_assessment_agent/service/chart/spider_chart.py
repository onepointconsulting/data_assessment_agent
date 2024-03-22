from pathlib import Path
from data_assessment_agent.model.db_model import TopicScoreResult
from data_assessment_agent.config.config import cfg
from data_assessment_agent.service.chart.common import generate_topic_scores_result
from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.service.chart.common import save_figure

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

plt.style.use("ggplot")

INTERNAL_COLOR = "#4dc48d"


def generate_spider_chart(
    topic_score_result: TopicScoreResult,
    output_format="png",
    size=8,
    legend_size=16,
    add_label_positions=False,
) -> Path:
    topic_scores = topic_score_result.topic_scores
    topic_names = [score.topic_name for score in topic_scores]
    scores = [score.score for score in topic_scores]
    # Obtain Angles
    topic_names_length = len(topic_names)
    if topic_names_length == 0:
        logger.info(f"No data available for {topic_score_result.session_id}")
        return None
    angles = np.linspace(0, 2 * np.pi, topic_names_length, endpoint=False)
    # angles = np.concatenate((angles, [angles[0]]))

    # Draw the Chart
    fig = plt.figure(figsize=(size, size))
    ax = fig.add_subplot(polar=True)
    # Basic plot

    ax.plot(
        np.concatenate((angles, [angles[0]])),
        np.concatenate((scores, [scores[0]])),
        "o--",
        color=INTERNAL_COLOR,
    )

    ax.set_facecolor("#d3d3d3")

    if add_label_positions:
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
    ax.fill(angles, scores, alpha=0.5, color=INTERNAL_COLOR)

    # Add labels
    ax.set_thetagrids(angles * 180 / np.pi, topic_names)

    ax.tick_params(axis="both", which="major", pad=25, labelsize=legend_size - 3)
    ax.set_yticklabels([])

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

    return save_figure(topic_score_result.session_id, output_format, "radar")


async def generate_spider_chart_for(session_id: str, size=8, legend_size=16) -> Path:
    scores_result = await generate_topic_scores_result(session_id)
    return generate_spider_chart(scores_result, size=size, legend_size=legend_size)


if __name__ == "__main__":
    import asyncio
    from data_assessment_agent.test.provider.session_id_provider import (
        session_id_provider,
    )

    session_id = asyncio.run(session_id_provider())
    graph_path = asyncio.run(generate_spider_chart_for(session_id, size=12))
    logger.info("graph path: %s", graph_path)
