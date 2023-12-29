from typing import Tuple


def ranking_prompt_provider() -> Tuple[str, str, str]:
    topic = "Business alignment"
    question_answers = """
Is there a published business strategy that data strategy needs to align to?

Yes, we have a very detailed published business strategy.
"""
    ranking_questions = """
Does your current data strategy align with your business strategy? Are there gaps or misalignments to address?
Is there market demand for the type of data your organization possess?
Are there any known GenAI use cases or would the orgranization be interested in knowing how data strategy can be enabler for GenAI?
Are you aware of the potential business impact of analyzing and using currently untapped data sources?
Is there data governance that aligns and support business objectives?
Do you have executive support for data initiatives?
Is there budget allocated for data infrastructure needs?
Have you explored various monetization models (e.g., data licensing, data subscriptions, data-as-a-service)?
Is there a need or opportunity to simplify data sharing and collaboration amoungst internal teams?
Is there a need to democratize data access and empower business units or teams to access and analyze data independently?
Are there emerging use cases that require agility in data access and processing?
Are there bottlenecks in data access, processing, or analytics?
How long does it take for a medium size complexity analytical project to from requirements to production? Are there any concerns about the time it takes to go live? 
Does your organization have the necessary skills in-house, or do you rely on external expertise?
"""
    return topic, question_answers, ranking_questions


def topics_ranking_prompt_provider() -> Tuple[str, str]:
    question_answers = """What best describes the reality of your organization's advanced analytics tools landscape?
Our advanced analytics tools landscape includes a data lake based on Snowflake which hosts the data used by our Power BI reports. We are currently not using any advanced features of Power BI related to machine learning. Power BI is in this context only a visualization instrument.
"""
    ranking_topics_str = """
Business Alignment
Data Acquisition
Data Architecture
Data Assets
Data Governance
Data Modelling
Data Privacy
Data Quality
Data Security
Dataops
"""
    return question_answers, ranking_topics_str
