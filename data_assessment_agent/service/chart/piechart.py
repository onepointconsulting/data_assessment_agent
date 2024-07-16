from pathlib import Path

from matplotlib.figure import Figure

from data_assessment_agent.model.db_model import TotalScore
from data_assessment_agent.service.chart.common import save_figure_axis
from data_assessment_agent.service.chart.common import CHART_GRAY, INTERNAL_COLOR


def generate_pie(
    total_score: TotalScore,
    session_id: str,
    output_format="png",
) -> Path:
    labels = ["scored", "missed"]
    points = [total_score.total_score, total_score.max_score - total_score.total_score]
    colors = [INTERNAL_COLOR, CHART_GRAY]
    explode = (0.1, 0)
    fig = Figure()
    ax = fig.subplots()
    ax.pie(
        points,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        shadow=True,
        startangle=0,
    )
    ax.set_aspect(
        "equal", adjustable="datalim"
    )  # Equal aspect ratio ensures that pie is drawn as a circle.

    ax.set_title("D-Wise Score")
    return save_figure_axis(fig, session_id, output_format, "pie")


if __name__ == "__main__":
    total_score = TotalScore(total_score=110, max_score=150, pct_score=110 / 150 * 100)
    path = generate_pie(total_score, "123212312312")
    print(path)
