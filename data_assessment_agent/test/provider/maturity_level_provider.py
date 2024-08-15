from data_assessment_agent.config.config import cfg


def provide_session_report() -> str:
    dummy_session_output = cfg.project_root / "docs/session_output.txt"
    assert dummy_session_output.exists, f"Cannot find file {dummy_session_output}"
    return dummy_session_output.read_text(encoding="utf-8")
