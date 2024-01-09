from typing import List
import csv
import zipfile
from pathlib import Path

from data_assessment_agent.service.persistence_service_async import (
    select_session_report,
)
from data_assessment_agent.service.spider_chart import generate_spider_chart_for
from data_assessment_agent.config.config import cfg


async def generate_session_report(session_id: str) -> Path:
    sessions = await select_session_report(session_id)
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


async def generate_combined_report(session_id: str) -> Path:
    qa_report = await generate_session_report(session_id)
    spider_chart = await generate_spider_chart_for(session_id)
    files_to_zip = [qa_report, spider_chart]
    zip_file = cfg.report_tmp_path / f"{session_id}.zip"
    compress_zip_file(zip_file, files_to_zip)
    return zip_file


def compress_zip_file(zip_file: Path, files_to_zip: List[Path]):
    compression = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for file in files_to_zip:
            if file.exists():
                zf.write(file, file.name, compress_type=compression)


if __name__ == "__main__":
    import asyncio

    path = asyncio.run(generate_session_report("b8ce68f0-f754-4af8-8822-97dac817250d"))
    print(f"Check path {path}")
