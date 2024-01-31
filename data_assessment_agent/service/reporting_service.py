from typing import List
import csv
import zipfile
from pathlib import Path
import datetime
from collections import defaultdict

from jinja2 import FileSystemLoader, Environment
import pdfkit

from data_assessment_agent.service.persistence_service_async import (
    select_session_report,
    select_session_qa,
)
from data_assessment_agent.model.db_model import QAScored
from data_assessment_agent.service.chart.spider_chart import generate_spider_chart_for
from data_assessment_agent.service.chart.barchart import generate_bar_chart_for
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


async def generate_html_report(session_id: str) -> Path:
    spider_chart = await generate_spider_chart_for(session_id)
    bar_chart = await generate_bar_chart_for(session_id)
    qa_scored = await select_session_qa(session_id)
    results_template = cfg.templates_folder / "results-template.html"
    questionnaire_html = generate_qa_scored(qa_scored)
    report_date = datetime.datetime.now()
    report_date_str = report_date.strftime("%a, %d %b %Y")
    context = {
        "spider_chart": spider_chart.as_posix(),
        "bar_chart": bar_chart.as_posix(),
        "questionnaire": questionnaire_html,
        "timestamp": report_date_str,
    }
    template_loader = FileSystemLoader(cfg.templates_folder)
    template_env = Environment(loader=template_loader, enable_async=True)
    template = template_env.get_template("results-template.html")
    results_template = await template.render_async(context)
    report_path: Path = cfg.report_tmp_path / f"{session_id}.html"
    report_path.write_text(results_template, encoding="utf-8")
    return report_path


async def generate_pdf_report(session_id: str) -> Path:
    report_path: Path = await generate_html_report(session_id)
    pdf_file: Path = cfg.pdf_generation_folder / f"{session_id}.pdf"
    config = pdfkit.configuration(wkhtmltopdf=cfg.wkhtmltopdf_binary.as_posix())
    pdfkit.from_string(
        report_path.read_text(encoding="utf-8"),
        pdf_file,
        configuration=config,
        options={"enable-local-file-access": ""},
    )
    return pdf_file


def generate_qa_scored(qa_scored: List[QAScored]) -> str:
    html = ""
    previous_topic = ""
    topic_scores = defaultdict(int)

    def print_score_func(topic_score):
        return f"""
<tr>
    <td>
        <b>Total:</b>
    </td>
    <td>
        <b>{topic_score}</b>
    </td>
</tr>
"""

    for i, record in enumerate(qa_scored):
        new_topic = previous_topic != record.topic
        topic = ""
        topic_scores[record.topic] += record.score
        print_score = ""
        if new_topic:
            topic_score = topic_scores[previous_topic]
            previous_topic = record.topic
            topic = f"""<h3>{record.topic}</h3>"""
            if i > 0:
                print_score = print_score_func(topic_score)

        html += f"""
{print_score}
<tr>
    <td>
        {topic}
        <p>Q: {record.question}</p>
        <p>A: {record.answer}</p>
    </td>
    <td>
        {record.score}
    </td>
</tr>
"""
    html += print_score_func(topic_scores[previous_topic])
    return html


if __name__ == "__main__":
    import asyncio

    # path = asyncio.run(generate_session_report("b8ce68f0-f754-4af8-8822-97dac817250d"))
    # print(f"Check path {path}")
    report_path = asyncio.run(
        generate_pdf_report("cf19c46c-5011-432f-bdf6-8e979ed47d23")
    )
    print(report_path)
