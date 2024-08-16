from typing import List
import csv
import zipfile
import shutil
from pathlib import Path
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
from data_assessment_agent.utils.date_utils import generate_footer_date
from data_assessment_agent.service.maturity_level_service import (
    generate_maturity_level_report,
    create_maturity_level_report_context,
)
from data_assessment_agent.service.report_helper import generate_report_date


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
    maturity_level_path = await generate_maturity_level_report(session_id)
    files_to_zip = [qa_report, spider_chart, maturity_level_path]
    zip_file = cfg.report_tmp_path / f"{session_id}.zip"
    compress_zip_file(zip_file, files_to_zip)
    return zip_file


def compress_zip_file(zip_file: Path, files_to_zip: List[Path]):
    compression = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for file in files_to_zip:
            if file.exists():
                zf.write(file, file.name, compress_type=compression)


async def generate_html_report(session_id: str, template_env: Environment) -> Path:
    spider_chart = await generate_spider_chart_for(session_id)
    bar_chart = await generate_bar_chart_for(session_id)
    qa_scored = await select_session_qa(session_id)
    questionnaire_html = generate_qa_scored(qa_scored)
    report_date_str = generate_report_date()
    ml_context = await create_maturity_level_report_context(session_id)
    context = {
        "spider_chart": spider_chart.as_posix(),
        "bar_chart": bar_chart.as_posix(),
        "questionnaire": questionnaire_html,
        "timestamp": report_date_str,
        **ml_context,
    }
    template = template_env.get_template("results-template.html")
    results_template = await template.render_async(context)
    report_path: Path = cfg.report_tmp_path / f"{session_id}.html"
    report_path.write_text(results_template, encoding="utf-8")
    return report_path


async def generate_pdf_report(session_id: str) -> Path:
    template_loader = FileSystemLoader(cfg.templates_folder)
    template_env = Environment(loader=template_loader, enable_async=True)

    report_path: Path = await generate_html_report(session_id, template_env)
    pdf_file: Path = cfg.pdf_generation_folder / f"{session_id}.pdf"
    config = pdfkit.configuration(wkhtmltopdf=cfg.wkhtmltopdf_binary.as_posix())
    footer_file = await generate_footer_file(template_env, session_id)
    header_file = cfg.templates_folder / "header.html"
    pdfkit_options = {
        "enable-local-file-access": "",
        "footer-html": footer_file.as_posix(),
        "footer-left": "[page]",
        "header-html": header_file.as_posix(),
        "footer-font-size": "7",
    }
    pdfkit.from_string(
        report_path.read_text(encoding="utf-8"),
        pdf_file,
        configuration=config,
        options=pdfkit_options,
    )
    return pdf_file


async def generate_footer_file(template_env: Environment, session_id: str) -> Path:
    footer_date = generate_footer_date()
    template = template_env.get_template("footer.html")
    context = {"date": footer_date}
    results_template = await template.render_async(context)
    for img in cfg.templates_folder.glob("*.png"):
        shutil.copyfile(img, cfg.report_tmp_path / img.name)
    footer_path: Path = cfg.report_tmp_path / f"{session_id}_footer.html"
    footer_path.write_text(results_template)
    return footer_path


def generate_qa_scored(qa_scored: List[QAScored]) -> str:
    html = ""
    previous_topic = ""
    topic_scores = defaultdict(int)

    def print_score_func(topic_score):
        return f"""
<tr ckass="total-row">
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
<tr ckass="topic-row">
    <td colspan="2">{topic}</td>
</tr>
<tr ckass="question-row">
    <td>
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

    session_id = "da437e34-e64f-45a6-9042-36808d8fc8ea"

    target_file = asyncio.run(generate_pdf_report(session_id))
    print(target_file)
