from pathlib import Path

import matplotlib.pyplot as plt

from data_assessment_agent.config.config import cfg
from data_assessment_agent.model.db_model import TopicScoreResult
from data_assessment_agent.service.persistence_service_async import select_topic_scores


async def generate_topic_scores_result(session_id: str) -> TopicScoreResult:
    topic_scores = await select_topic_scores(session_id)
    return TopicScoreResult(topic_scores=topic_scores, session_id=session_id)


def save_figure(session_id: str, output_format: str, prefix: str) -> Path:
    chart_file = cfg.chart_tmp_folder / f"{prefix}_{session_id}.{output_format}"
    plt.savefig(chart_file)
    return chart_file
