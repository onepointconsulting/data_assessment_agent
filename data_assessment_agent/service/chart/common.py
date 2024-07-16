from pathlib import Path
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

from data_assessment_agent.config.config import cfg
from data_assessment_agent.model.db_model import TopicScoreResult
from data_assessment_agent.service.persistence_service_async import select_topic_scores


CHART_GRAY = "#d3d3d3"
INTERNAL_COLOR = "#4dc48d"


async def generate_topic_scores_result(session_id: str) -> TopicScoreResult:
    topic_scores = await select_topic_scores(session_id)
    return TopicScoreResult(topic_scores=topic_scores, session_id=session_id)


def save_figure(session_id: str, output_format: str, prefix: str) -> Path:
    chart_file = cfg.chart_tmp_folder / f"{prefix}_{session_id}.{output_format}"
    plt.savefig(chart_file)
    return chart_file


def save_figure_axis(
    fig: Figure, session_id: str, output_format: str, prefix: str
) -> Path:
    chart_file = cfg.chart_tmp_folder / f"{prefix}_{session_id}.{output_format}"
    fig.savefig(chart_file)
    return chart_file
