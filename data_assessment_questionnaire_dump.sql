--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: tb_configuration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_configuration (
    id integer NOT NULL,
    config_key character varying(36) NOT NULL,
    config_value character varying(256) NOT NULL
);


ALTER TABLE public.tb_configuration OWNER TO postgres;

--
-- Name: tb_configuration_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_configuration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_configuration_id_seq OWNER TO postgres;

--
-- Name: tb_configuration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_configuration_id_seq OWNED BY public.tb_configuration.id;


--
-- Name: tb_question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_question (
    id integer NOT NULL,
    question character varying(1024) NOT NULL,
    score integer NOT NULL,
    topic_id integer NOT NULL,
    preferred_question_order integer,
    yes_no_question boolean,
    scored boolean
);


ALTER TABLE public.tb_question OWNER TO postgres;

--
-- Name: tb_question_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_question_id_seq OWNER TO postgres;

--
-- Name: tb_question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_question_id_seq OWNED BY public.tb_question.id;


--
-- Name: tb_question_score; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_question_score (
    id integer NOT NULL,
    question_id integer NOT NULL,
    affirmative_score integer,
    undecided_score integer,
    negative_score integer
);


ALTER TABLE public.tb_question_score OWNER TO postgres;

--
-- Name: tb_question_score_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_question_score_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_question_score_id_seq OWNER TO postgres;

--
-- Name: tb_question_score_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_question_score_id_seq OWNED BY public.tb_question_score.id;


--
-- Name: tb_questionnaire_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_questionnaire_status (
    id integer NOT NULL,
    session_id character varying(36) NOT NULL,
    topic character varying(256) NOT NULL,
    question character varying(1024) NOT NULL,
    answer character varying(4096),
    score integer,
    sentiment_id integer,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.tb_questionnaire_status OWNER TO postgres;

--
-- Name: tb_questionnaire_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_questionnaire_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_questionnaire_status_id_seq OWNER TO postgres;

--
-- Name: tb_questionnaire_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_questionnaire_status_id_seq OWNED BY public.tb_questionnaire_status.id;


--
-- Name: tb_quiz_mode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_quiz_mode (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    question_count integer NOT NULL
);


ALTER TABLE public.tb_quiz_mode OWNER TO postgres;

--
-- Name: tb_quiz_mode_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_quiz_mode_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_quiz_mode_id_seq OWNER TO postgres;

--
-- Name: tb_quiz_mode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_quiz_mode_id_seq OWNED BY public.tb_quiz_mode.id;


--
-- Name: tb_selected_quiz_mode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_selected_quiz_mode (
    id integer NOT NULL,
    session_id character varying(36) NOT NULL,
    quiz_mode_id integer NOT NULL
);


ALTER TABLE public.tb_selected_quiz_mode OWNER TO postgres;

--
-- Name: tb_selected_quiz_mode_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_selected_quiz_mode_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_selected_quiz_mode_id_seq OWNER TO postgres;

--
-- Name: tb_selected_quiz_mode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_selected_quiz_mode_id_seq OWNED BY public.tb_selected_quiz_mode.id;


--
-- Name: tb_selected_topics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_selected_topics (
    id integer NOT NULL,
    session_id character varying(36) NOT NULL,
    topic_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.tb_selected_topics OWNER TO postgres;

--
-- Name: tb_selected_topics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_selected_topics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_selected_topics_id_seq OWNER TO postgres;

--
-- Name: tb_selected_topics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_selected_topics_id_seq OWNED BY public.tb_selected_topics.id;


--
-- Name: tb_sentiment_score; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_sentiment_score (
    id integer NOT NULL,
    name character varying(15) NOT NULL
);


ALTER TABLE public.tb_sentiment_score OWNER TO postgres;

--
-- Name: tb_suggested_response; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_suggested_response (
    id integer NOT NULL,
    title character varying(256) NOT NULL,
    subtitle character varying(256),
    body character varying(1024) NOT NULL,
    question_id integer NOT NULL,
    score integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.tb_suggested_response OWNER TO postgres;

--
-- Name: tb_suggested_response_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_suggested_response_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_suggested_response_id_seq OWNER TO postgres;

--
-- Name: tb_suggested_response_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_suggested_response_id_seq OWNED BY public.tb_suggested_response.id;


--
-- Name: tb_topic; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_topic (
    id integer NOT NULL,
    name character varying(256) NOT NULL,
    description character varying(4096),
    question_amount integer NOT NULL,
    preferred_topic_order integer
);


ALTER TABLE public.tb_topic OWNER TO postgres;

--
-- Name: tb_topic_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tb_topic_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tb_topic_id_seq OWNER TO postgres;

--
-- Name: tb_topic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tb_topic_id_seq OWNED BY public.tb_topic.id;


--
-- Name: vw_question_scores; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vw_question_scores AS
 SELECT
        CASE
            WHEN (q.yes_no_question = true) THEN
            CASE
                WHEN (strpos('positive'::text, (ss.name)::text) > 0) THEN ( SELECT qs.affirmative_score
                   FROM public.tb_question_score qs
                  WHERE (qs.question_id = q.id))
                WHEN (strpos('negative'::text, (ss.name)::text) > 0) THEN ( SELECT qs.negative_score
                   FROM public.tb_question_score qs
                  WHERE (qs.question_id = q.id))
                WHEN ((ss.name)::text = 'ambiguous'::text) THEN ( SELECT qs.undecided_score
                   FROM public.tb_question_score qs
                  WHERE (qs.question_id = q.id))
                ELSE 0
            END
            ELSE s.score
        END AS score,
    ( SELECT GREATEST(qs.affirmative_score, qs.undecided_score, qs.negative_score) AS "greatest"
           FROM public.tb_question_score qs
          WHERE (qs.question_id = q.id)) AS max_score,
    ss.name AS sentiment_name,
    s.sentiment_id,
    t.name AS topic_name,
    s.session_id,
    q.question,
    s.answer,
    s.created_at,
    s.updated_at
   FROM (((public.tb_questionnaire_status s
     JOIN public.tb_sentiment_score ss ON ((ss.id = s.sentiment_id)))
     JOIN public.tb_question q ON (((q.question)::text = (s.question)::text)))
     FULL JOIN public.tb_topic t ON (((t.id = q.topic_id) AND ((t.name)::text = (s.topic)::text))))
  WHERE (q.scored = true);


ALTER VIEW public.vw_question_scores OWNER TO postgres;

--
-- Name: tb_configuration id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_configuration ALTER COLUMN id SET DEFAULT nextval('public.tb_configuration_id_seq'::regclass);


--
-- Name: tb_question id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_question ALTER COLUMN id SET DEFAULT nextval('public.tb_question_id_seq'::regclass);


--
-- Name: tb_question_score id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_question_score ALTER COLUMN id SET DEFAULT nextval('public.tb_question_score_id_seq'::regclass);


--
-- Name: tb_questionnaire_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_questionnaire_status ALTER COLUMN id SET DEFAULT nextval('public.tb_questionnaire_status_id_seq'::regclass);


--
-- Name: tb_quiz_mode id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_quiz_mode ALTER COLUMN id SET DEFAULT nextval('public.tb_quiz_mode_id_seq'::regclass);


--
-- Name: tb_selected_quiz_mode id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_selected_quiz_mode ALTER COLUMN id SET DEFAULT nextval('public.tb_selected_quiz_mode_id_seq'::regclass);


--
-- Name: tb_selected_topics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_selected_topics ALTER COLUMN id SET DEFAULT nextval('public.tb_selected_topics_id_seq'::regclass);


--
-- Name: tb_suggested_response id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_suggested_response ALTER COLUMN id SET DEFAULT nextval('public.tb_suggested_response_id_seq'::regclass);


--
-- Name: tb_topic id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_topic ALTER COLUMN id SET DEFAULT nextval('public.tb_topic_id_seq'::regclass);


--
-- Data for Name: tb_configuration; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_configuration (id, config_key, config_value) FROM stdin;
1	minimum topics	3
\.


--
-- Data for Name: tb_question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_question (id, question, score, topic_id, preferred_question_order, yes_no_question, scored) FROM stdin;
389	Is there a published business strategy that data strategy needs to align to?	15	16	3	t	t
392	What are the primary use cases for data within your organization (e.g., reporting, analytics, machine learning)?	15	16	6	f	f
391	Is there market demand for the type of data your organization possesses?	15	16	5	t	f
394	Are you aware of the potential business impact of analyzing and using currently untapped data sources?	15	16	8	t	f
400	Are there cost optimization opportunities?	15	16	14	t	f
395	Is there data governance that aligns and support business objectives?	15	16	9	t	t
396	Do you have executive support for data initiatives?	15	16	10	t	t
397	Is there budget allocated for data infrastructure needs?	15	16	11	t	t
398	What is the budget allocated for data infrastructure needs?	15	16	12	f	t
399	What is the current cost of data storage and management?	15	16	13	f	t
403	What are your future data needs and growth projections?	15	16	17	f	f
401	What is your budget for data-related initiatives for the coming year?	15	16	15	f	t
402	Have you explored various monetization models (e.g., data licensing, data subscriptions, data-as-a-service)?	15	16	16	t	t
406	Is there a need or opportunity to simplify data sharing and collaboration amoungst internal teams?	15	16	20	t	f
404	Are there pain points or challenges related to data that stakeholders have identified?	15	16	18	t	t
405	How do different business/product teams or departments collaborate on data initiatives?	15	16	19	f	t
409	Is there a need to democratize data access and empower business units or teams to access and analyze data independently?	15	16	23	t	f
407	What measures are in place to ensure business continuity in the event of disasters? What tier is data lake and reporting classified as?	15	16	21	f	t
408	How is data ownership and responsibility currently structured within the organization? How many data owners do we have?	15	16	22	f	t
410	Are there ethical considerations related to data usage and sharing in your industry?	15	16	24	t	f
411	Are there emerging use cases that require agility in data access and processing?	15	16	25	t	f
412	Can you identify specific pain points or challenges in implementation of analytics use cases? 	15	16	26	f	f
416	Are there competitors or data providers offering similar data products or services?	15	16	30	t	f
413	Are there bottlenecks in data access, processing, or analytics?	15	16	27	t	t
414	Is your organization open to realigning data teams based on how data is consumed?	15	16	28	t	t
415	Have you conducted market research or received inquiries from potential data buyers?	15	16	29	t	t
417	What differentiates your data from your competitors?	15	16	31	f	f
419	What are the new analytical initiatives that may have been planned or communicated? 	15	16	33	f	f
418	How can your data address specific business or industry needs?	15	16	32	f	t
420	What other business use cases/capabilities are in the pipeline to be implemented?	15	16	34	f	f
421	Are you aware of any initiatives that require to ingest social media data or CCTV data?	15	16	35	t	f
365	What best describes the reality of your organization's advanced analytics tools landscape?	15	15	0	f	f
422	Are there any plan to make analytics data highly available 24x7 to external partners to monetize data?	15	16	36	t	f
366	What type of capability do you have currently for supporting analytics (example: SAS, Python, Pyspark, R, notebook, text analytics, elastic search etc )?	15	15	1	f	f
367	What is the strength and composition of the analytics team?	15	15	2	f	f
390	Does your current data strategy align with your business strategy?	15	16	4	t	t
368	What programming language is available to be used by the analysts?	15	15	3	f	f
369	What IDE, notebooks are used by the analysts?	15	15	4	f	f
370	What analytical capability or algorithms are being used?	15	15	5	f	f
371	What machine learning frameworks such as PyTorch, NumPy etc are used currently?	15	15	6	f	f
372	Do you provide self-service capability to analytical users in production environment, and how it is currently managed?	15	15	7	f	t
374	What techniques/frameworks/toolkits/libraries are used or are in place to make the LLM models interpretable and explainable?	15	15	9	f	f
381	What machine learning model evaluation frameworks and libraries do you use for assessing the performance of ML models?	15	15	16	f	f
375	Do you version the models?	15	15	10	t	t
376	Are data scientists able to collborate and easily share ML models?	15	15	11	t	t
377	Do you expose your model through APIs?	15	15	12	t	t
378	Do you serialize the model, including its architecture and weights, into a single binary file or format for interoperability? 	15	15	13	t	t
379	Have you considered training your models using federated learning for data privacy or for edge computing?	15	15	14	t	t
380	Do you use AutoML to automate model selection and hyperparameter tuning?	15	15	15	t	t
383	What metric evaluation framework do you use to evaluate the performance of the models?	15	15	18	f	f
382	Does your organization support interoperability of ML models?	15	15	17	t	t
384	Are there any use cases for Analytics as a Service or use cases to support self service by business?	15	15	19	t	t
385	Has the team explored the use of a data science platform?	15	15	20	t	t
387	What are the organization's short-term and long-term business goals?	15	16	1	f	f
388	How does data or data strategy support these goals?	15	16	2	f	f
426	Does your organization have the necessary skills in-house, or do you rely on external expertise?	15	16	40	t	t
427	Are there skill gaps that need to be addressed?	15	16	41	t	t
428	Is there a mandatory data training for all new comers/employess, and contractors?	15	16	42	t	t
436	Are there data ingestion pipelines for bringing the data in data lake in place? How many such data pipelines exist?	15	17	3	f	f
430	Are there ongoing data exploration and analytics efforts to uncover insights from dark data?	15	16	44	t	t
431	Are there any known use cases that the data strategy is going to drive for implementation?	15	16	45	t	t
432	Are there any specific data-driven initiatives in progress or planned?	15	16	46	t	t
433	How is data shared with external partners outside the organization?	15	17	0	f	t
434	How is data ingested into the data lake?	15	17	1	f	t
435	Is the data lake leveraged as real time data hub?	15	17	2	t	t
441	What data pipelines exist within your organization?	15	17	8	f	f
437	Is data streaming, or pushed as batch data in flat file or pulled from database or consumed from systems using API?	15	17	4	f	t
438	How are different data sources integrated with the data lake?	15	17	5	f	t
439	Are there data integration challenges or bottlenecks?	15	17	6	t	t
440	How frequently is data integrated? What is the data latency for majority of the data pipelines?	15	17	7	f	t
443	What tools and technologies are used for data transformation and processing?	15	17	10	f	f
442	How are data pipelines documented and cataloged?	15	17	9	f	t
451	How are different versions of data assets managed?	15	17	18	f	f
444	How are data transformations managed and versioned?	15	17	11	f	t
445	How do you orchestrate and schedule data workflows and tasks?	15	17	12	f	t
446	Are there tools or platforms used for orchestration?	15	17	13	f	t
447	How do you monitor data pipelines for issues or anomalies?	15	17	14	f	t
448	Are there alerting mechanisms in place for data pipeline failures?	15	17	15	t	t
449	Do you track and document data lineage?	15	17	16	t	t
450	Is data lineage exported from the data pipelines in to the data catalog?	15	17	17	t	t
453	How do you optimize the performance and cost of data pipelines?	15	17	20	f	f
452	Do you have data recovery strategies in place?	15	17	19	t	t
457	How do you track pipeline efficiency and reliability?	15	17	24	f	f
454	Are there processes for continuous improvement?	15	17	21	t	t
455	Is there documentation of data pipelines, workflows, and best practices?	15	17	22	t	t
459	Do you need to handle real-time or near-real-time data?	15	17	26	t	f
458	How complex are the data transformations and computations?	15	17	25	f	t
465	What tools and technologies are used for data analysis?	15	18	3	f	f
460	Does data arrive in real-time or batch processes?	15	17	27	f	t
461	What file formats are supported on the data lake?	15	17	28	f	t
462	How is data accessed (dashboards, reports, APIs, etc.)?	15	18	0	f	t
463	Are there data access restrictions or security measures in place?	15	18	1	t	t
464	How is data used for analytics and reporting?	15	18	2	f	t
468	What are the potential use cases for your data (e.g., market research, predictive analytics, targeted advertising)?	15	18	6	f	f
466	Are there data analytics skills and resources within the organization?	15	18	4	t	t
469	Is there a MDM tool used for master data?	15	18	7	f	t
473	Are there any known challenges with data silos or centralization?	15	18	11	t	t
470	Does the organization support use of open source products?	15	18	8	t	t
471	Is there a design document for the data lake?	15	18	9	t	t
472	Are there gaps or opportunities for improvement in your technology stack?	15	18	10	t	t
475	Do you have specific pain points or challenges in your current data ecosystem?	15	18	13	f	t
474	How do different teams or departments collaborate on data initiatives?	15	18	12	f	t
477	Is there an existing published data strategy?	15	18	15	f	t
476	Have you reviewed the core principles of data mesh, such as domain-oriented ownership, product thinking, and self-serve data infrastructure?	15	18	14	t	t
479	Do the principles of data mesh align with your organization's goals and culture?	15	18	17	t	t
478	How do you plan to adapt your data strategy to meet evolving requirements such as Gen AI use cases?	15	18	16	f	t
480	Are you open to conducting a data mesh pilot or proof of concept to evaluate its feasibility and benefits within your organization?	15	18	18	t	t
481	Are you aware of any initiatives that require to ingest unstructured or semi structured data? 	15	18	19	t	t
483	What is the composition of your data team (data engineers, data scientists, analysts)?	15	18	21	f	f
482	Is the data science platform or analytical platform vendor supported or open-source?	15	18	20	t	t
429	Are there strategic initiatives that could benefit from accessing dark data?	15	16	43	t	t
484	What is the potential business impact of analyzing and using currently untapped data sources?	15	18	22	f	t
425	What percentage of advanced analytics projects have been operationalized (i.e., actually integrated into business processes)?	15	16	39	f	t
456	Are the tools used for DevOps/DataOps effectively meeting your needs?	15	17	23	t	t
489	What is data partitioning strategy?	15	18	27	f	f
491	How does your company acquire data and ensure data quality?	15	19	0	f	f
490	Is there any terminology server to centralize storage of reference data sets?	15	18	28	t	t
492	What types of data does the organization collect and store?	15	19	1	f	f
493	Where is the data located (databases, data warehouses, cloud platforms, etc.)?	15	19	2	f	f
494	What are the types and sources of data that your organization deals with (e.g., structured, semi-structured, unstructured)?	15	19	3	f	f
495	What are the different types of data persistance stores within the organization such as RDBMS, No SQL databases, Graph databases and so on?	15	19	4	f	f
496	What NoSql Databases are used?	15	19	5	f	f
497	What Graph databases have been used or explored so far?	15	19	6	f	f
498	What are the data sources corresponding to the data domains?	15	19	7	f	f
499	What is the approximate total volume of data on the data lake?	15	19	8	f	f
500	What sources generate or contribute to your data (e.g., IoT devices, applications, websites, manual entry)?	15	19	9	f	f
501	What external data sources are leveraged for insights or decision-making?	15	19	10	f	f
502	How do you ensure the quality and reliability of external data?	15	19	11	f	f
505	Are there cost optimization opportunities for data storage?	15	19	14	t	f
503	Do you have an inventory of all data assets, including their location and sensitivity?	15	19	12	t	t
504	Have data assets been classified based on their importance and sensitivity?	15	19	13	t	t
507	How does dark data fit into your overall data governance framework and data strategy?	15	19	16	f	f
506	Do you have tools or teams dedicated to analyzing dark data?	15	19	15	t	t
509	Where is reference data stored and how is it accessed within the data lake?	15	19	18	f	f
508	Are there plans to bring dark data into alignment with organizational goals?	15	19	17	t	t
510	How is reference data managed?	15	19	19	f	f
520	Who are the key stakeholders involved in data governance decision-making and implementation?	15	20	1	f	f
511	Are there duplicate copies of ungoverned data in the organization?	15	19	20	t	t
512	Is there a data catalog in place?	15	19	21	t	t
514	What data sources is the data catalog integrated with?	15	19	23	f	t
515	Does the data catalog support dynamic or auto discovery of data assets?	15	19	24	t	t
516	How frequently is the data catalog refreshed to reflect changes in the schema of the backend data sources?	15	19	25	f	t
517	Does the data catalog govern NoSQL and event driven messages or schema?	15	19	26	t	t
518	Does the data catalog support tagging data attributes as PII or senstive data fields?	15	19	27	t	t
519	Is there an established data governance program or framework in place? Is there a published data governance charter?	15	20	0	t	t
523	How many data owners, stewards or custodians are assigned to each data domain?	15	20	4	f	f
521	Is there CxO level sponsorship for the data governance program?	15	20	2	t	t
522	Are data domain, data ownership and stewardship roles defined and communicated in the charter?	15	20	3	t	t
524	Who is responsible for data governance within the organization? Is there a central team or is data governance federated?	15	20	5	f	f
528	How are data governance principles and practices communicated and promoted?	15	20	9	f	f
525	What is the level of awareness and understanding of data governance among employees? Is there a a training program to create awareness?	15	20	6	t	t
526	Is there a clear alignment of business data owners within the line of business responsible for data assets within the organization?	15	20	7	t	t
527	Is there a culture of data governance and data stewardship within the organization?	15	20	8	t	t
530	What were the findings, and how have they been addressed?	15	20	11	f	f
529	Have there been any external audits or assessments of your data governance practices?	15	20	10	t	t
531	How do you engage with and involve business units and IT in data governance?	15	20	12	f	f
532	What are the major challenges and pain points related to data governance?	15	20	13	f	f
535	What tools and technology are used for data governance (e.g., data catalog, data lineage)?	15	20	16	f	f
533	Are there specific areas where improvement is needed?	15	20	14	t	t
534	Is there comprehensive documentation of data governance policies, procedures, and standards?	15	20	15	t	t
536	Are the tools used for data governance (data catalog, data lineage tool) effective in supporting data governance efforts?	15	20	17	t	t
537	What processes are in place for data governance, including data capture, validation, and reporting?	15	20	18	f	f
539	How do you measure the effectiveness of your data governance efforts?	15	20	20	f	f
538	Are data governance workflows documented and followed?	15	20	19	t	t
540	What key performance indicators (KPIs) are used to assess data quality and governance success?	15	20	21	f	f
544	What are the prioritized initiatives and goals for enhancing data governance?	15	20	25	f	f
541	Is there ongoing data governance education and awareness programs?	15	20	22	t	t
542	Are employees provided with yearly mandatory training on data governance best practices?	15	20	23	t	t
543	Do you have a data governance roadmap or plan for future improvements?	15	20	24	t	t
545	Do you have processes for managing data from external sources or partners?	15	20	26	t	t
488	What is the data lake folder hierarchy?	15	18	26	f	f
486	Are there ongoing data exploration and analytics efforts to uncover insights from dark data?	15	18	24	t	t
487	How many data zones are there in the data lake?	15	18	25	f	t
550	Do you have a process and tool to manage master data?	15	20	31	t	t
552	How do the data modellers collaborate and share the data models?	15	21	1	f	f
553	What the key data domains and how are the data modellers aligned to the domains?	15	21	2	f	f
557	How are the data models published?	15	21	6	f	f
555	Is there a naming convention that is enforced?	15	21	4	t	t
556	Is there a data dictionary for the data models?	15	21	5	t	t
559	Do the data modellers model only relationship data to be stored in databases or do they model for NoSQL databases as well?	15	21	8	f	t
558	Are there sufficient read licenses for viewers to view the data models?	15	21	7	t	t
573	How is data quality measured and monitored?	15	23	0	f	f
560	Is graph data modelling relevant to the organization? Do the data modellers have adequete training to model knowledge graphs if relevant to the organization?	15	21	9	t	t
561	Do the data modellers use data vault or explored the use of data vault? Are they trained to model data using data vault?	15	21	10	t	t
562	Are the data modellers trained to identify PII data attributes in the data models?	15	21	11	t	t
563	Do the data modellers use a tool to generate the physical data models or generate DML?	15	21	12	t	t
564	Do data modellers model messages/events that are to be published on an event stream such as Kafka?	15	21	13	t	t
577	Who are the key stakeholders responsible for data quality?	15	23	4	f	f
574	Are there data validation and cleansing processes?	15	23	1	t	t
575	Is there an Audit, Balance & Control Framework that the organisation has built or adopted?	15	23	2	t	t
576	Are data quality standards and guidelines defined and enforced?	15	23	3	t	t
584	How are data anomalies and discrepancies identified and corrected?	15	23	11	f	f
578	Have you conducted data profiling exercises to understand the characteristics of your data?	15	23	5	t	t
579	Are you using any tools or methods for data profiling?	15	23	6	t	t
580	Are there any quality metrics or Key Performance Metrics (KPIs) in place?	15	23	7	t	t
581	Do you use any methods for measuring accuracy, completeness, consistency and timeliness?	15	23	8	t	t
582	Have you established data quality standards and guidelines?	15	23	9	t	t
583	Do you have data validation processes in place to catch errors at the point of entry?	15	23	10	t	t
586	Are the tools used for anomaly detection and data quality monitoring effective in addressing data quality issues?	15	23	13	t	t
585	What tools and technologies are used for data quality monitoring and improvement?	15	23	12	f	f
587	What is the process for conducting data quality assessments?	15	23	14	f	f
589	Who is responsible for data quality within the organization?	15	23	16	f	f
588	How frequently are data quality assessments performed?	15	23	15	f	t
591	How do you validate data accuracy and completeness?	15	23	18	f	f
590	Are data quality responsibilities clearly defined?	15	23	17	t	t
593	How do you clean and enrich data to improve quality?	15	23	20	f	f
592	Are there automated tests or manual checks in place?	15	23	19	t	t
594	What processes are used to standardize and normalize data?	15	23	21	f	f
596	How do you detect and respond to data quality issues as they arise?	15	23	23	f	f
595	Do you have real-time or batch data quality monitoring in place?	15	23	22	t	t
598	What were the outcomes of these initiatives?	15	23	25	f	f
597	Have you implemented specific initiatives to address data quality challenges?	15	23	24	t	t
601	What are the major challenges and pain points related to data quality?	15	23	28	f	f
599	Is data quality information communicated to stakeholders?	15	23	26	t	t
600	Do you have data quality dashboards or reports?	15	23	27	t	t
603	How comprehensive and high-quality is your data?	15	23	30	f	f
602	Are there specific areas where data quality improvement is needed?	15	23	29	t	t
605	What data quality issues have been identified, and how are they addressed?	15	23	32	f	f
604	Are there critical data quality issues that need to be addressed?	15	23	31	t	t
606	How do you ensure data quality and compliance when integrating external data?	15	23	33	f	f
607	How do you ensure data quality and governance to maintain the value of your data assets?	15	23	34	f	f
572	Did you implement right to forget as part of GDPR compliance?	15	22	7	t	t
567	How do you handle customer and employee data privacy? What tools or technology is used?	15	22	2	f	f
569	What are the most common tokens used?	15	22	4	f	f
568	Do you use any tokenization tools to tokenize PII data fields?	15	22	3	t	t
570	How and where consent by the customer to share data captured and stored? 	15	22	5	f	f
571	Is consent across multiple LOBs stored in a central repository and exposed as API?	15	22	6	t	t
610	How do you handle sensitive data?	15	24	2	f	f
608	Are there specific industry regulations or legal requirements that impact your data strategy?	15	24	0	t	t
609	Are you compliant with relevant data regulations such as GDPR?	15	24	1	t	t
611	What measures are in place to protect data from security breaches?	15	24	3	f	f
612	Do you have a disaster recovery plan for data?	15	24	4	t	t
613	Are data access permissions aligned with business needs and regulations?	15	24	5	t	t
548	How is data backed up and archived and deleted when it reaches the end of its lifecycle?	15	20	29	f	f
551	What tool is used by the data modellers?	15	21	0	f	f
549	Are there data disposal procedures in place?	15	20	30	t	t
617	Do you use a keystore to manage the keys?	15	24	9	t	t
618	Do you use your own keystore for managing keys stored on the cloud?	15	24	10	t	t
620	Can you tap into industry data ecosystems or consortiums?	15	24	12	t	t
621	Do you have a well defined Role Based access control policy in place with roles aligned to AD groups?	15	24	13	t	t
622	Is there a well defined process to add users to the AD groups?	15	24	14	t	t
623	Are there any policies that use attribute based access control for row based filtering?	15	24	15	t	t
624	Are you using any audit compliance tools, like e.g. Splunk, Guardium?	15	24	16	t	t
626	What is the process to identify if data is PII, PHI, and PCI according to the compliance?	15	24	18	f	f
629	Are you aware of any legal challenges that would prohibit sharing data internally among the lines of business?	15	24	21	t	f
627	What process and tools are used for bringing prod data in to lower environment after psuedo anonymization of the data?	15	24	19	f	f
628	Do you have process defined and tools identified for generating synthetic data?	15	24	20	t	t
630	Who performs security code reviews to identify and address vulnerabilities in the model's code and dependencies?	15	24	22	f	f
632	What practises do you use for securing ML models?	15	24	24	f	f
631	Do you secure the transfer of model weights and configurations between training environments, deployment environments, and remote clients?	15	24	23	t	t
633	How do you encrypt ML models? 	15	24	25	f	f
637	How do you handle sensitive data and ensure ethical data practices?	15	24	29	f	f
634	Do you encrypt the model weights and parameters?	15	24	26	t	t
635	Do you implement regular key rotation procedures to minimize the risk associated with long-lived encryption keys?	15	24	27	t	t
638	Can you define what does DevOps/DataOps pipeline look like?	15	25	0	f	f
640	How do teams collaborate on DevOps/DataOps tasks and projects?	15	25	2	f	f
639	Are there dedicated DataOps teams or roles within the organization?	15	25	1	t	t
641	What tools and technologies are used for DevOps/DataOps automation?	15	25	3	f	f
642	How are DevOps/DataOps principles and practices communicated and promoted?	15	25	4	f	f
643	What are the major challenges and pain points related to DevOps/DataOps?	15	25	5	f	f
645	What are your future plans and initiatives for enhancing DevOps/DataOps capabilities?	15	25	7	f	f
644	Are there specific areas where improvement is needed?	15	25	6	t	t
647	What metrics and Key Performance Indicators (KPIs) are used to measure DevOps/DataOps success?	15	25	9	f	f
646	Do you have a roadmap for DevOps/DataOps improvements?	15	25	8	t	t
648	Are the tools used for DevOps/DataOps effectively meeting your needs?	15	25	10	t	t
649	What are the current known pain points that you are aware that you would like to see it addressed?	15	25	11	f	f
651	How are data pipelines deployed to production?	15	25	13	f	f
653	What is the process for rolling back data changes in case of issues?	15	25	15	f	f
652	Do you have processes for promoting changes from development to production?	15	25	14	t	t
654	Is there a culture of collaboration and automation within the DevOps/DataOps teams?	15	25	16	t	t
655	Is your data lake on-prem or on cloud? If data lake is on-prem do you use open source or Cloudera? If on cloud, which Cloud Service Provider (CSP) do you use?	15	26	0	f	f
656	Are you considering a cloud-based data infrastructure, on-premises solutions, or a hybrid approach for your analytics needs?	15	26	1	f	f
658	If on-prem, what is the footprint of the infrastructure? What applications are on those on-prem servers? 	15	26	3	f	f
657	Does your organization have a comprehensive cloud infrastructure strategy to support workloads federated over on-premise and multiple cloud service providers?	15	26	2	t	t
662	What technologies and platforms are used for data storage and management?	15	26	7	f	f
659	Is there a private cloud or plans to introduce a private cloud?	15	26	4	t	t
660	Is your data infrastructure scalable to handle growing data volumes?	15	26	5	t	t
661	 Does your organization support a cost-effective strategy of utilizing serverless computing?	15	26	6	t	t
665	What are the latency requirements for data access?	15	26	10	f	f
663	Is there an object storage server on-prem?	15	26	8	t	t
664	Are there any known performance bottlenecks?	15	26	9	t	t
666	What is the latency between clouds if your organization is using multi-cloud strategy and have transactional workloads and analytical workloads on separate clouds?	15	26	11	f	f
667	How do you anticipate data volumes and processing needs will grow over time? Does your organization have a strategy to scale your existing infrastructure for AI/ML workloads?	15	26	12	f	f
670	How do you ensure data resilience and availability?	15	26	15	f	f
668	Is your data infrastructure designed to scale horizontally or vertically?	15	26	13	f	t
669	Do you have backup and disaster recovery strategies in place for your data infrastructure?	15	26	14	t	t
650	Are there any specific topics that you would like to discuss or topics to be addressed as part of the assessment?	15	25	12	f	f
671	Do you deploy ML models in containers (e.g., Docker)? 	15	26	16	t	t
672	Do you use any GPU clusters or FPGA's or any specialized hardware for analytics?	15	26	17	t	t
615	Who has access to what data, and how is access controlled and audited?	15	24	7	f	f
616	How is data security and compliance ensured throughout the data lifecycle?	15	24	8	f	f
625	What compliance laws or frameworks such as GDPR, CCPA, NIST, HIPAA, FISMA, SOX, PCI, FIPS are relevant to the organization and that the organization needs to adhere to?	15	24	17	f	f
677	How are data retention policies enforced for data stored? 	15	26	22	f	f
680	Who does the FinOps for data?	15	26	25	f	f
678	Are all data assets including on-prem and cloud integrated with CMDB or Software Asset Management tool?	15	26	23	t	t
679	How are costs associated with data assets or analytics on the cloud tracked, analyzed and optimized? Is tagging policy used?	15	26	24	t	t
682	What is the reaction time when a request is made to increase the infrastructure capacity?	15	26	27	f	f
681	How frequest is the infrastucture footprint analyzed and capacity added?	15	26	26	f	t
685	If there are multiple tools, is there a plan to rationalize reporting tools?	15	27	0	f	t
683	Do you have the necessary technology infrastructure to support data monetization efforts (e.g., data platforms, data marketplaces)?	15	26	28	t	t
684	Do lot of analytical projects frequently need to add infrastructure?	15	26	29	t	t
687	Who are the consumers of the reports? Do you have any external users for the reports?	15	27	2	f	f
686	Is there a semantic layer defined within the reporting tool?	15	27	1	t	t
688	Are these reports operational in nature or do they use historical data?	15	27	3	f	f
690	How many scheduled reports are currently generated?	15	27	5	f	f
689	Are there any SLAs for the reports?	15	27	4	t	t
692	How are reports deployed or accessed by the users?	15	27	7	f	f
691	Do the scheduled reports have any visualization embdeeded or is it all tabular data?	15	27	6	t	t
693	What is the largest size in MB for the report? How many pages does it have?	15	27	8	f	f
694	How many dashboards are deployed in production for data driven insights?	15	27	9	f	f
697	Is there a plan to consolidate reporting?	15	27	12	f	t
695	Does business prefer dashboards over scheduled reports?	15	27	10	t	t
696	Are there any reports that are outsourced to any 3rd parties? Is there desire to bring that reporting in-house?	15	27	11	f	f
698	What are the data sources for the reports?	15	27	13	f	f
701	Is there a DR environment for the reporting server?	15	27	16	t	t
700	Is the reporting server on-prem or on cloud?	15	27	15	f	t
702	What is the archival policy for reports?	15	27	17	f	f
707	Does business have the ability to create reports without IT involvement?	15	27	22	t	t
703	Is PII protected within reports?	15	27	18	t	t
704	Are reports with sensitive data encrypted or secured if they are emailed to end users?	15	27	19	t	t
705	Is there an option for the users to run their own queries against the data and generate the reports or perform self-service reports?	15	27	20	t	t
706	How long does it (weeks or months?) typically take from the time business defines KPI's and the time it takes to generate a report corresponding to the KPI's?	15	27	21	f	t
708	Is there desire from business to query data using conversational AI?	15	27	23	t	f
710	What are the current known pain points that you are aware that you would like to see addressed?	15	27	25	f	f
709	Is there a plan to increase the number of dashboards/reports to become data driven organization?	15	27	24	t	t
711	Are there any specific topics that you would like to discuss or topics to be addressed as part of the assessment?	15	27	26	f	f
676	What is the infrastructure for storing cold data? 	15	26	21	f	f
722	What tools do you or does your team use to remove PII from test data?	15	28	10	f	f
713	Who tests your ML models before they are deployed in PROD? Do data scientists do all the testing or is there a dedicated team?	15	28	1	f	t
714	Do you or does your team test AI models including ML, LLM models with the same vigor as you do for software testing?	15	28	2	t	t
715	Do you or does your team create test plans and perform unit testing, functional testing, performance testing, UAT, A/B testing?	15	28	3	t	t
716	Do you or does your team test ML models for bias and drift?	15	28	4	t	t
717	Do you or does your team implement continuous monitoring of your ML model in production to ensure it maintains its performance over time?	15	28	5	t	t
718	Do you or does your team perform any benchmarking of the ML model performance?	15	28	6	t	t
719	Do you or does your team compute the performance metrics of the models and present it to the analytics team?	15	28	7	t	t
720	Do you or does your team bring any PII data from PROD and use it as it is for testing?	15	28	8	t	t
674	Do you have any analytics use cases for which you need SSD?	15	26	19	t	t
393	Are there any known GenAI use cases or would the orgranization be interested in knowing how data strategy can be enabler for GenAI?	15	16	7	t	f
675	Do you have any analytics use cases for which you need VM with excessively large amounts of memory?	15	26	20	t	t
721	What controls are in place to ensure there is no leakage of PII or sensitive data?	15	28	9	f	t
724	Is your testing pipeline automated?	15	28	12	t	t
725	Does your team or security team test the ML models agasint adversarial attacks? 	15	28	13	t	t
726	Does your team test the models's resilence agasint data poisoning attacks?	15	28	14	t	t
712	What methods are used for data testing and validation of data pipelines?	15	28	0	f	f
728	Are there any specific topics that you would like to discuss or topics to be addressed as part of the assessment?	15	28	16	f	f
386	What are the organization's overall business goals and objectives?	15	16	0	f	f
727	What are the current known pain points that you are aware that you would like to see it addressed?	15	28	15	f	f
730	Are there gaps or misalignments to address between your data strategy and your business strategy?	15	16	4	t	t
424	Is business ok with higher OPEX (Operational Expenditures) and lower CAPEX (Capital Expenditures) with higher overall cost over 5 yr time period as compared to higher CAPEX and lower OPEX?	15	16	38	t	f
467	What types of data processing and analysis are required (e.g., batch processing, real-time streaming, machine learning, data warehousing)?	15	18	5	f	f
485	Are there strategic initiatives that could benefit from accessing dark data?	15	18	23	t	t
547	Is there data retention policy?	15	20	28	t	t
614	How is data protected against unauthorized access and breaches?	15	24	6	f	f
636	Do you ensure that the models deployed as containers are secured, and encryption keys are appropriately managed within the containerized environment?	15	24	28	t	t
673	Do you perform any edge or fog computing? Does your organization have use cases for edge or fog computing? What does the infrastructure footprint look like at the edge?	15	26	18	f	f
699	Is the reporting server highly available?	15	27	14	t	t
423	How long does it take for a medium size complexity analytical project to from requirements to production? Are there any concerns about the time it takes to go live? 	15	16	37	f	t
513	Does the catalog include metadata, data lineage, and data usage information?	15	19	22	t	t
546	Do you have DataOps framework for management and governance of data or data assets throughout its lifecycle?	15	20	27	t	t
554	Is there a conceptual, logical and physical data model for the entire organization or just few selected data domains?	15	21	3	t	t
566	Do you have policies and procedures in place to ensure data privacy (e.g., compliance with GDPR, HIPAA)?	15	22	1	t	t
619	Are there opportunities to collaborate with other organizations to enhance the value of your data?	15	24	11	t	t
723	Does your team use any synthetic data? If yes, how is the synthetic data generated? If No, would your team be interested in learning more about test data generation for ML models?	15	28	11	t	t
373	What techniques/frameworks/toolkits/libraries such as LIME (Local Interpretable Model-agnostic Explanations) and SHAP (SHapley Additive exPlanations) are used or are in place to make the ML models interpretable and explainable?	15	15	8	f	f
565	Do you have a comprehensive strategy for handing sensitive or personally identifiable information (PII)?	15	22	0	t	t
\.


--
-- Data for Name: tb_question_score; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_question_score (id, question_id, affirmative_score, undecided_score, negative_score) FROM stdin;
729	388	10	5	0
730	389	10	5	0
731	390	10	5	0
732	391	10	5	0
733	392	10	5	0
734	394	10	5	0
735	395	10	5	0
736	396	10	5	0
737	397	10	5	0
738	398	10	5	0
739	399	10	5	0
740	400	10	5	0
741	401	10	5	0
742	402	10	5	0
743	403	10	5	0
745	405	10	5	0
746	406	10	5	0
747	407	10	5	0
748	408	10	5	0
749	409	10	5	0
750	410	10	5	0
751	411	10	5	0
752	412	10	5	0
754	414	10	5	0
755	415	10	5	0
756	416	10	5	0
757	417	10	5	0
758	418	10	5	0
759	419	10	5	0
760	420	10	5	0
761	421	10	5	0
762	422	10	5	0
763	365	10	5	0
764	387	10	5	0
765	366	10	5	0
766	367	10	5	0
767	368	10	5	0
768	369	10	5	0
769	370	10	5	0
770	371	10	5	0
771	372	10	5	0
772	374	10	5	0
773	375	10	5	0
774	376	10	5	0
775	377	10	5	0
776	378	10	5	0
777	379	10	5	0
778	380	10	5	0
779	381	10	5	0
780	382	10	5	0
781	383	10	5	0
782	384	10	5	0
783	385	10	5	0
784	425	10	5	0
785	426	10	5	0
787	428	10	5	0
788	429	10	5	0
789	430	10	5	0
790	431	10	5	0
791	432	10	5	0
792	433	10	5	0
793	434	10	5	0
794	435	10	5	0
795	436	10	5	0
796	437	10	5	0
797	438	10	5	0
799	440	10	5	0
800	441	10	5	0
801	442	10	5	0
802	443	10	5	0
803	444	10	5	0
804	445	10	5	0
805	446	10	5	0
806	447	10	5	0
807	448	10	5	0
808	449	10	5	0
809	450	10	5	0
810	451	10	5	0
811	452	10	5	0
812	453	10	5	0
813	454	10	5	0
814	455	10	5	0
815	456	10	5	0
816	457	10	5	0
817	458	10	5	0
818	459	10	5	0
819	460	10	5	0
820	461	10	5	0
821	462	10	5	0
822	463	10	5	0
823	464	10	5	0
824	465	10	5	0
825	466	10	5	0
826	468	10	5	0
827	469	10	5	0
828	470	10	5	0
829	471	10	5	0
832	474	10	5	0
834	476	10	5	0
835	477	10	5	0
836	478	10	5	0
837	479	10	5	0
838	480	10	5	0
839	481	10	5	0
840	482	10	5	0
841	483	10	5	0
842	484	10	5	0
843	424	10	5	0
844	487	10	5	0
845	488	10	5	0
846	489	10	5	0
847	490	10	5	0
848	491	10	5	0
849	492	10	5	0
850	493	10	5	0
851	494	10	5	0
852	495	10	5	0
853	496	10	5	0
854	497	10	5	0
855	498	10	5	0
856	499	10	5	0
857	500	10	5	0
858	501	10	5	0
859	502	10	5	0
860	503	10	5	0
861	504	10	5	0
862	505	10	5	0
863	506	10	5	0
864	507	10	5	0
865	508	10	5	0
866	509	10	5	0
867	510	10	5	0
869	512	10	5	0
870	514	10	5	0
871	515	10	5	0
872	516	10	5	0
873	517	10	5	0
874	518	10	5	0
875	519	10	5	0
876	520	10	5	0
877	521	10	5	0
878	522	10	5	0
879	523	10	5	0
880	524	10	5	0
881	525	10	5	0
882	526	10	5	0
883	527	10	5	0
884	528	10	5	0
885	529	10	5	0
753	413	0	5	10
798	439	0	5	10
830	472	0	5	10
831	473	0	5	10
833	475	0	5	10
868	511	0	5	10
886	530	10	5	0
887	531	10	5	0
888	532	10	5	0
890	534	10	5	0
891	535	10	5	0
892	536	10	5	0
893	537	10	5	0
894	538	10	5	0
895	539	10	5	0
896	540	10	5	0
897	541	10	5	0
898	542	10	5	0
899	543	10	5	0
900	544	10	5	0
901	545	10	5	0
902	486	10	5	0
903	549	10	5	0
904	550	10	5	0
905	551	10	5	0
906	552	10	5	0
907	553	10	5	0
908	555	10	5	0
909	556	10	5	0
910	557	10	5	0
911	558	10	5	0
912	559	10	5	0
913	560	10	5	0
914	561	10	5	0
915	562	10	5	0
916	563	10	5	0
917	564	10	5	0
918	573	10	5	0
919	574	10	5	0
920	575	10	5	0
921	576	10	5	0
922	577	10	5	0
923	578	10	5	0
924	579	10	5	0
925	580	10	5	0
926	581	10	5	0
927	582	10	5	0
928	583	10	5	0
929	584	10	5	0
930	585	10	5	0
931	586	10	5	0
932	587	10	5	0
933	588	10	5	0
934	589	10	5	0
935	590	10	5	0
936	591	10	5	0
937	592	10	5	0
938	593	10	5	0
939	594	10	5	0
940	595	10	5	0
941	596	10	5	0
942	597	10	5	0
943	598	10	5	0
944	599	10	5	0
945	600	10	5	0
946	601	10	5	0
947	602	10	5	0
948	603	10	5	0
949	604	10	5	0
950	605	10	5	0
951	606	10	5	0
952	607	10	5	0
953	565	10	5	0
954	567	10	5	0
955	568	10	5	0
956	569	10	5	0
957	570	10	5	0
958	571	10	5	0
959	572	10	5	0
960	608	10	5	0
961	609	10	5	0
962	610	10	5	0
963	611	10	5	0
964	612	10	5	0
965	613	10	5	0
966	548	10	5	0
967	616	10	5	0
968	617	10	5	0
969	618	10	5	0
970	620	10	5	0
971	621	10	5	0
972	622	10	5	0
973	623	10	5	0
974	624	10	5	0
975	625	10	5	0
976	626	10	5	0
977	627	10	5	0
978	628	10	5	0
979	629	10	5	0
980	630	10	5	0
981	631	10	5	0
982	632	10	5	0
983	633	10	5	0
984	634	10	5	0
985	635	10	5	0
986	637	10	5	0
987	638	10	5	0
988	639	10	5	0
989	640	10	5	0
990	641	10	5	0
991	642	10	5	0
992	643	10	5	0
994	645	10	5	0
995	646	10	5	0
996	647	10	5	0
997	648	10	5	0
998	649	10	5	0
999	650	10	5	0
1000	651	10	5	0
1001	652	10	5	0
1002	653	10	5	0
1003	654	10	5	0
1004	655	10	5	0
1005	656	10	5	0
1006	657	10	5	0
1007	658	10	5	0
1008	659	10	5	0
1009	660	10	5	0
1010	661	10	5	0
1011	662	10	5	0
1012	663	10	5	0
1014	665	10	5	0
1015	666	10	5	0
1016	667	10	5	0
1017	668	10	5	0
1018	669	10	5	0
1019	670	10	5	0
1020	671	10	5	0
1021	672	10	5	0
1022	615	10	5	0
1023	675	10	5	0
1024	676	10	5	0
1025	677	10	5	0
1026	678	10	5	0
1027	679	10	5	0
1028	680	10	5	0
1029	681	10	5	0
1030	682	10	5	0
1031	683	10	5	0
1032	684	10	5	0
1033	685	10	5	0
1034	686	10	5	0
1035	687	10	5	0
1036	688	10	5	0
1037	689	10	5	0
1038	690	10	5	0
1039	691	10	5	0
1040	692	10	5	0
1041	693	10	5	0
1042	694	10	5	0
993	644	0	5	10
1043	695	10	5	0
1044	696	10	5	0
1045	697	10	5	0
1046	698	10	5	0
1047	700	10	5	0
1048	701	10	5	0
1049	702	10	5	0
1050	703	10	5	0
1051	704	10	5	0
1052	705	10	5	0
1053	706	10	5	0
1054	707	10	5	0
1055	708	10	5	0
1056	709	10	5	0
1057	710	10	5	0
1058	711	10	5	0
1059	712	10	5	0
1060	713	10	5	0
1061	714	10	5	0
1062	715	10	5	0
1063	716	10	5	0
1064	717	10	5	0
1065	718	10	5	0
1066	719	10	5	0
1067	393	10	5	0
1068	386	10	5	0
1069	674	10	5	0
1070	720	10	5	0
1071	721	10	5	0
1072	722	10	5	0
1073	723	10	5	0
1074	724	10	5	0
1075	725	10	5	0
1076	726	10	5	0
1077	727	10	5	0
1078	728	10	5	0
1079	423	10	5	0
1080	467	10	5	0
1081	485	10	5	0
1082	513	10	5	0
1083	546	10	5	0
1084	547	10	5	0
1085	554	10	5	0
1086	566	10	5	0
1087	614	10	5	0
1088	619	10	5	0
1089	636	10	5	0
1090	673	10	5	0
1091	699	10	5	0
1092	373	10	5	0
744	404	0	5	10
786	427	0	5	10
889	533	0	5	10
1013	664	0	5	10
1093	730	0	5	10
\.


--
-- Data for Name: tb_questionnaire_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_questionnaire_status (id, session_id, topic, question, answer, score, sentiment_id, created_at, updated_at) FROM stdin;
4	60bc8eca-e06c-4a6f-8fb3-c84c33c7a34a	Business Alignment	What are the organization's overall business goals and objectives?	\N	\N	0	2024-01-29 10:33:18.589814	2024-01-29 10:33:18.589814
5	38989d65-a7cc-4fc3-9615-8ea3ba5c3afb	Business Alignment	What are the organization's overall business goals and objectives?	\N	10	0	2024-01-29 10:34:24.019191	2024-01-29 10:34:24.019191
6	49c90ae9-1f54-4368-848f-32742e82a4d6	Business Alignment	What are the organization's overall business goals and objectives?	\N	\N	0	2024-01-29 11:22:20.724153	2024-01-29 11:22:20.724153
7	cf19c46c-5011-432f-bdf6-8e979ed47d23	Business Alignment	What are the organization's overall business goals and objectives?	Yes, the main goals include increasing profitability, expanding market share, and enhancing customer satisfaction to ensure long-term success.	10	0	2024-01-29 11:24:31.756077	2024-01-29 11:25:24.427642
8	cf19c46c-5011-432f-bdf6-8e979ed47d23	Business Alignment	Does your current data strategy align with your business strategy? Are there gaps or misalignments to address?	Partially, our data strategy aligns with our business goals, but there are significant gaps in data integration and accessibility across departments. Addressing these gaps is crucial for achieving a more cohesive and efficient operation.	5	0	2024-01-29 11:25:30.305232	2024-01-29 11:31:01.475856
19	cf19c46c-5011-432f-bdf6-8e979ed47d23	Data Assets	What types of data does the organization collect and store?	Financial records, including income statements, balance sheets, and transaction histories, are meticulously collected and stored for compliance, reporting, and strategic planning purposes.	10	0	2024-01-29 15:52:54.957804	2024-01-29 15:56:50.558606
20	cf19c46c-5011-432f-bdf6-8e979ed47d23	Data Assets	Do you have an inventory of all data assets, including their location and sensitivity?	Yes, we have a comprehensive inventory that includes the location and sensitivity of all data assets.	10	4	2024-01-29 15:56:56.615068	2024-01-29 15:57:18.002863
25	cf19c46c-5011-432f-bdf6-8e979ed47d23	Data Privacy	Do you have policies and procedures in place to ensure data privacy (e.g., compliance with GDPR, HIPAA)?	Yes, we have comprehensive policies and procedures in place to ensure data privacy, including compliance with GDPR, HIPAA, and other relevant regulations.	10	4	2024-01-29 16:12:11.67913	2024-01-29 16:13:34.116349
16	cf19c46c-5011-432f-bdf6-8e979ed47d23	Business Alignment	Is there data governance that aligns and support business objectives?	Yes, our data governance framework is meticulously designed to ensure it aligns with and supports our overarching business objectives, including enhancing operational efficiency and ensuring regulatory compliance.	10	4	2024-01-29 15:46:24.72351	2024-01-29 15:48:24.534663
17	cf19c46c-5011-432f-bdf6-8e979ed47d23	Business Alignment	Are there any known use cases that the data strategy is going to drive for implementation?	Partially, some use cases have been identified, but it's still unclear how the data strategy will drive their implementation. Further analysis and planning are needed to clarify this.	0	3	2024-01-29 15:48:26.012788	2024-01-29 15:52:28.155086
18	cf19c46c-5011-432f-bdf6-8e979ed47d23	Data Assets	How does your company acquire data and ensure data quality?	We primarily collect data directly from our operations and customer interactions. This in-house data collection is facilitated by our advanced IT infrastructure, which includes IoT devices and online platforms. To maintain high data quality, we implement strict data entry standards and use sophisticated data cleaning and validation tools.	0	0	2024-01-29 15:52:31.190374	2024-01-29 15:52:46.814156
21	cf19c46c-5011-432f-bdf6-8e979ed47d23	Data Assets	How is data classified? Have data assets been classified based on their importance and sensitivity?	Yes, all data assets have been meticulously classified according to their level of importance and sensitivity, ensuring that each category is managed with the appropriate level of security and access control.	10	4	2024-01-29 15:57:24.613434	2024-01-29 15:57:44.82297
22	cf19c46c-5011-432f-bdf6-8e979ed47d23	Data Assets	What are the types and sources of data that your organization deals with (e.g., structured, semi-structured, unstructured)?	Yes, our organization handles a variety of data types including structured data from databases, semi-structured data such as XML or JSON files, and unstructured data like emails, documents, and multimedia.	10	4	2024-01-29 15:57:52.883486	2024-01-29 15:59:01.208612
15	cf19c46c-5011-432f-bdf6-8e979ed47d23	Business Alignment	How does data or data strategy support these goals?	Yes, our data strategy is integral to achieving our goals. It enables us to make informed decisions, optimize operations, and enhance customer experiences, directly contributing to profit maximization and market share growth.	10	5	2024-01-29 15:29:37.566618	2024-01-29 15:42:14.114217
23	cf19c46c-5011-432f-bdf6-8e979ed47d23	Data Privacy	How do you handle sensitive or personally identifiable information (PII)?	Our handling of sensitive or personally identifiable information (PII) is in strict compliance with relevant data protection laws, such as GDPR in the European Union. We conduct regular training for our staff to ensure they are aware of their responsibilities and the legal requirements for protecting customer data.	0	0	2024-01-29 15:59:03.784034	2024-01-29 16:11:04.838037
24	cf19c46c-5011-432f-bdf6-8e979ed47d23	Data Privacy	How do you handle customer and employee data privacy? What tools or technology is used?	Yes, we prioritize data privacy for both customers and employees by employing advanced encryption technologies and strict access controls. We use tools like secure cloud storage solutions and data anonymization software to ensure that personal information is protected at all times.	10	4	2024-01-29 16:11:26.353771	2024-01-29 16:12:09.697896
26	cf19c46c-5011-432f-bdf6-8e979ed47d23	Data Privacy	How is right to forget as part of GDPR compliance implemented?	Yes, the right to be forgotten is fully implemented as part of our GDPR compliance. We have established processes to ensure that individuals can easily request the deletion of their personal data, and we ensure these requests are processed in a timely manner.	10	4	2024-01-29 16:13:55.715513	2024-01-29 16:18:17.046662
27	cf19c46c-5011-432f-bdf6-8e979ed47d23	Data Privacy	Is consent across multiple LOBs stored in a central repository and exposed as API?	No, currently, consent data is managed separately within each Line of Business (LOB), without a centralized repository or API exposure.	0	2	2024-01-29 16:18:28.304583	2024-01-29 16:19:11.23125
28	35d4bcec-dd36-4b53-8cdd-742254ea5920	Business Alignment	What are the organization's overall business goals and objectives?	\N	\N	0	2024-02-01 16:34:16.25365	2024-02-01 16:34:16.25365
29	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Data Privacy	How do you handle sensitive or personally identifiable information (PII)?	Whenever possible, we minimize the collection of sensitive or personally identifiable information (PII) and use data anonymization techniques to protect individual identities. This approach reduces the risk of data breaches and ensures that the data we do collect is only what is necessary for our operations.	10	0	2024-02-06 09:04:27.316386	2024-02-06 09:04:38.487894
54	7562def8-24ed-4756-83b2-1ec124ae4baf	Data Assets	Does the data catalog support dynamic or auto discovery of data assets?	No, unfortunately, our data catalog does not support dynamic or auto discovery of data assets.	0	2	2024-03-11 12:03:07.158946	2024-03-11 12:07:18.18015
30	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Data Privacy	How do you handle customer and employee data privacy? What tools or technology is used?	Yes, we prioritize data privacy for both customers and employees by employing advanced encryption technologies and strict access controls. We use tools like secure cloud storage solutions and data anonymization software to ensure that personal information is protected at all times.	10	4	2024-02-06 09:04:43.295148	2024-02-06 09:05:10.734443
31	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Data Privacy	Do you have policies and procedures in place to ensure data privacy (e.g., compliance with GDPR, HIPAA)?	Yes, we have comprehensive policies and procedures in place to ensure data privacy, including compliance with GDPR, HIPAA, and other relevant regulations.	10	4	2024-02-06 09:05:12.733041	2024-02-06 09:05:21.628747
32	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Data Privacy	How is right to forget as part of GDPR compliance implemented?	No, unfortunately, we have not fully implemented the right to be forgotten as part of our GDPR compliance. We are currently working on developing the necessary processes and systems to support this requirement.	0	2	2024-02-06 09:05:40.456202	2024-02-06 09:05:57.956839
33	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Data Privacy	Is consent across multiple LOBs stored in a central repository and exposed as API?	Yes, all consents across various Lines of Business (LOBs) are centrally stored and accessible via an API, ensuring streamlined data management and compliance.	10	4	2024-02-06 09:06:08.676065	2024-02-06 09:06:23.109125
34	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Dataops	Can you define what does DevOps/DataOps pipeline look like?	No, it's challenging to define a universal DevOps/DataOps pipeline as it varies significantly depending on the organization's specific needs and the technologies they use.	0	2	2024-02-06 09:06:25.512088	2024-02-06 09:06:59.196228
35	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Dataops	What tools and technologies are used for DevOps/DataOps automation?	Yes, we use a variety of tools and technologies for DevOps/DataOps automation, including Jenkins for continuous integration, Docker for containerization, Ansible for configuration management, and Apache Airflow for workflow automation.	10	4	2024-02-06 09:07:26.54802	2024-02-06 09:07:33.488359
36	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Dataops	Are there dedicated DataOps teams or roles within the organization?	We are in the process of evaluating the need for dedicated DataOps roles or teams. Some departments have initiated pilot projects to assess the impact of DataOps practices on their operations.	0	3	2024-02-06 09:07:44.782332	2024-02-06 09:08:08.609127
37	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Dataops	How do teams collaborate on DevOps/DataOps tasks and projects?	Partially, while some teams have established strong collaboration practices, others still struggle with communication and alignment. The success of collaboration varies significantly across different projects and departments.	0	3	2024-02-06 09:08:19.30103	2024-02-06 09:08:43.382519
38	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Dataops	Is there a culture of collaboration and automation within the DevOps/DataOps teams?	Yes, definitely, of course. Our teams are highly integrated, focusing on seamless collaboration and the automation of processes to enhance efficiency and productivity.	10	5	2024-02-06 09:08:51.538689	2024-02-06 09:08:59.708924
39	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Testing	What methods are used for data testing and validation of data pipelines?	Yes, we employ a variety of methods for data testing and validation, including automated testing, manual inspection, and the use of data quality tools to ensure the integrity and accuracy of our data pipelines.	10	4	2024-02-06 09:09:01.736373	2024-02-06 09:09:18.835605
40	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Testing	Do you or does your team test ML models for bias and drift?	Yes, we actively test our ML models for bias and drift to ensure fairness and accuracy in predictions.	10	4	2024-02-06 09:09:22.542256	2024-02-06 09:09:52.239281
41	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Testing	Do you or does your team create test plans and perform unit testing, functional testing, performance testing, UAT, A/B testing?	Yes, we definitely create very thorough test plans for testing and have a dedicated team for that.\n	10	4	2024-02-06 09:09:56.825423	2024-02-06 09:10:37.768537
42	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Testing	Who tests your ML models before they are deployed in PROD? Do data scientists do all the testing or is there a dedicated team?	Testing of ML models is a collaborative effort between data scientists and a specialized testing team. Data scientists perform the initial tests, while the testing team conducts further, more rigorous testing to ensure the models are ready for production.	10	0	2024-02-06 09:10:41.667806	2024-02-06 09:10:52.019021
43	92f5e819-e65d-4502-a9b6-d912ea5d32a2	Testing	Do you or does your team test AI models including ML, LLM models with the same vigor as you do for software testing?	Actually even more vigour that normally. ML models are really tested very well.\n	10	4	2024-02-06 09:10:55.932441	2024-02-06 09:11:26.968123
44	83befd92-7a6f-4c0a-a459-1d41cf399334	Business Alignment	What are the organization's overall business goals and objectives?	\N	\N	0	2024-02-06 09:26:23.310262	2024-02-06 09:26:23.310262
45	7562def8-24ed-4756-83b2-1ec124ae4baf	Business Alignment	Is there a published business strategy that data strategy needs to align to?	Yes, indeed, there is a published business strategy that our data strategy aligns to.	10	4	2024-03-11 09:26:52.847433	2024-03-11 11:41:34.596723
46	7562def8-24ed-4756-83b2-1ec124ae4baf	Business Alignment	Does your current data strategy align with your business strategy?	There might be some minor misalignments between our data strategy and business strategy, but we are in the process of reviewing and addressing these.	0	3	2024-03-11 11:41:35.951629	2024-03-11 11:41:57.347694
47	7562def8-24ed-4756-83b2-1ec124ae4baf	Business Alignment	Are there gaps or misalignments to address between your data strategy and your business strategy?	No, there are some gaps available between our data and business strategy.	10	2	2024-03-11 11:41:59.907445	2024-03-11 11:52:56.969978
48	7562def8-24ed-4756-83b2-1ec124ae4baf	Business Alignment	Is there data governance that aligns and support business objectives?	Yes, indeed, our data governance is designed to align with and support our business objectives.	10	5	2024-03-11 11:52:58.923939	2024-03-11 11:53:34.861139
49	7562def8-24ed-4756-83b2-1ec124ae4baf	Business Alignment	What is your budget for data-related initiatives for the coming year?	The budget for data-related initiatives for the coming year is only partially adequate.	5	0	2024-03-11 11:53:36.116733	2024-03-11 11:54:15.412125
50	7562def8-24ed-4756-83b2-1ec124ae4baf	Data Assets	Do you have an inventory of all data assets, including their location and sensitivity?	No, unfortunately, we do not have a complete inventory of all our data assets at this time.	0	2	2024-03-11 11:54:17.049511	2024-03-11 11:55:34.217514
51	7562def8-24ed-4756-83b2-1ec124ae4baf	Data Assets	Have data assets been classified based on their importance and sensitivity?	Some assets have been classified based on their importance and sensitivity.	0	3	2024-03-11 11:55:38.296555	2024-03-11 12:01:14.03725
52	7562def8-24ed-4756-83b2-1ec124ae4baf	Data Assets	Do you have tools or teams dedicated to analyzing dark data?	Yes, indeed, we have both tools and teams specifically dedicated to analysing dark data.	10	5	2024-03-11 12:01:31.533071	2024-03-11 12:02:04.513018
53	7562def8-24ed-4756-83b2-1ec124ae4baf	Data Assets	Is there a data catalog in place?	Yes, indeed, we do have a data catalog in place.	10	5	2024-03-11 12:02:18.831176	2024-03-11 12:02:56.256664
55	7562def8-24ed-4756-83b2-1ec124ae4baf	Data Privacy	Do you have policies and procedures in place to ensure data privacy (e.g., compliance with GDPR, HIPAA)?	Yes, indeed. We have robust policies and procedures in place to ensure data privacy, including compliance with GDPR, HIPAA and other relevant regulations.	10	5	2024-03-11 12:07:19.775118	2024-03-11 12:07:37.170219
56	7562def8-24ed-4756-83b2-1ec124ae4baf	Data Privacy	Do you use any tokenization tools to tokenize PII data fields?	Yes, we do use tokenization tools to tokenize PII data fields.	10	4	2024-03-11 12:07:42.059175	2024-03-11 12:10:05.8815
57	7562def8-24ed-4756-83b2-1ec124ae4baf	Data Privacy	Is consent across multiple LOBs stored in a central repository and exposed as API?	No, consent across multiple LOBs is not currently stored in a central repository nor exposed as an API.	0	2	2024-03-11 12:10:09.397738	2024-03-11 12:12:27.500302
58	7562def8-24ed-4756-83b2-1ec124ae4baf	Data Privacy	Did you implement right to forget as part of GDPR compliance?	We have implemented right to forget as part of GDPR compliance.	10	5	2024-03-11 13:00:35.785914	2024-03-11 13:26:51.272081
59	7562def8-24ed-4756-83b2-1ec124ae4baf	Data Privacy	Do you have a comprehensive strategy for handing sensitive or personally identifiable information (PII)?	We have a partial strategy available which covers some aspects of our handing of sensitive or personally identifiable information (PII).	0	3	2024-03-11 13:26:55.485913	2024-03-11 13:27:11.207524
\.


--
-- Data for Name: tb_quiz_mode; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_quiz_mode (id, name, question_count) FROM stdin;
1	Easy	3
2	Medium	5
3	Professional	7
4	Expert	8
\.


--
-- Data for Name: tb_selected_quiz_mode; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_selected_quiz_mode (id, session_id, quiz_mode_id) FROM stdin;
1	60bc8eca-e06c-4a6f-8fb3-c84c33c7a34a	2
2	38989d65-a7cc-4fc3-9615-8ea3ba5c3afb	2
3	49c90ae9-1f54-4368-848f-32742e82a4d6	2
4	cf19c46c-5011-432f-bdf6-8e979ed47d23	2
5	35d4bcec-dd36-4b53-8cdd-742254ea5920	2
6	92f5e819-e65d-4502-a9b6-d912ea5d32a2	2
7	83befd92-7a6f-4c0a-a459-1d41cf399334	1
8	7562def8-24ed-4756-83b2-1ec124ae4baf	2
\.


--
-- Data for Name: tb_selected_topics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_selected_topics (id, session_id, topic_id, created_at) FROM stdin;
1	60bc8eca-e06c-4a6f-8fb3-c84c33c7a34a	16	2024-01-29 10:33:16.10267
2	60bc8eca-e06c-4a6f-8fb3-c84c33c7a34a	19	2024-01-29 10:33:16.10267
3	60bc8eca-e06c-4a6f-8fb3-c84c33c7a34a	22	2024-01-29 10:33:16.10267
4	38989d65-a7cc-4fc3-9615-8ea3ba5c3afb	16	2024-01-29 10:34:22.02855
5	38989d65-a7cc-4fc3-9615-8ea3ba5c3afb	19	2024-01-29 10:34:22.02855
6	38989d65-a7cc-4fc3-9615-8ea3ba5c3afb	22	2024-01-29 10:34:22.02855
7	49c90ae9-1f54-4368-848f-32742e82a4d6	16	2024-01-29 11:22:18.333224
8	49c90ae9-1f54-4368-848f-32742e82a4d6	19	2024-01-29 11:22:18.333224
9	49c90ae9-1f54-4368-848f-32742e82a4d6	22	2024-01-29 11:22:18.333224
10	cf19c46c-5011-432f-bdf6-8e979ed47d23	16	2024-01-29 11:24:29.869592
11	cf19c46c-5011-432f-bdf6-8e979ed47d23	19	2024-01-29 11:24:29.869592
12	cf19c46c-5011-432f-bdf6-8e979ed47d23	22	2024-01-29 11:24:29.869592
13	35d4bcec-dd36-4b53-8cdd-742254ea5920	16	2024-02-01 16:34:14.402716
14	35d4bcec-dd36-4b53-8cdd-742254ea5920	19	2024-02-01 16:34:14.402716
15	35d4bcec-dd36-4b53-8cdd-742254ea5920	22	2024-02-01 16:34:14.402716
16	35d4bcec-dd36-4b53-8cdd-742254ea5920	23	2024-02-01 16:34:14.402716
17	92f5e819-e65d-4502-a9b6-d912ea5d32a2	22	2024-02-06 09:04:25.829812
18	92f5e819-e65d-4502-a9b6-d912ea5d32a2	25	2024-02-06 09:04:25.829812
19	92f5e819-e65d-4502-a9b6-d912ea5d32a2	28	2024-02-06 09:04:25.829812
20	83befd92-7a6f-4c0a-a459-1d41cf399334	16	2024-02-06 09:26:20.301131
21	83befd92-7a6f-4c0a-a459-1d41cf399334	19	2024-02-06 09:26:20.301131
22	83befd92-7a6f-4c0a-a459-1d41cf399334	22	2024-02-06 09:26:20.301131
23	7562def8-24ed-4756-83b2-1ec124ae4baf	16	2024-03-11 09:26:50.169297
24	7562def8-24ed-4756-83b2-1ec124ae4baf	19	2024-03-11 09:26:50.169297
25	7562def8-24ed-4756-83b2-1ec124ae4baf	22	2024-03-11 09:26:50.169297
\.


--
-- Data for Name: tb_sentiment_score; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_sentiment_score (id, name) FROM stdin;
0	unknown
1	very negative
2	negative
3	ambiguous
4	positive
5	very positive
\.


--
-- Data for Name: tb_suggested_response; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_suggested_response (id, title, subtitle, body, question_id, score) FROM stdin;
1852	Affirmative	\N	Yes, indeed, there is a published business strategy that our data strategy aligns to.	389	0
1853	Negative	\N	No, unfortunately, there isn't a published business strategy for our data strategy to align to at the moment.	389	0
1854	Undecided	\N	There might be a published business strategy, but I would need to confirm this.	389	0
1855	Affirmative	\N	Yes, our current data strategy is fully aligned with our business strategy. We have made sure that our data initiatives support our business objectives.	390	0
1856	Negative	\N	No, unfortunately, there are some gaps and misalignments between our data strategy and business strategy that we need to address.	390	0
1857	Undecided	\N	There might be some minor misalignments between our data strategy and business strategy, but we are in the process of reviewing and addressing these.	390	0
1858	Affirmative	\N	Yes, indeed, there is a significant market demand for the type of data our organisation possesses.	391	0
1859	Negative	\N	No, unfortunately, there doesn't seem to be a market demand for the type of data our organisation possesses.	391	0
1860	Undecided	\N	It's uncertain at the moment, we are still conducting market research to determine the demand for the type of data our organisation possesses.	391	0
1861	Affirmative	\N	Yes, indeed, we have several GenAI use cases and we are always interested in learning how data strategy can further enable GenAI.	393	0
1862	Negative	\N	No, currently we do not have any known GenAI use cases and we are not considering data strategy as an enabler for GenAI at the moment.	393	0
1863	Undecided	\N	We might have some GenAI use cases, but I would need to confirm. As for data strategy being an enabler for GenAI, we would certainly be interested in exploring this further.	393	0
1864	Affirmative	\N	Yes, absolutely. We understand the potential business impact of analysing and using currently untapped data sources. It can provide us with valuable insights and help us make informed decisions.	394	0
1865	Negative	\N	No, we have not yet fully explored the potential business impact of analysing and using currently untapped data sources.	394	0
1866	Undecided	\N	We are somewhat aware of the potential business impact of analysing and using currently untapped data sources, but we need to conduct further research to fully understand its implications.	394	0
1867	Affirmative	\N	Yes, indeed, our data governance is designed to align with and support our business objectives.	395	0
1868	Negative	\N	No, unfortunately, our data governance does not currently align with or support our business objectives.	395	0
1869	Undecided	\N	Partially, our data governance does align with some of our business objectives, but there is still room for improvement.	395	0
1870	Affirmative	\N	Yes, absolutely. Our executives are fully supportive of our data initiatives.	396	0
1871	Negative	\N	No, unfortunately, we do not have executive support for our data initiatives at the moment.	396	0
1872	Undecided	\N	It's a bit of a mixed bag. Some executives are supportive, while others need more convincing.	396	0
1873	Affirmative	\N	Yes, indeed, we have allocated a budget specifically for data infrastructure needs.	397	0
1874	Negative	\N	No, unfortunately, we have not yet allocated a budget for data infrastructure needs.	397	0
1875	Undecided	\N	There might be some budget set aside for data infrastructure, but I would need to confirm this.	397	0
1876	Affirmative	\N	Yes, indeed, there are always opportunities for cost optimisation in any business.	400	0
1877	Negative	\N	No, at the moment, we have already optimised all costs to the best of our ability.	400	0
1878	Undecided	\N	Possibly, we would need to conduct a thorough review of our operations to identify any potential areas for cost optimisation.	400	0
1879	Affirmative	\N	Yes, we have explored various monetization models including data licensing, data subscriptions, and data-as-a-service.	402	0
1880	Negative	\N	No, we have not yet explored various monetization models such as data licensing, data subscriptions, or data-as-a-service.	402	0
1881	Undecided	\N	We have started looking into different monetization models, but we have not yet fully explored options like data licensing, data subscriptions, or data-as-a-service.	402	0
1882	Affirmative	\N	Yes, indeed, stakeholders have identified several challenges related to data, such as data quality issues and lack of data integration.	404	0
1883	Negative	\N	No, so far, stakeholders have not identified any specific pain points or challenges related to data.	404	0
1884	Undecided	\N	There might be some challenges related to data that stakeholders have identified, but I would need to confirm this.	404	0
1885	Affirmative	\N	Yes, indeed. There is always room for improvement in data sharing and collaboration amongst internal teams.	406	0
1886	Negative	\N	No, our current systems and processes for data sharing and collaboration are already optimised.	406	0
1887	Undecided	\N	Possibly, it would be beneficial to review our current data sharing and collaboration processes to identify any areas for simplification.	406	0
1888	Affirmative	\N	Yes, absolutely. It's crucial to democratize data access and empower business units to access and analyse data independently. This will foster a data-driven culture and enhance decision-making processes.	409	0
1889	Negative	\N	No, it's not necessary. We have a dedicated data team that handles all data-related tasks. This ensures data security and consistency.	409	0
1890	Undecided	\N	It's a bit of a mixed bag. While it's beneficial to empower business units to access and analyse data independently, we also need to consider data security and governance issues.	409	0
1891	Affirmative	\N	Yes, absolutely. There are stringent ethical guidelines in place regarding data usage and sharing in our industry.	410	0
1892	Negative	\N	No, there are no specific ethical considerations related to data usage and sharing in our industry.	410	0
1893	Undecided	\N	There might be some ethical considerations, but I would need to look into it more thoroughly to give a definitive answer.	410	0
1894	Affirmative	\N	Yes, indeed, there are emerging use cases that necessitate agility in data access and processing.	411	0
1895	Negative	\N	No, at the moment, there are no emerging use cases that require agility in data access and processing.	411	0
1896	Undecided	\N	Possibly, there might be emerging use cases that require agility in data access and processing, but I would need to investigate further.	411	0
1897	Affirmative	\N	Yes, indeed, there are certain bottlenecks in data access, processing, and analytics.	413	0
1898	Negative	\N	No, there are no bottlenecks in data access, processing, or analytics.	413	0
1899	Undecided	\N	There might be some bottlenecks in data access, processing, or analytics, but I would need to investigate further to confirm.	413	0
1900	Affirmative	\N	Yes, absolutely. We are always open to realigning our data teams to better suit the needs of our data consumption.	414	0
1901	Negative	\N	No, at the moment, we are not considering realigning our data teams based on data consumption.	414	0
1902	Undecided	\N	It's possible, but we would need to evaluate the benefits and potential challenges of such a realignment.	414	0
1903	Affirmative	\N	Yes, we have conducted extensive market research and received numerous inquiries from potential data buyers.	415	0
1904	Negative	\N	No, we have not yet conducted any market research or received inquiries from potential data buyers.	415	0
1905	Undecided	\N	We have conducted some market research, but we have not yet received any inquiries from potential data buyers.	415	0
1906	Affirmative	\N	Yes, indeed, there are several competitors and data providers offering similar data products or services.	416	0
1907	Negative	\N	No, as far as we are aware, there are no competitors or data providers offering similar data products or services.	416	0
1908	Undecided	\N	There might be some competitors or data providers offering similar data products or services, but we need to conduct further research to confirm this.	416	0
1909	Affirmative	\N	Yes, indeed, we have several initiatives that require the ingestion of social media data and CCTV data.	421	0
1910	Negative	\N	No, at the moment, we do not have any initiatives that require the ingestion of social media data or CCTV data.	421	0
1911	Undecided	\N	There might be some initiatives that require the ingestion of social media data or CCTV data, but I would need to confirm this.	421	0
1912	Affirmative	\N	Yes, indeed, we are actively working on making our analytics data highly available to our external partners as part of our data monetisation strategy.	422	0
1913	Negative	\N	No, at present, we do not have any plans to make our analytics data available 24x7 to external partners.	422	0
1914	Undecided	\N	We are currently exploring various options, and making our analytics data highly available to external partners is one of the possibilities under consideration.	422	0
1915	Affirmative	\N	Yes, the business is comfortable with a higher OPEX and lower CAPEX model if it leads to a higher overall cost over a 5-year period, as compared to a higher CAPEX and lower OPEX model.	424	0
1916	Negative	\N	No, the business is not in favour of a higher OPEX and lower CAPEX model if it results in a higher overall cost over a 5-year period, as compared to a higher CAPEX and lower OPEX model.	424	0
1917	Undecided	\N	It's uncertain at this point. The business is still evaluating the potential impact of a higher OPEX and lower CAPEX model versus a higher CAPEX and lower OPEX model over a 5-year period.	424	0
1918	Affirmative	\N	Yes, we have a highly skilled team in-house that is capable of handling all our business needs.	426	0
1919	Negative	\N	No, we often rely on external expertise to supplement our in-house capabilities.	426	0
1920	Undecided	\N	We have some skills in-house, but we also utilise external expertise when necessary.	426	0
1921	Affirmative	\N	Yes, indeed, there are certain skill gaps that we need to address.	427	0
1922	Negative	\N	No, at the moment, we believe our team has all the necessary skills.	427	0
1923	Undecided	\N	Possibly, we are currently in the process of evaluating our team's skills.	427	0
1924	Affirmative	\N	Yes, indeed, we do have a mandatory data training for all new employees, including contractors.	428	0
1925	Negative	\N	No, unfortunately, we do not have a mandatory data training for all new employees and contractors.	428	0
1926	Undecided	\N	There is some form of data training, but I'm not entirely sure if it's mandatory for all new employees and contractors.	428	0
1927	Affirmative	\N	Yes, indeed. There are several strategic initiatives that could greatly benefit from accessing dark data.	429	0
1928	Negative	\N	No, at the moment, we do not see any strategic initiatives that could benefit from accessing dark data.	429	0
1929	Undecided	\N	Potentially, there might be some strategic initiatives that could benefit from accessing dark data, but we would need to investigate this further.	429	0
1930	Affirmative	\N	Yes, indeed, we are continuously exploring and analysing our dark data to uncover valuable insights.	430	0
1931	Negative	\N	No, unfortunately, we have not yet initiated any efforts to explore or analyse our dark data.	430	0
1932	Undecided	\N	We have started some preliminary exploration of our dark data, but it's still early days and we have a long way to go.	430	0
1933	Affirmative	\N	Yes, indeed, there are several use cases that our data strategy is designed to drive for implementation.	431	0
1934	Negative	\N	No, at the moment, we do not have any specific use cases that the data strategy is going to drive for implementation.	431	0
1935	Undecided	\N	There might be some use cases that the data strategy could drive for implementation, but we are still in the process of identifying them.	431	0
1936	Affirmative	\N	Yes, indeed, we have several data-driven initiatives currently in progress and more planned for the future.	432	0
1937	Negative	\N	No, at the moment, we do not have any specific data-driven initiatives in progress or planned.	432	0
1938	Undecided	\N	There might be some data-driven initiatives in the pipeline, but I would need to confirm this.	432	0
1939	Affirmative	\N	Yes, indeed, our data lake is utilised as a real-time data hub.	435	0
1940	Negative	\N	No, our data lake is not currently used as a real-time data hub.	435	0
1941	Undecided	\N	It's a bit of a mixed bag, our data lake is used as a real-time data hub for some applications, but not for all.	435	0
1942	Affirmative	\N	Yes, indeed, there are some data integration challenges we are currently facing.	439	0
1943	Negative	\N	No, we have not encountered any significant data integration challenges or bottlenecks.	439	0
1944	Undecided	\N	There might be some minor issues, but I would need to investigate further to give a definitive answer.	439	0
1945	Affirmative	\N	Yes, indeed, we have robust alerting mechanisms in place for any data pipeline failures.	448	0
1946	Negative	\N	No, unfortunately, we do not have any alerting mechanisms in place for data pipeline failures at the moment.	448	0
2360	Negative	\N	No, we have not yet explored the use of a data science platform.	385	0
1947	Undecided	\N	There might be some alerting mechanisms in place, but I would need to confirm this.	448	0
1948	Affirmative	\N	Yes, absolutely, we do track and document data lineage.	449	0
1949	Negative	\N	No, unfortunately, we do not track or document data lineage at the moment.	449	0
1950	Undecided	\N	We do track some aspects of data lineage, but it's not a comprehensive process yet.	449	0
1951	Affirmative	\N	Yes, indeed, data lineage is exported from the data pipelines into the data catalogue.	450	0
1952	Negative	\N	No, unfortunately, data lineage is not currently exported from the data pipelines into the data catalogue.	450	0
1953	Undecided	\N	It's a bit of a mixed bag, some data lineage is exported from the data pipelines into the data catalogue, but not all.	450	0
1954	Affirmative	\N	Yes, indeed, we have robust data recovery strategies in place.	452	0
1955	Negative	\N	No, unfortunately, we have not yet implemented data recovery strategies.	452	0
1956	Undecided	\N	We have some data recovery measures in place, but we are still in the process of developing comprehensive strategies.	452	0
1957	Affirmative	\N	Yes, indeed, we have established processes for continuous improvement.	454	0
1958	Negative	\N	No, unfortunately, we have not yet implemented processes for continuous improvement.	454	0
1959	Undecided	\N	There are some processes in place, but we are still working on fully integrating continuous improvement into our operations.	454	0
1960	Affirmative	\N	Yes, indeed, we have comprehensive documentation of our data pipelines, workflows, and best practices.	455	0
1961	Negative	\N	No, unfortunately, we have not yet documented our data pipelines, workflows, and best practices.	455	0
1962	Undecided	\N	We have some documentation, but it does not cover all of our data pipelines, workflows, and best practices.	455	0
1963	Affirmative	\N	Yes, absolutely, these tools are effectively meeting our needs.	456	0
1964	Negative	\N	No, unfortunately, these tools are not effectively meeting our needs.	456	0
1965	Undecided	\N	Well, some of the tools are meeting our needs, but others are not as effective as we would like.	456	0
1966	Affirmative	\N	Yes, indeed, we do need to handle real-time or near-real-time data.	459	0
1967	Negative	\N	No, we do not require to handle real-time or near-real-time data.	459	0
1968	Undecided	\N	It's possible, but we're still assessing our data handling needs.	459	0
1969	Affirmative	\N	Yes, indeed, we have robust data access restrictions and security measures in place.	463	0
1970	Negative	\N	No, unfortunately, we have not implemented any data access restrictions or security measures yet.	463	0
1971	Undecided	\N	There are some data access restrictions and security measures in place, but we are still in the process of enhancing them.	463	0
1972	Affirmative	\N	Yes, indeed, we have a dedicated team of data analysts who are well-versed in data analytics.	466	0
1973	Negative	\N	No, unfortunately, we currently lack the necessary skills and resources in data analytics.	466	0
1974	Undecided	\N	There are some individuals with data analytics skills, but it's not widespread across the organisation.	466	0
1975	Affirmative	\N	Yes, absolutely, we do support the use of open source products.	470	0
1976	Negative	\N	No, unfortunately, we do not support the use of open source products.	470	0
1977	Undecided	\N	It's a bit of a mixed bag, we do use some open source products, but not extensively.	470	0
1978	Affirmative	\N	Yes, indeed, we have a comprehensive design document for the data lake.	471	0
1979	Negative	\N	No, unfortunately, we have not yet created a design document for the data lake.	471	0
1980	Undecided	\N	There might be a preliminary design document, but I need to confirm its existence and completeness.	471	0
1981	Affirmative	\N	Yes, indeed, there are always areas for improvement in our technology stack.	472	0
1982	Negative	\N	No, at the moment, our technology stack is quite robust and meets all our needs.	472	0
1983	Undecided	\N	There might be some, but we would need to conduct a thorough review to identify them.	472	0
1984	Affirmative	\N	Yes, indeed, we have thoroughly reviewed the core principles of data mesh, including domain-oriented ownership, product thinking, and self-serve data infrastructure.	476	0
1985	Negative	\N	No, we have not yet reviewed the core principles of data mesh such as domain-oriented ownership, product thinking, and self-serve data infrastructure.	476	0
1986	Undecided	\N	We have partially reviewed the core principles of data mesh. However, we still need to delve deeper into aspects such as domain-oriented ownership, product thinking, and self-serve data infrastructure.	476	0
1987	Affirmative	\N	Yes, indeed, the principles of data mesh perfectly align with our organisation's goals and culture.	479	0
1988	Negative	\N	No, unfortunately, the principles of data mesh do not align with our organisation's goals and culture.	479	0
1989	Undecided	\N	It's a bit of a mixed bag, some aspects of data mesh align with our organisation's goals and culture, but others do not.	479	0
1990	Affirmative	\N	Yes, absolutely, we are open to exploring new methodologies and technologies that could potentially enhance our data architecture.	480	0
1991	Negative	\N	No, at the moment, we are not considering conducting a data mesh pilot or proof of concept.	480	0
1992	Undecided	\N	We are currently in the process of evaluating various data architecture strategies, and a data mesh pilot could potentially be one of them.	480	0
1993	Affirmative	\N	Yes, indeed, we have several initiatives that require the ingestion of unstructured or semi-structured data.	481	0
1994	Negative	\N	No, at the moment, we do not have any initiatives that require the ingestion of unstructured or semi-structured data.	481	0
1995	Undecided	\N	There might be some initiatives that require the ingestion of unstructured or semi-structured data, but I would need to confirm this.	481	0
1996	Affirmative	\N	Yes, indeed, there are several strategic initiatives that could greatly benefit from accessing dark data.	485	0
1997	Negative	\N	No, at the moment, we do not have any strategic initiatives that could benefit from accessing dark data.	485	0
1998	Undecided	\N	Potentially, there might be some strategic initiatives that could benefit from accessing dark data, but we would need to investigate this further.	485	0
1999	Affirmative	\N	Yes, indeed, we are continuously exploring and analysing our dark data to uncover valuable insights.	486	0
2000	Negative	\N	No, unfortunately, we have not yet initiated any efforts to explore or analyse our dark data.	486	0
2001	Undecided	\N	There are some efforts in place, but it's not a consistent or comprehensive approach yet.	486	0
2002	Affirmative	\N	Yes, indeed, we do have a terminology server to centralise storage of reference data sets.	490	0
2003	Negative	\N	No, unfortunately, we do not have a terminology server for centralising storage of reference data sets.	490	0
2004	Undecided	\N	I'm not entirely sure, I would need to check if we have a terminology server for centralising storage of reference data sets.	490	0
2005	Affirmative	\N	Yes, indeed, we have a comprehensive inventory of all our data assets, including their location and sensitivity.	503	0
2006	Negative	\N	No, unfortunately, we do not have a complete inventory of all our data assets at this time.	503	0
2007	Undecided	\N	We have some information about our data assets, but it's not comprehensive and we're still working on it.	503	0
2008	Affirmative	\N	Yes, indeed, there are numerous opportunities for cost optimisation in data storage. For instance, we could consider cloud storage solutions, data deduplication, or tiered storage strategies.	505	0
2009	Negative	\N	No, at the moment, we have already optimised our data storage costs to the best of our abilities.	505	0
2010	Undecided	\N	Potentially, there might be some opportunities for cost optimisation in data storage, but we would need to conduct a thorough review of our current systems and strategies first.	505	0
2011	Affirmative	\N	Yes, indeed, we have both tools and teams specifically dedicated to analysing dark data.	506	0
2012	Negative	\N	No, unfortunately, we do not have any specific tools or teams dedicated to analysing dark data at the moment.	506	0
2013	Undecided	\N	We have some tools that can handle dark data, but we are still in the process of building a dedicated team for this task.	506	0
2014	Affirmative	\N	Yes, indeed, we are actively working on it.	508	0
2015	Negative	\N	No, there are currently no plans to align dark data with our organisational goals.	508	0
2016	Undecided	\N	It's under consideration, but no definitive plans have been made yet.	508	0
2017	Affirmative	\N	Yes, indeed, there are duplicate copies of ungoverned data in the organisation.	511	0
2018	Negative	\N	No, we have a strict policy against maintaining duplicate copies of ungoverned data.	511	0
2019	Undecided	\N	It's possible, but we would need to conduct a thorough audit to confirm.	511	0
2020	Affirmative	\N	Yes, indeed, we do have a data catalog in place.	512	0
2021	Negative	\N	No, unfortunately, we do not have a data catalog at the moment.	512	0
2022	Undecided	\N	There might be a data catalog, but I would need to confirm this.	512	0
2023	Affirmative	\N	Yes, indeed, our catalog includes metadata, data lineage, and data usage information.	513	0
2024	Negative	\N	No, unfortunately, our catalog does not include metadata, data lineage, and data usage information.	513	0
2025	Undecided	\N	The catalog includes some of these elements, but I need to verify if all of them are present.	513	0
2026	Affirmative	\N	Yes, indeed, our data catalog does support dynamic or auto discovery of data assets.	515	0
2027	Negative	\N	No, unfortunately, our data catalog does not support dynamic or auto discovery of data assets.	515	0
2028	Undecided	\N	It's a bit of a mixed bag, our data catalog does support some level of dynamic or auto discovery of data assets, but it's not fully automated.	515	0
2029	Affirmative	\N	Yes, indeed, our data catalog does govern NoSQL and event driven messages or schema.	517	0
2030	Negative	\N	No, unfortunately, our data catalog does not govern NoSQL and event driven messages or schema.	517	0
2031	Undecided	\N	It's a bit of a mixed bag, our data catalog governs some aspects of NoSQL and event driven messages or schema, but not all.	517	0
2032	Affirmative	\N	Yes, indeed, our data catalog does support tagging data attributes as PII or sensitive data fields.	518	0
2033	Negative	\N	No, unfortunately, our data catalog does not currently support tagging data attributes as PII or sensitive data fields.	518	0
2034	Undecided	\N	I'm not entirely sure, I would need to check whether our data catalog supports tagging data attributes as PII or sensitive data fields.	518	0
2035	Affirmative	\N	Yes, indeed, we have a well-established data governance program and a published charter.	519	0
2036	Negative	\N	No, unfortunately, we have not yet established a data governance program or published a charter.	519	0
2037	Undecided	\N	We have some elements of a data governance program in place, but we are still in the process of formalising and publishing a comprehensive charter.	519	0
2038	Affirmative	\N	Yes, indeed, our CxO level executives are fully supportive of the data governance program.	521	0
2039	Negative	\N	No, unfortunately, we do not have CxO level sponsorship for the data governance program at the moment.	521	0
2040	Undecided	\N	There is some interest at the CxO level, but full sponsorship for the data governance program has not been confirmed yet.	521	0
2041	Affirmative	\N	Yes, indeed, data domain, data ownership and stewardship roles are clearly defined and communicated in the charter.	522	0
2042	Negative	\N	No, unfortunately, the data domain, data ownership and stewardship roles have not been defined or communicated in the charter yet.	522	0
2043	Undecided	\N	Some aspects of data domain and ownership have been defined, but stewardship roles are still under discussion.	522	0
2044	Affirmative	\N	Yes, indeed. We have a comprehensive training programme in place to ensure all employees are well-versed in data governance.	525	0
2045	Negative	\N	No, unfortunately, we have not yet implemented a training programme for data governance awareness.	525	0
2046	Undecided	\N	There is some level of awareness, but we are still in the process of developing a comprehensive training programme.	525	0
2047	Affirmative	\N	Yes, indeed, there is a clear alignment of business data owners within the line of business responsible for data assets within our organisation.	526	0
2048	Negative	\N	No, unfortunately, there isn't a clear alignment of business data owners within the line of business responsible for data assets within our organisation.	526	0
2049	Undecided	\N	There is some alignment of business data owners within the line of business responsible for data assets, but it's not entirely clear and needs further clarification.	526	0
2477	Dedicated Team	Dedicated team	A dedicated team typically tests our ML models.	713	10
2050	Affirmative	\N	Yes, absolutely, we have a strong culture of data governance and data stewardship within our organisation.	527	0
2051	Negative	\N	No, unfortunately, we have not yet established a culture of data governance and data stewardship within our organisation.	527	0
2052	Undecided	\N	There are some elements of data governance and data stewardship present, but it's not yet fully ingrained in our organisation's culture.	527	0
2053	Affirmative	\N	Yes, indeed, we have undergone several external audits and assessments of our data governance practices.	529	0
2054	Negative	\N	No, we have not yet had any external audits or assessments of our data governance practices.	529	0
2055	Undecided	\N	There have been some discussions about it, but I am not certain if any external audits or assessments have been conducted.	529	0
2056	Affirmative	\N	Yes, indeed, there are certain areas that require improvement.	533	0
2057	Negative	\N	No, at the moment, all areas are performing optimally.	533	0
2058	Undecided	\N	There might be, but we would need to conduct a thorough review to identify them.	533	0
2059	Affirmative	\N	Yes, indeed, we have comprehensive documentation of our data governance policies, procedures, and standards.	534	0
2060	Negative	\N	No, unfortunately, we have not yet fully documented our data governance policies, procedures, and standards.	534	0
2061	Undecided	\N	We have some documentation, but it's not comprehensive. We're still in the process of documenting our data governance policies, procedures, and standards.	534	0
2062	Affirmative	\N	Yes, absolutely, these tools have proven to be very effective in supporting our data governance efforts.	536	0
2063	Negative	\N	No, unfortunately, these tools have not been effective in supporting our data governance efforts.	536	0
2064	Undecided	\N	It's a bit of a mixed bag, some tools have been effective while others have not.	536	0
2065	Affirmative	\N	Yes, absolutely, our data governance workflows are thoroughly documented and strictly adhered to.	538	0
2066	Negative	\N	No, unfortunately, we have not yet documented our data governance workflows.	538	0
2067	Undecided	\N	Some of our data governance workflows are documented and followed, but we are still in the process of improving this area.	538	0
2068	Affirmative	\N	Yes, indeed, we have ongoing data governance education and awareness programs.	541	0
2069	Negative	\N	No, unfortunately, we do not have ongoing data governance education and awareness programs at the moment.	541	0
2070	Undecided	\N	There are some data governance education initiatives, but I'm not sure if they can be classified as ongoing programs.	541	0
2071	Affirmative	\N	Yes, indeed, all employees are required to undergo annual training on data governance best practices.	542	0
2072	Negative	\N	No, unfortunately, we do not currently provide mandatory yearly training on data governance best practices.	542	0
2073	Undecided	\N	Some departments do provide yearly training on data governance, but it's not a company-wide policy yet.	542	0
2074	Affirmative	\N	Yes, we have a comprehensive data governance roadmap in place, outlining our plans for future improvements.	543	0
2075	Negative	\N	No, we do not currently have a data governance roadmap or plan for future improvements.	543	0
2076	Undecided	\N	We have some initial thoughts on a data governance roadmap, but it's not fully developed yet.	543	0
2077	Affirmative	\N	Yes, indeed, we have established processes for managing data from external sources and partners.	545	0
2078	Negative	\N	No, unfortunately, we do not have processes in place for managing data from external sources or partners.	545	0
2079	Undecided	\N	We have some processes in place for managing data from external sources, but it's not comprehensive and we are still working on it.	545	0
2080	Affirmative	\N	Yes, we have a robust DataOps framework in place for managing and governing our data assets throughout their lifecycle.	546	0
2081	Negative	\N	No, we do not currently have a DataOps framework for managing and governing our data assets.	546	0
2082	Undecided	\N	We have some elements of a DataOps framework in place, but it's not fully comprehensive yet.	546	0
2083	Affirmative	\N	Yes, indeed, we have established data disposal procedures.	549	0
2084	Negative	\N	No, we have not yet implemented any data disposal procedures.	549	0
2085	Undecided	\N	There might be some data disposal procedures in place, but I need to confirm this.	549	0
2086	Affirmative	\N	Yes, indeed, we have a conceptual, logical, and physical data model for the entire organisation.	554	0
2087	Negative	\N	No, unfortunately, we only have data models for a few selected data domains.	554	0
2088	Undecided	\N	We have data models for some data domains, but I'm not certain if it covers the entire organisation.	554	0
2089	Affirmative	\N	Yes, indeed, we do have a strict naming convention that is enforced.	555	0
2090	Negative	\N	No, unfortunately, we do not have a naming convention that is enforced.	555	0
2091	Undecided	\N	There might be a naming convention, but I am not entirely sure if it is enforced.	555	0
2092	Affirmative	\N	Yes, indeed, we do have a data dictionary for our data models.	556	0
2093	Negative	\N	No, unfortunately, we do not have a data dictionary for our data models at the moment.	556	0
2094	Undecided	\N	There might be a data dictionary for some of our data models, but I would need to check to be certain.	556	0
2095	Affirmative	\N	Yes, indeed, we have enough read licenses for all viewers to access the data models.	558	0
2096	Negative	\N	No, unfortunately, we are currently facing a shortage of read licenses for viewers to view the data models.	558	0
2097	Undecided	\N	We have some read licenses available, but I'm not entirely sure if it's sufficient for all viewers to view the data models.	558	0
2098	Affirmative	\N	Yes, graph data modelling is indeed relevant to our organisation. Our data modellers have received adequate training and are fully equipped to model knowledge graphs.	560	0
2099	Negative	\N	No, at present, graph data modelling is not relevant to our organisation. Consequently, our data modellers have not undergone training for modelling knowledge graphs.	560	0
2100	Undecided	\N	Graph data modelling could potentially be relevant to our organisation, but we are still in the process of determining this. As for our data modellers, they have some training in this area, but we are looking into further development opportunities.	560	0
2101	Affirmative	\N	Yes, our data modellers are well-versed in using data vault and have undergone extensive training to model data using this method.	561	0
2102	Negative	\N	No, our data modellers have not yet explored the use of data vault, nor have they been trained to model data using this method.	561	0
2103	Undecided	\N	Some of our data modellers have explored the use of data vault, but not all have been trained to model data using this method.	561	0
2104	Affirmative	\N	Yes, our data modellers are indeed trained to identify PII data attributes in the data models.	562	0
2105	Negative	\N	No, unfortunately, our data modellers have not received specific training to identify PII data attributes in the data models.	562	0
2106	Undecided	\N	Some of our data modellers have been trained to identify PII data attributes in the data models, but not all of them.	562	0
2107	Affirmative	\N	Yes, our data modellers utilise a specific tool to generate the physical data models and DML.	563	0
2108	Negative	\N	No, our data modellers do not use a tool for generating the physical data models or DML.	563	0
2109	Undecided	\N	Some of our data modellers use a tool for this purpose, while others prefer to generate the physical data models and DML manually.	563	0
2110	Affirmative	\N	Yes, indeed, data modellers often model messages/events for publication on an event stream like Kafka.	564	0
2111	Negative	\N	No, data modellers do not typically model messages/events for an event stream such as Kafka.	564	0
2112	Undecided	\N	It can vary, some data modellers might model messages/events for an event stream like Kafka, while others might not.	564	0
2113	Affirmative	\N	Yes, indeed, we have robust data validation and cleansing processes in place.	574	0
2114	Negative	\N	No, unfortunately, we have not yet implemented data validation and cleansing processes.	574	0
2115	Undecided	\N	There are some data validation and cleansing processes, but they are not comprehensive.	574	0
2116	Affirmative	\N	Yes, indeed, we have a robust Audit, Balance & Control Framework in place.	575	0
2117	Negative	\N	No, unfortunately, we have not yet established an Audit, Balance & Control Framework.	575	0
2118	Undecided	\N	We have some elements of an Audit, Balance & Control Framework, but it's not fully developed yet.	575	0
2119	Affirmative	\N	Yes, indeed, we have clearly defined and enforced data quality standards and guidelines.	576	0
2120	Negative	\N	No, unfortunately, we have not yet defined or enforced data quality standards and guidelines.	576	0
2121	Undecided	\N	Some data quality standards and guidelines have been defined, but enforcement is still a work in progress.	576	0
2122	Affirmative	\N	Yes, we have conducted data profiling exercises to understand the characteristics of our data.	578	0
2123	Negative	\N	No, we have not conducted any data profiling exercises yet.	578	0
2124	Undecided	\N	We have conducted some data profiling exercises, but we need to do more to fully understand the characteristics of our data.	578	0
2125	Affirmative	\N	Yes, we have established data quality standards and guidelines.	582	0
2126	Negative	\N	No, we have not established data quality standards and guidelines yet.	582	0
2127	Undecided	\N	We have established some data quality standards and guidelines, but we are still in the process of refining them.	582	0
2128	Affirmative	\N	Yes, indeed, we have robust data validation processes in place to catch errors at the point of entry.	583	0
2129	Negative	\N	No, unfortunately, we do not have data validation processes in place at the moment.	583	0
2130	Undecided	\N	We have some data validation processes, but they might not cover all potential errors at the point of entry.	583	0
2131	Affirmative	\N	Yes, absolutely, these tools are highly effective in addressing data quality issues.	586	0
2132	Negative	\N	No, unfortunately, these tools are not effective in addressing data quality issues.	586	0
2133	Undecided	\N	It's hard to say, the effectiveness of these tools in addressing data quality issues can vary.	586	0
2134	Affirmative	\N	Yes, absolutely. The responsibilities for data quality are clearly defined and assigned.	590	0
2135	Negative	\N	No, unfortunately, the responsibilities for data quality have not been clearly defined yet.	590	0
2136	Undecided	\N	Well, some roles and responsibilities related to data quality have been defined, but there's still some ambiguity.	590	0
2137	Affirmative	\N	Yes, indeed, we have both automated tests and manual checks in place.	592	0
2138	Negative	\N	No, unfortunately, we do not have any automated tests or manual checks in place at the moment.	592	0
2139	Undecided	\N	There are some automated tests in place, but manual checks are not consistently performed.	592	0
2140	Affirmative	\N	Yes, we have a robust system in place for real-time and batch data quality monitoring.	595	0
2141	Negative	\N	No, we do not currently have real-time or batch data quality monitoring in place.	595	0
2142	Undecided	\N	We have some measures in place for data quality monitoring, but it's not comprehensive and does not cover all real-time and batch data.	595	0
2143	Affirmative	\N	Yes, we have implemented several initiatives to address data quality challenges.	597	0
2144	Negative	\N	No, we have not yet implemented specific initiatives to address data quality challenges.	597	0
2145	Undecided	\N	We have started some initiatives, but it's still a work in progress to fully address data quality challenges.	597	0
2146	Affirmative	\N	Yes, we do have data quality dashboards and reports.	600	0
2147	Negative	\N	No, we do not have data quality dashboards or reports at the moment.	600	0
2148	Undecided	\N	We have some basic reports, but we are still in the process of developing comprehensive data quality dashboards.	600	0
2149	Affirmative	\N	Yes, indeed, there are certain areas where we need to focus on improving data quality.	602	0
2150	Negative	\N	No, at the moment, we believe our data quality is up to the mark across all areas.	602	0
2151	Undecided	\N	There might be some areas that require attention, but we need to conduct a thorough data quality assessment first.	602	0
2152	Affirmative	\N	Yes, indeed, there are critical data quality issues that need immediate attention.	604	0
2153	Negative	\N	No, currently, we do not have any critical data quality issues.	604	0
2154	Undecided	\N	There might be some data quality issues, but we need to conduct a thorough analysis to confirm.	604	0
2155	Affirmative	\N	Yes, indeed. We have robust policies and procedures in place to ensure data privacy, including compliance with GDPR, HIPAA and other relevant regulations.	566	0
2156	Negative	\N	No, unfortunately, we are still in the process of developing comprehensive policies and procedures for data privacy.	566	0
2157	Undecided	\N	We have some policies in place to ensure data privacy, but we are still working on fully aligning with GDPR, HIPAA and other regulations.	566	0
2158	Affirmative	\N	Yes, we do use tokenization tools to tokenize PII data fields.	568	0
2159	Negative	\N	No, we do not use any tokenization tools to tokenize PII data fields.	568	0
2160	Undecided	\N	We are currently exploring the use of tokenization tools for PII data fields, but have not fully implemented them yet.	568	0
2161	Affirmative	\N	Yes, indeed, consent across multiple LOBs is stored in a central repository and exposed as an API.	571	0
2162	Negative	\N	No, consent across multiple LOBs is not currently stored in a central repository nor exposed as an API.	571	0
2163	Undecided	\N	It's possible that some consent across multiple LOBs is stored in a central repository and exposed as an API, but I would need to confirm this.	571	0
2164	Affirmative	\N	Yes, indeed. We are bound by specific industry regulations and legal requirements that significantly influence our data strategy.	608	0
2165	Negative	\N	No, there are no specific industry regulations or legal requirements that impact our data strategy.	608	0
2166	Undecided	\N	There might be some industry regulations or legal requirements that impact our data strategy, but I would need to confirm this.	608	0
2167	Affirmative	\N	Yes, absolutely, we are fully compliant with all relevant data regulations, including GDPR.	609	0
2168	Negative	\N	No, unfortunately, we are not yet fully compliant with all relevant data regulations such as GDPR.	609	0
2169	Undecided	\N	We are in the process of becoming compliant with all relevant data regulations, including GDPR, but it's a work in progress.	609	0
2170	Affirmative	\N	Yes, we do have a comprehensive disaster recovery plan in place for data.	612	0
2171	Negative	\N	No, we have not yet established a disaster recovery plan for data.	612	0
2172	Undecided	\N	We have some measures in place, but we are still in the process of developing a comprehensive disaster recovery plan for data.	612	0
2173	Affirmative	\N	Yes, absolutely. Our data access permissions are meticulously aligned with both business needs and regulatory requirements.	613	0
2174	Negative	\N	No, unfortunately, our data access permissions are not yet fully aligned with business needs and regulations.	613	0
2175	Undecided	\N	Partially, some of our data access permissions are aligned with business needs and regulations, but there's still work to be done.	613	0
2176	Affirmative	\N	Yes, we do use our own keystore for managing keys stored on the cloud.	618	0
2177	Negative	\N	No, we do not use our own keystore for managing keys stored on the cloud.	618	0
2178	Undecided	\N	We are currently in the process of evaluating whether to use our own keystore for managing keys stored on the cloud.	618	0
2179	Affirmative	\N	Yes, indeed, we are always open to collaboration with other organisations to enhance the value of our data.	619	0
2180	Negative	\N	No, currently we are not considering collaborations with other organisations for data enhancement.	619	0
2181	Undecided	\N	Possibly, we are exploring various avenues to enhance the value of our data, collaboration could be one of them.	619	0
2182	Affirmative	\N	Yes, we certainly have the capability to tap into industry data ecosystems or consortiums.	620	0
2183	Negative	\N	No, unfortunately, we do not have the ability to tap into industry data ecosystems or consortiums at this time.	620	0
2184	Undecided	\N	We are currently exploring the possibility of tapping into industry data ecosystems or consortiums, but a final decision has not yet been made.	620	0
2185	Affirmative	\N	Yes, indeed, we have a well-defined Role Based Access Control policy in place, and the roles are aligned with AD groups.	621	0
2186	Negative	\N	No, unfortunately, we do not have a well-defined Role Based Access Control policy in place with roles aligned to AD groups.	621	0
2187	Undecided	\N	We have some elements of a Role Based Access Control policy in place, but it's not fully aligned with AD groups yet.	621	0
2188	Affirmative	\N	Yes, indeed, we have a well-defined process for adding users to the AD groups.	622	0
2189	Negative	\N	No, unfortunately, we do not have a well-defined process for adding users to the AD groups.	622	0
2190	Undecided	\N	There is a process, but it could be more clearly defined and streamlined.	622	0
2191	Affirmative	\N	Yes, indeed, we do have policies that utilise attribute-based access control for row-based filtering.	623	0
2192	Negative	\N	No, unfortunately, we do not have any policies that use attribute-based access control for row-based filtering.	623	0
2193	Undecided	\N	We might have some policies that use attribute-based access control for row-based filtering, but I would need to confirm this.	623	0
2194	Affirmative	\N	Yes, we have a well-defined process and have identified the necessary tools for generating synthetic data.	628	0
2195	Negative	\N	No, we have not yet defined a process or identified tools for generating synthetic data.	628	0
2196	Undecided	\N	We have started to define a process, but we are still in the process of identifying the appropriate tools for generating synthetic data.	628	0
2197	Affirmative	\N	Yes, there are indeed certain legal challenges that could potentially hinder the sharing of data internally among the lines of business.	629	0
2198	Negative	\N	No, we are not aware of any legal challenges that would prohibit sharing data internally among the lines of business.	629	0
2199	Undecided	\N	There might be some legal challenges, but we would need to conduct a thorough review to confirm.	629	0
2200	Affirmative	\N	Yes, absolutely, we ensure the secure transfer of model weights and configurations between all environments.	631	0
2201	Negative	\N	No, unfortunately, we have not implemented such measures yet.	631	0
2202	Undecided	\N	We do secure some aspects, but not all. We are still working on improving our data security measures.	631	0
2203	Affirmative	\N	Yes, indeed, we do encrypt the model weights and parameters.	634	0
2204	Negative	\N	No, we do not currently encrypt the model weights and parameters.	634	0
2205	Undecided	\N	We are in the process of considering whether to encrypt the model weights and parameters.	634	0
2206	Affirmative	\N	Yes, indeed, we do implement regular key rotation procedures to minimise the risk associated with long-lived encryption keys.	635	0
2207	Negative	\N	No, unfortunately, we have not yet implemented regular key rotation procedures.	635	0
2208	Undecided	\N	We are in the process of implementing regular key rotation procedures, but it's not fully operational yet.	635	0
2209	Affirmative	\N	Yes, indeed, we have dedicated DataOps teams working on various projects within the organisation.	639	0
2210	Negative	\N	No, at the moment, we do not have any dedicated DataOps teams or roles within the organisation.	639	0
2211	Undecided	\N	There might be some individuals or teams working on DataOps, but I would need to confirm to give a definitive answer.	639	0
2212	Affirmative	\N	Yes, indeed, there are always areas that could benefit from improvement.	644	0
2213	Negative	\N	No, at the moment, all areas are performing optimally.	644	0
2214	Undecided	\N	Possibly, we would need to conduct a thorough review to identify any areas that may need improvement.	644	0
2215	Affirmative	\N	Yes, indeed, we have a detailed roadmap for DevOps/DataOps improvements.	646	0
2216	Negative	\N	No, unfortunately, we do not have a roadmap for DevOps/DataOps improvements at the moment.	646	0
2217	Undecided	\N	We have some plans in place, but a comprehensive roadmap for DevOps/DataOps improvements is still in the works.	646	0
2218	Affirmative	\N	Yes, absolutely, these tools are effectively meeting our needs.	648	0
2219	Negative	\N	No, unfortunately, these tools are not meeting our needs effectively.	648	0
2220	Undecided	\N	Well, some of the tools are meeting our needs, but others are not as effective as we would like.	648	0
2221	Affirmative	\N	Yes, we have a well-defined process for promoting changes from development to production.	652	0
2222	Negative	\N	No, we do not have any processes in place for promoting changes from development to production.	652	0
2223	Undecided	\N	We have some processes in place, but they are not fully established or consistent.	652	0
2224	Affirmative	\N	Yes, absolutely. Our DevOps/DataOps teams are built around a culture of collaboration and automation.	654	0
2225	Negative	\N	No, unfortunately, we are still working on fostering a culture of collaboration and automation within our DevOps/DataOps teams.	654	0
2226	Undecided	\N	There is some level of collaboration and automation, but it's not as pervasive as we would like it to be.	654	0
2227	Affirmative	\N	Yes, indeed, our organisation has a comprehensive cloud infrastructure strategy that supports workloads federated over on-premise and multiple cloud service providers.	657	0
2228	Negative	\N	No, unfortunately, our organisation does not yet have a comprehensive cloud infrastructure strategy to support workloads federated over on-premise and multiple cloud service providers.	657	0
2229	Undecided	\N	We are in the process of developing a comprehensive cloud infrastructure strategy to support workloads federified over on-premise and multiple cloud service providers, but it's not fully implemented yet.	657	0
2230	Affirmative	\N	Yes, indeed, we have a private cloud in place.	659	0
2231	Negative	\N	No, at the moment, we do not have a private cloud nor plans to introduce one.	659	0
2232	Undecided	\N	There have been discussions about introducing a private cloud, but no final decision has been made yet.	659	0
2233	Affirmative	\N	Yes, our data infrastructure is designed to scale and handle growing data volumes.	660	0
2234	Negative	\N	No, at the moment our data infrastructure is not scalable to handle growing data volumes.	660	0
2235	Undecided	\N	We are in the process of evaluating the scalability of our data infrastructure to handle growing data volumes.	660	0
2236	Affirmative	\N	Yes, indeed, our organisation is fully committed to a cost-effective strategy of utilising serverless computing.	661	0
2237	Negative	\N	No, at the moment, our organisation does not support a cost-effective strategy of utilising serverless computing.	661	0
2238	Undecided	\N	We are currently exploring the potential benefits and drawbacks of a cost-effective strategy of utilising serverless computing, but have not yet made a final decision.	661	0
2239	Affirmative	\N	Yes, indeed, we do have an on-premises object storage server.	663	0
2240	Negative	\N	No, unfortunately, we do not have an on-premises object storage server.	663	0
2241	Undecided	\N	I'm not entirely sure, I would need to check on the presence of an on-premises object storage server.	663	0
2242	Affirmative	\N	Yes, indeed, there are a few performance bottlenecks that we are currently addressing.	664	0
2243	Negative	\N	No, at the moment, we are not aware of any performance bottlenecks.	664	0
2244	Undecided	\N	There might be some, but we are still in the process of identifying potential performance bottlenecks.	664	0
2245	Affirmative	\N	Yes, indeed, we have robust backup and disaster recovery strategies in place for our data infrastructure.	669	0
2246	Negative	\N	No, unfortunately, we have not yet implemented backup and disaster recovery strategies for our data infrastructure.	669	0
2247	Undecided	\N	We have some measures in place, but we are still in the process of developing comprehensive backup and disaster recovery strategies for our data infrastructure.	669	0
2248	Affirmative	\N	Yes, indeed, we do deploy ML models in containers such as Docker.	671	0
2249	Negative	\N	No, we do not deploy ML models in containers like Docker.	671	0
2250	Undecided	\N	We are currently exploring the possibility of deploying ML models in containers like Docker, but have not made a final decision yet.	671	0
2251	Affirmative	\N	Yes, we do utilise GPU clusters and FPGA's for our analytics.	672	0
2252	Negative	\N	No, we do not use any specialised hardware for our analytics.	672	0
2253	Undecided	\N	We are currently exploring the use of GPU clusters and FPGA's for our analytics, but have not fully implemented them yet.	672	0
2254	Affirmative	\N	Yes, indeed, we do have analytics use cases that require SSD.	674	0
2255	Negative	\N	No, at the moment, we do not have any analytics use cases that require SSD.	674	0
2256	Undecided	\N	Possibly, we might have some analytics use cases that could benefit from SSD, but we need to investigate further.	674	0
2257	Affirmative	\N	Yes, indeed, we do have analytics use cases that require VMs with large amounts of memory.	675	0
2258	Negative	\N	No, at the moment, we do not have any analytics use cases that require excessively large amounts of memory.	675	0
2259	Undecided	\N	We might have some analytics use cases that could benefit from VMs with large amounts of memory, but we need to further investigate this.	675	0
2260	Affirmative	\N	Yes, indeed, all data assets, whether on-premises or in the cloud, are integrated with our CMDB or Software Asset Management tool.	678	0
2261	Negative	\N	No, unfortunately, not all data assets are integrated with our CMDB or Software Asset Management tool.	678	0
2262	Undecided	\N	Some of our data assets are integrated with our CMDB or Software Asset Management tool, but I'm not certain about all of them.	678	0
2263	Affirmative	\N	Yes, indeed. We use a tagging policy to track and analyse costs associated with data assets or analytics on the cloud. We also have a dedicated team that constantly monitors and optimises these costs.	679	0
2264	Negative	\N	No, unfortunately, we do not currently have a system in place to track, analyse, or optimise costs associated with data assets or analytics on the cloud. We also do not use a tagging policy.	679	0
2265	Undecided	\N	We do have some measures in place to track and analyse costs associated with data assets or analytics on the cloud, but it's not comprehensive and we are still working on optimisation. As for the tagging policy, it's under consideration.	679	0
2266	Affirmative	\N	Yes, indeed, we have the necessary technology infrastructure in place to support data monetization efforts.	683	0
2267	Negative	\N	No, unfortunately, we do not currently have the necessary technology infrastructure to support data monetization efforts.	683	0
2268	Undecided	\N	We have some of the necessary technology infrastructure, but we are still in the process of developing and implementing others.	683	0
2269	Affirmative	\N	Yes, indeed, many analytical projects often require additional infrastructure.	684	0
2270	Negative	\N	No, not all analytical projects frequently need to add infrastructure.	684	0
2271	Undecided	\N	It varies, some analytical projects may need to add infrastructure frequently, while others may not.	684	0
2273	Negative	\N	No, at the moment, we do not have a plan to rationalise our reporting tools.	685	0
2275	Affirmative	\N	Yes, indeed, we have a well-defined semantic layer within our reporting tool.	686	0
2276	Negative	\N	No, unfortunately, we have not yet defined a semantic layer within our reporting tool.	686	0
2277	Undecided	\N	There might be a semantic layer, but I would need to confirm this.	686	0
2278	Affirmative	\N	Yes, indeed, we have established SLAs for all our reports.	689	0
2279	Negative	\N	No, unfortunately, we have not set up any SLAs for our reports yet.	689	0
2280	Undecided	\N	There might be some SLAs in place for certain reports, but I would need to check to be certain.	689	0
2281	Affirmative	\N	Yes, our scheduled reports do include visualisations such as graphs and charts, in addition to tabular data.	691	0
2282	Negative	\N	No, our scheduled reports are currently only presented in tabular format.	691	0
2283	Undecided	\N	Some of our reports do include visualisations, but not all. It largely depends on the specific report and its intended audience.	691	0
2284	Affirmative	\N	Yes, indeed, dashboards are preferred as they provide real-time data and are more interactive.	695	0
2285	Negative	\N	No, scheduled reports are still favoured as they provide a more detailed and comprehensive view of the data.	695	0
2286	Undecided	\N	It varies, some departments prefer dashboards for their immediacy, while others prefer scheduled reports for their depth of information.	695	0
2287	Affirmative	\N	Yes, indeed, some of our reports are currently outsourced to third parties. However, we are actively considering bringing that reporting in-house.	696	0
2288	Negative	\N	No, we do not outsource any of our reports to third parties. All our reporting is done in-house.	696	0
2289	Undecided	\N	Some of our reports are outsourced, but we haven't made a decision yet about bringing that reporting in-house.	696	0
2291	Negative	\N	No, there is currently no plan to consolidate reporting.	697	0
2293	Affirmative	\N	Yes, our reporting server is highly available. It operates on an active/active configuration and the active server is deployed in the European region.	699	0
2294	Negative	\N	No, unfortunately, our reporting server is not highly available. It operates on an active/passive configuration and the active server is deployed in the Asian region.	699	0
2295	Undecided	\N	Our reporting server is somewhat available. It operates on a mix of active/active and active/passive configurations. As for the region of the active server, I would need to check that information.	699	0
2296	Affirmative	\N	Yes, indeed, we do have a DR environment for the reporting server.	701	0
2297	Negative	\N	No, unfortunately, we do not have a DR environment for the reporting server.	701	0
2298	Undecided	\N	I'm not entirely sure, I would need to check on the existence of a DR environment for the reporting server.	701	0
2299	Affirmative	\N	Yes, absolutely. All reports containing sensitive data are encrypted before being emailed to end users.	704	0
2300	Negative	\N	No, unfortunately, we have not implemented encryption for emailed reports yet.	704	0
2301	Undecided	\N	Some reports are encrypted, but it's not a standard practice for all of them.	704	0
2302	Affirmative	\N	Yes, indeed, users have the ability to run their own queries against the data and generate reports.	705	0
2303	Negative	\N	No, unfortunately, users do not have the option to run their own queries or generate self-service reports.	705	0
2304	Undecided	\N	It's a bit of a mixed bag, some users have the ability to run their own queries and generate reports, but not all.	705	0
2305	Affirmative	\N	Yes, indeed. Our business has the capability to generate reports independently, without the need for IT involvement. There is also a strong desire for self-service reporting.	707	0
2306	Negative	\N	No, currently our business relies on IT for report generation. There is no significant push for self-service reporting at the moment.	707	0
2307	Undecided	\N	There is some capacity for independent report generation, but it's not widespread. The desire for self-service reporting varies across different departments.	707	0
2274	Undecided	\N	There might be a plan in the works, but I am not entirely sure at the moment.	685	3
2290	Affirmative	\N	Yes, indeed, there is a plan to consolidate reporting.	697	6
2292	Undecided	\N	There might be a plan, but I am not entirely sure at the moment.	697	3
2308	Affirmative	\N	Yes, indeed, there is a strong interest in using conversational AI to query data.	708	0
2309	Negative	\N	No, at the moment, there is no interest in using conversational AI to query data.	708	0
2310	Undecided	\N	There might be some interest, but it's not entirely clear at this point.	708	0
2311	Affirmative	\N	Yes, indeed, we are planning to increase the number of dashboards and reports to become a more data-driven organisation.	709	0
2312	Negative	\N	No, at the moment, there are no plans to increase the number of dashboards or reports.	709	0
2313	Undecided	\N	It's under consideration, but we haven't made a final decision yet.	709	0
2314	Affirmative	\N	Yes, absolutely. We believe that testing AI models, including ML and LLM models, is just as crucial as software testing.	714	0
2315	Negative	\N	No, unfortunately, we do not test AI models with the same intensity as we do for software testing.	714	0
2316	Undecided	\N	We do test AI models, but I'm not entirely sure if it's with the same rigour as our software testing.	714	0
2317	Affirmative	\N	Yes, indeed. Our team is responsible for creating test plans and performing various types of testing including unit testing, functional testing, performance testing, UAT, and A/B testing.	715	0
2318	Negative	\N	No, unfortunately, our team does not currently create test plans or perform any of the mentioned types of testing.	715	0
2319	Undecided	\N	We do some of these tests, but not all. For instance, we perform unit testing and functional testing, but we have not yet implemented performance testing, UAT, or A/B testing.	715	0
2320	Affirmative	\N	Yes, indeed, we do test our ML models for bias and drift.	716	0
2321	Negative	\N	No, we have not yet started testing our ML models for bias and drift.	716	0
2322	Undecided	\N	We are in the process of implementing such tests, but it's not fully operational yet.	716	0
2323	Affirmative	\N	Yes, indeed, we do implement continuous monitoring of our ML model in production to ensure it maintains its performance over time.	717	0
2324	Negative	\N	No, unfortunately, we do not currently implement continuous monitoring of our ML model in production.	717	0
2325	Undecided	\N	We are in the process of implementing continuous monitoring for our ML model in production, but it's not fully operational yet.	717	0
2326	Affirmative	\N	Yes, indeed, we do perform benchmarking of the ML model performance.	718	0
2327	Negative	\N	No, we have not started benchmarking the ML model performance yet.	718	0
2328	Undecided	\N	We do some benchmarking, but it's not a consistent or formalised process.	718	0
2329	Affirmative	\N	Yes, absolutely. We regularly compute the performance metrics of our models and present them to the analytics team.	719	0
2330	Negative	\N	No, we do not currently compute the performance metrics of our models nor present them to the analytics team.	719	0
2331	Undecided	\N	We do compute some performance metrics, but we are still working on a comprehensive presentation for the analytics team.	719	0
2332	Affirmative	\N	Yes, we do bring PII data from PROD for testing, but it is always anonymised to ensure privacy.	720	0
2333	Negative	\N	No, we do not use any PII data from PROD for testing. We strictly adhere to privacy and data protection regulations.	720	0
2334	Undecided	\N	Sometimes, we might use PII data from PROD for testing, but it is always anonymised and used in compliance with data protection regulations.	720	0
2335	Affirmative	\N	Yes, our team does use synthetic data. We generate it using a variety of methods, including data augmentation techniques and generative models.	723	0
2336	Negative	\N	No, our team does not currently use synthetic data. However, we would be interested in learning more about test data generation for ML models.	723	0
2337	Undecided	\N	We have not yet decided whether to use synthetic data or not. We are open to exploring the possibilities of test data generation for ML models.	723	0
2338	Affirmative	\N	Yes, indeed, our team regularly tests the ML models against adversarial attacks.	725	0
2339	Negative	\N	No, unfortunately, we have not yet started testing our ML models against adversarial attacks.	725	0
2340	Undecided	\N	We have started to consider it, but we have not fully implemented testing against adversarial attacks yet.	725	0
2341	Affirmative	\N	Yes, indeed, our team rigorously tests the model's resilience against data poisoning attacks.	726	0
2342	Negative	\N	No, unfortunately, we have not yet implemented testing for data poisoning attacks.	726	0
2343	Undecided	\N	We have started to consider it, but we haven't fully implemented tests against data poisoning attacks yet.	726	0
2344	Affirmative	\N	Yes, indeed, our data scientists are able to collaborate and share ML models with ease.	376	0
2345	Negative	\N	No, unfortunately, our data scientists are currently facing challenges in collaborating and sharing ML models.	376	0
2346	Undecided	\N	It varies, some of our data scientists are able to collaborate and share ML models easily, while others are still facing some difficulties.	376	0
2347	Affirmative	\N	Yes, indeed, we do expose our model through APIs.	377	0
2348	Negative	\N	No, we do not currently expose our model through APIs.	377	0
2349	Undecided	\N	We are in the process of considering whether to expose our model through APIs.	377	0
2350	Affirmative	\N	Yes, indeed, we do serialize the model, including its architecture and weights, into a single binary file for interoperability.	378	0
2351	Negative	\N	No, we do not serialize the model into a single binary file. We have a different approach.	378	0
2352	Undecided	\N	We do serialize some aspects of the model, but I'm not entirely sure if it includes both the architecture and weights.	378	0
2353	Affirmative	\N	Yes, indeed, we utilise AutoML to automate model selection and hyperparameter tuning.	380	0
2354	Negative	\N	No, we have not implemented AutoML for automating model selection and hyperparameter tuning yet.	380	0
2355	Undecided	\N	We are currently exploring the potential of AutoML for automating model selection and hyperparameter tuning.	380	0
2356	Affirmative	\N	Yes, indeed, our organisation fully supports the interoperability of ML models.	382	0
2357	Negative	\N	No, unfortunately, our organisation does not currently support the interoperability of ML models.	382	0
2358	Undecided	\N	We are in the process of evaluating the benefits of supporting interoperability of ML models.	382	0
2359	Affirmative	\N	Yes, indeed, we have explored the use of a data science platform.	385	0
2361	Undecided	\N	We have considered it, but have not made a final decision on whether to use a data science platform.	385	0
2362	Adequate	Budget allocation adequate	The budget allocation is adequate	398	10
2363	Partially Adequate	Budget allocation partially adequate	The budget allocation is partially adequate. In some areas it is not ok though.	398	5
2364	Not Adequate	Budget allocation not adequate	The budget allocation is not adequate at all.	398	0
2365	Acceptable	Cost acceptable	The data storage cost is acceptable right now	399	10
2366	Partially Acceptable	Cost partially acceptable	The data storage cost is only partially acceptable right now.	399	5
2367	Unacceptable	Cost not acceptable	The data storage cost is not acceptable right now.	398	0
2368	Adequate	Budget adequate	The budget for data-related initiatives for the coming year is adequate	401	10
2369	Partially Adequate	Budget partially adequate	The budget for data-related initiatives for the coming year is only partially adequate.	401	5
2370	Not Adequate	Budget not adequate	The budget for data-related initiatives for the coming year is not adequate.	401	0
2371	Full Collaboration	Full collaboration on data initiatives	The department teams show full collaboration on new data initiatives.	405	10
2372	Some Collaboration	Some collaboration on data initiatives	Some departments are collaborative whereas others are not like that.	405	5
2373	No Collaboration	Teams do not collaborate	The teams do not collaborate at all on new data initiatives.	405	0
2374	Full Measures	Full measures for business continuity	Full measures are in place for business continuity	407	10
2375	Some Measures	Some measures for business continuity	Some measures are in please for business continuity.	407	5
2376	No Measures	No measures for business continuity	No measures are in please for business continuity.	407	0
2377	Ownership Identified	Ownership identified with the organisation	The data ownership is fully identified within the organisation.	408	10
2378	Some Identified	Some ownership identified	Some data ownership, but not all is identified within the organisation.	408	5
2379	None Identified	No ownership identified	The data ownership is not clear within the organisation.	408	0
2381	Some Use	Some use for business data	There is limited use for our business data	418	5
2382	No idea	No knowledge about the value of business data	There is no clear understanding of how the business data can address industry needs.	418	0
2380	Concrete Use	Concrete Use for Business Data	There is a clearly defined use for our business data.	418	10
2383	Fast	Fast project implementation	A medium size analytical project has typically a fast turn around time.	423	10
2384	Medium	Some amount of time	A medium sized analytical project takes a reasonable amount of time which is still acceptable.	423	5
2385	Long	A perceived long time	A medium sized analytical project takes a perceived long time.	423	0
2386	High	High percentage	A high percentage of advanced analytics projects has been operationalized.	425	10
2387	Medium	Medium percentage	A medium percentage of advanced analytics projects has been operationalized.	425	5
2388	Low	Low percentage	A low percentage of advanced analytics projects has been operationalized.	425	0
2389	Organised	Organised data sharing	The data is shared with external partners in a well organised manner.	433	10
2390	Adhoc	Adhoc data sharing	The data is shared with external partners in an adhoc manner.	433	5
2391	No data sharing	Data is not shared	We do not share data with external partners.	433	0
2392	Organised	Organised ingestion	The data is ingested into the data lake in an organised manner.	434	10
2393	Adhoc	Adhoc ingestion	The data is ingested into the data lake in an adhoc manner.	434	5
2394	No data lake ingestion	No data lake ingestion	The data is not ingested into the data lake.	434	0
2395	Streaming	Streaming data	The data is streamed into the database in real time.	437	10
2396	Batch	Batch ingestion	The data is pushed as a batch into the database	437	5
2398	API	API based ingestion	The data is pulled from an API into the database	437	5
2399	Organised	Organised and well structured manner	The data sources follow a common pattern of integration with the data lake.	438	10
2400	Adhoc	Adhoc patterns	The data sources follow no discernible pattern of integration with the data lake.	438	0
2401	Low Latency	Low latency integration	As soon as the data is changed in one source, it is quickly replicated to target databases.	440	10
2402	Medium Latency	Medium latency integration	In some cases data is replicated quickly in others it takes a long time.	440	5
2403	High Latency	High latency integration	The data takes a long time to replicate from source to target systems.	440	0
2404	Common Tool	Documentation with common tool	The data pipelines are documented with a common tool.	442	10
2405	Adhoc	Documentation with different tools	The data pipelines are documented with a disparate set of tools.	442	5
2406	No Documentation	No documentation for data pipelines	The data pipelines are typically not documented.	442	0
2407	Common Tool	Transformations with common tool	The data transformations are managed and versioned with a common tool.	444	10
2408	Adhoc	Transformations with different tools	The data transformations are managed and versioned with a disparate set of tools.	444	5
2409	None	No data transformations	We are not dealing with any data transformations.	444	0
2410	Organised	Orchestration and scheduling with a well known tool set	The orchestration and scheduling is done with a well defined set of tools.	445	10
2411	None	No orchestration and scheduling	We are not dealing with orchestration and scheduling.	445	0
2412	Adhoc	Orchestration and scheduling with different tools	Orchestration and scheduling happens with a disparate set of tools. There are no clear guidelines for which tools to use.	445	5
2414	Adhoc	Adhoc monitoring	Data pipeline monitoring happens with a disparate set of tools. There are no clear guidelines for which tools to use.	447	5
2415	No Monitoring	Not monitoring our pipelines	We are not dealing with pipeline monitoring at the moment.	447	0
2413	Organised	Well organised monitoring	We monitor our data pipelines in a well defined manner, with a well defined set of tools.	447	10
2416	OK	Acceptable complexity	The complexity of the computations and computations is acceptable in most cases.	458	10
2417	Depends	Partially acceptable complexity	The complexity of the computations and computations is acceptable in some cases and not in others.	458	5
2419	Too Complex	Too complex for our liking	The complexity of the computations and computations is too high for our liking.	458	0
2420	Real-time	Real-time data	Most of the data arrives in real time.	460	10
2421	Batch	Batch data	Most of the data arrives as batches from other systems.	460	5
2422	Unclear incoming data	Not clear how data arrives	It is not clear how data is ingested.	460	0
2423	All	All file formats	All file formats are supported by the data lake.	461	10
2424	Some	Some file formats	Some file formats are supported by the data lake.	461	5
2425	Only structured	Only structured file formats	Only structured file formats are supported by the data lake.	461	3
2426	No idea	No idea about file formats	Not clear which file formats are supported by the data lake.	461	0
2427	Dashboards	Dashboard based access	The data can be accessed via dashboards.	462	10
2428	Reports	File reports	The data can be accessed by file based reports.	462	5
2429	Not sure	No clarity how data is accessed	It is not clear how data is accessed at all.	462	0
2430	Central Reporting Layer	Central reporting and analytics layer	There is a central reporting and analytics data layer which is used for reporting tools.	464	10
2431	Adhoc	Adhoc reporting and analytics databases	The data for reporting is scattered among different databases.	464	5
2432	Not sure	No clarity about reporting and analytics data	It is unclear how reporting and analytics data is stored.	464	0
2433	Full Co-operation	Departments offer full co-operation	Departments offer full co-operation on data initiatives.	474	10
2434	Some Co-operation	Departments offer sometimes co-operation	Some departments offer co-operation whereas some others not.	474	5
2435	None	Departments offer no co-operation	Departments offer no collaboration on data initiatives.	474	0
2437	Ideas	Adhoc ideas	We have recorded some ideas to adapt our data strategy to evolving requirements.	478	5
2436	Plan	Plan available	We have a well detailed plan to adapt our data strategy to evolving requiremeents	478	10
2438	None	No plan or ideas	We have not created plans or recorded any ideas to adapt our data strategy.	478	0
2439	High	High business impact	There is an expected high business impact of analyzing and using currently untapped data sources.	484	10
2440	Medium	Medium business impact	There is an expected relative business impact of analyzing and using currently untapped data sources.	484	5
2441	None	No business impact	There is no expected business impact of analyzing and using currently untapped data sources.	484	0
2442	Plenty	Many data zones in data lake	We have numerous data zones in our data lake.	487	10
2443	Some	Some data zones in our data lake	We have some data zones in our data lake (4 < 10).	487	6
2444	Hardly Any	Hardly Any Datazones	We have hardly any data zones in our data lake (3 or less).	487	3
2445	None	No data zones	We are using no data zones right now	487	0
2446	All	All data sources	The data catalog is connected with all sources.	514	10
2447	Some	Some data sources	The data catalog is only connected with some data sources	514	6
2448	Only DBs	Only databases	The data catalog is only connected to the databases.	514	3
2449	None	No data sources	The data catalog is not being used.	514	0
2450	Daily	Every day	The data catalog is refreshed daily.	516	10
2451	Weekly	Every week	The data catalog is refreshed weekly.	516	6
2452	On demand	Whenever requested	The data catalog is updated on demand.	516	3
2453	Never	No updates to the data catalog	The data catalog is never updated.	516	0
2454	Both	Both SQL and NoSQL	The data modellers model SQL and NoSQL relationships.	559	10
2455	Only SQL	Only SQL	The data modellers model only SQL relationnships.	559	5
2456	Only NoSQL	Only NoSQL	The data modellers model only NoSQL relationnships.	559	5
2457	No Modelling	No modelling of any type	We have no data modellers or no modelling is done.	559	0
2458	Weekly	Every week	The data quality assessments are performed every week.	588	10
2459	Monthly	Every month	The data quality assessments are performed every month.	588	6
2460	Annually	Every Year	The data quality assessments are performed every year.	588	3
2461	Never	No checks	No checks are being performed.	588	0
2462	Horizontally	Horizontal scaling	The data infrastructure is designed to scale horizontally.	668	10
2463	Vertically	Vertical scaling	The data infrastructure is designed to scale vertically.	668	5
2464	No scaling strategy	No scaling strategy	We are not clear about the scaling strategy or we have none.	668	0
2465	Monthly	Every month	The infrastructure footprint is analyzed every month.	681	10
2466	Yearly	Every year	The infrastructure footprint is analyzed every year.	681	5
2467	5 Years	Every 5 years	We analyze it every five years or longer.	681	0
2468	Single Tool Available	Single tool available	We have already a simplified landscape of reporting tools.	685	10
2272	Affirmative	\N	Yes, indeed, we have a plan to rationalise our reporting tools.	685	6
2469	Reports Already Consolidated	Reports already consolidated	Our reports are already consolidated.	697	10
2470	Cloud	Reporting server in the cloud	Our reporting server is the cloud.	700	10
2471	Cloud and On-prem	Some on-prem and some on cloud	Our reporting servers are either on-prem or in the cloud	700	6
2472	No Servers / Do Not Know	No Servers / Do Not Know	No reporting servers or do not really know.	700	0
2473	On-prem	Reporting server on-prem	Our reporting server is on-prem.	700	3
2474	Weeks	Weeks	It takes typically just weeks to generate KPI based reports.	706	10
2475	Months	Months	It takes typically months to generate KPI based reports.	706	5
2476	Years	Years	It takes typically many years to generate KPI based reports.	706	0
2478	Data Scientists	Data scientists as testers	Our team of data scientists tests the ML models.	713	5
2479	No Testing / Do Not Know	No testing of knowledge about this	We have no clear understanding of who is testing the ML models or we are not doing it at all.	713	0
2482	None	No controls	No controls are in place to ensure that there are no leakages.	721	0
2480	Tight Controls	Tight Controls	Tight controls are in place to ensure that there are no leakages.	721	10
2481	Some Controls	Some controls	Some controls are in place to ensure that there are no leakages.	721	5
2483	Affirmative	Fully automated	All of our projects are tested using fully automated pipelines.	724	10
2484	Undecided	Partially automated	Some of our projects are tested using fully automated pipelines.	724	5
2485	Negative	Not using test automation	We are not using test automation.	724	0
2486	Yes	Self-service capability to analytical users	We provide self-service capability to users in production environment using a platform we developed ourselves.	372	10
2487	No	No self-service capability to analytical users	We provide no self-service capability to users in production environment.	372	0
2488	Affirmative	Using model versioning	We use model versioning for all our ML models.	375	10
2489	Undecided	Using some model versioning	We use model versioning for some of our ML models.	375	5
2490	Negative	Not using model versioning	We are not using model versioning.	375	0
2491	Affirmative	Considered federated learning and edge computing	We have considered using federated learning and also edge computing	379	10
2492	Undecided	Considered either federated learning or edge computing	We have considered using either federated learning or also edge computing	379	5
2493	Negative	Not considering federated learning nor edge computing	We have not considered using neither federated learning nor edge computing	379	0
2494	Affirmative	Cases available	Yes, there are use cases for Analytics as a service and use cases to support self service by business	384	10
2495	Undecided	Cases available for analytics or self service as a business	Yes, there are use cases for Analytics as a service OR use cases to support self service by business	384	5
2496	Negative	No use cases available	No, there are neither use cases for Analytics as a service nor use cases to support self service by business	384	0
2498	Undecided	Some gaps available	Yes, there are some gaps available between our data and business strategy	730	5
2497	Affirmative	Gaps available	Yes, there are large gaps available between our data and business strategy.	730	0
2499	Negative	No gaps	No, there are some gaps available between our data and business strategy.	730	10
2500	Affirmative	All assets classified	All assets have been classified based on their importance and sensitivity.	504	10
2501	Undecided	Some assets classified	Some assets have been classified based on their importance and sensitivity.	504	5
2502	Negative	No assets classified	No assets have been classified based on their importance and sensitivity.	504	0
2503	Affirmative	Comprehensive strategy available	We have a comprehensive strategy for handing sensitive or personally identifiable information (PII).	565	10
2504	Undecided	Partial strategy available	We have a partial strategy available which covers some aspects of our handing of sensitive or personally identifiable information (PII).	565	5
2505	Negative	No strategy available	We do not have a comprehensive strategy for handing sensitive or personally identifiable information (PII).	565	0
2506	Affirmative	Right to forget implemented	We have implemented right to forget as part of GDPR compliance.	572	10
2507	Undecided	Implemented partially	We have implemented partially the right to forget as part of GDPR compliance.	572	5
2508	Negative	No implementation	We have not implemented the right to forget as part of GDPR compliance.	572	0
\.


--
-- Data for Name: tb_topic; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tb_topic (id, name, description, question_amount, preferred_topic_order) FROM stdin;
15	Advanced Analytics	Advanced Analytics	5	14
16	Business Alignment	Business Alignment	5	1
17	Data Acquisition	Data Acquisition	5	2
18	Data Architecture	Data Architecture	5	3
19	Data Assets	Data Assets	5	4
20	Data Governance	Data Governance	5	5
21	Data Modelling	Data Modelling	5	6
22	Data Privacy	Data Privacy	5	8
23	Data Quality	Data Quality	5	7
24	Data Security	Data Security	5	9
25	Dataops	Dataops	5	10
26	Infrastructure	Infrastructure	5	11
27	Reporting	Reporting	5	12
28	Testing	Testing	5	13
\.


--
-- Name: tb_configuration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_configuration_id_seq', 1, true);


--
-- Name: tb_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_question_id_seq', 730, true);


--
-- Name: tb_question_score_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_question_score_id_seq', 1093, true);


--
-- Name: tb_questionnaire_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_questionnaire_status_id_seq', 59, true);


--
-- Name: tb_quiz_mode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_quiz_mode_id_seq', 4, true);


--
-- Name: tb_selected_quiz_mode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_selected_quiz_mode_id_seq', 8, true);


--
-- Name: tb_selected_topics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_selected_topics_id_seq', 25, true);


--
-- Name: tb_suggested_response_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_suggested_response_id_seq', 2508, true);


--
-- Name: tb_topic_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_topic_id_seq', 28, true);


--
-- Name: tb_configuration config_key_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_configuration
    ADD CONSTRAINT config_key_unique UNIQUE (config_key);


--
-- Name: tb_sentiment_score name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_sentiment_score
    ADD CONSTRAINT name_unique UNIQUE (name);


--
-- Name: tb_question_score question_id_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_question_score
    ADD CONSTRAINT question_id_unique UNIQUE (question_id);


--
-- Name: tb_quiz_mode quiz_mode_name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_quiz_mode
    ADD CONSTRAINT quiz_mode_name_unique UNIQUE (name);


--
-- Name: tb_selected_quiz_mode session_id_quiz_mode_id_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_selected_quiz_mode
    ADD CONSTRAINT session_id_quiz_mode_id_unique UNIQUE (session_id, quiz_mode_id);


--
-- Name: tb_selected_topics session_id_topic_id_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_selected_topics
    ADD CONSTRAINT session_id_topic_id_unique UNIQUE (session_id, topic_id);


--
-- Name: tb_configuration tb_configuration_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_configuration
    ADD CONSTRAINT tb_configuration_pkey PRIMARY KEY (id);


--
-- Name: tb_question tb_question_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_question
    ADD CONSTRAINT tb_question_pkey PRIMARY KEY (id);


--
-- Name: tb_question_score tb_question_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_question_score
    ADD CONSTRAINT tb_question_score_pkey PRIMARY KEY (id);


--
-- Name: tb_quiz_mode tb_quiz_mode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_quiz_mode
    ADD CONSTRAINT tb_quiz_mode_pkey PRIMARY KEY (id);


--
-- Name: tb_selected_quiz_mode tb_selected_quiz_mode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_selected_quiz_mode
    ADD CONSTRAINT tb_selected_quiz_mode_pkey PRIMARY KEY (id);


--
-- Name: tb_sentiment_score tb_sentiment_score_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_sentiment_score
    ADD CONSTRAINT tb_sentiment_score_pkey PRIMARY KEY (id);


--
-- Name: tb_suggested_response tb_suggested_response_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_suggested_response
    ADD CONSTRAINT tb_suggested_response_pkey PRIMARY KEY (id);


--
-- Name: tb_topic tb_topic_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_topic
    ADD CONSTRAINT tb_topic_pkey PRIMARY KEY (id);


--
-- Name: tb_topic topic_name_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_topic
    ADD CONSTRAINT topic_name_unique UNIQUE (name);


--
-- Name: tb_suggested_response question_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_suggested_response
    ADD CONSTRAINT question_id FOREIGN KEY (question_id) REFERENCES public.tb_question(id);


--
-- Name: tb_question_score question_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_question_score
    ADD CONSTRAINT question_id FOREIGN KEY (question_id) REFERENCES public.tb_question(id);


--
-- Name: tb_questionnaire_status sentiment_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_questionnaire_status
    ADD CONSTRAINT sentiment_id FOREIGN KEY (sentiment_id) REFERENCES public.tb_sentiment_score(id);


--
-- Name: tb_selected_quiz_mode tb_quiz_mode_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_selected_quiz_mode
    ADD CONSTRAINT tb_quiz_mode_id FOREIGN KEY (quiz_mode_id) REFERENCES public.tb_quiz_mode(id);


--
-- Name: tb_selected_topics tb_selected_topics_topic_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_selected_topics
    ADD CONSTRAINT tb_selected_topics_topic_id FOREIGN KEY (topic_id) REFERENCES public.tb_topic(id);


--
-- Name: tb_question topic_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_question
    ADD CONSTRAINT topic_id FOREIGN KEY (topic_id) REFERENCES public.tb_topic(id);


--
-- PostgreSQL database dump complete
--

