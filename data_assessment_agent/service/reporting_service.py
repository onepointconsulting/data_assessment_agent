import csv
from pathlib import Path

from data_assessment_agent.service.persistence_service import select_session_report
from data_assessment_agent.config.config import cfg


def generate_session_report(session_id: str) -> Path:
    sessions = select_session_report(session_id)
    tmp_path = cfg.report_tmp_path / f"{session_id}.csv"
    with open(tmp_path, "w", newline="") as f:
        wr = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        wr.writerow(
            [
                "TOPIC",
                "QUESTION",
                "ANSWER",
                "SCORE",
                "SENTIMENT",
                "CREATED_AT",
                "UPDATED_AT",
            ]
        )
        for session in sessions:
            wr.writerow(
                [
                    session.topic,
                    session.question,
                    session.answer,
                    session.score,
                    session.sentiment,
                    session.created_at.isoformat(),
                    session.updated_at.isoformat(),
                ]
            )
    return tmp_path


if __name__ == "__main__":
    path = generate_session_report("b8ce68f0-f754-4af8-8822-97dac817250d")
    print(f"Check path {path}")
