-- For newer versions of Postgres
CREATE DATABASE data_assessment_questionnaire
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- For older versions of Postgres
CREATE DATABASE data_assessment_questionnaire
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


DROP TABLE IF EXISTS public.tb_questionnaire_status;
DROP TABLE IF EXISTS public.tb_suggested_response;
DROP TABLE IF EXISTS public.tb_question;
DROP TABLE IF EXISTS public.tb_topic;
DROP TABLE IF EXISTS public.tb_sentiment_score;
DROP TABLE IF EXISTS public.tb_question_score;

CREATE TABLE public.tb_topic
(
    id serial NOT NULL,
    name character varying(256) NOT NULL,
    description character varying(4096),
    question_amount int NOT NULL,
    preferred_topic_order int NULL,
    PRIMARY KEY (id)
);

ALTER TABLE tb_topic ADD CONSTRAINT topic_name_unique UNIQUE (name);

CREATE TABLE public.tb_question
(
    id serial NOT NULL,
    question character varying(1024) NOT NULL,
    score integer NOT NULL,
    topic_id integer NOT NULL,
    preferred_question_order int NULL,
    PRIMARY KEY (id),
    CONSTRAINT topic_id FOREIGN KEY (topic_id)
        REFERENCES public.tb_topic (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE public.tb_suggested_response
(
    id serial NOT NULL,
    title character varying(256) NOT NULL,
    subtitle character varying(256),
    body character varying(1024) NOT NULL,
    question_id integer NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT question_id FOREIGN KEY (question_id)
        REFERENCES public.tb_question (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE public.tb_sentiment_score
(
    id int NOT NULL,
    name character varying(15) NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE tb_sentiment_score ADD CONSTRAINT name_unique UNIQUE (name);

CREATE TABLE public.tb_question_score
(
    id serial NOT NULL,
    question_id int NOT NULL,
    affirmative_score int,
    undecided_score int,
    negative_score int,
    PRIMARY KEY (id),
    CONSTRAINT question_id FOREIGN KEY (question_id)
        REFERENCES public.tb_question (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE tb_question_score ADD CONSTRAINT question_id_unique UNIQUE (question_id);

CREATE TABLE public.tb_questionnaire_status
(
    id serial NOT NULL,
    session_id character varying(36) NOT NULL,
    topic character varying(256) NOT NULL,
    question character varying(1024) NOT NULL,
    answer character varying(4096) NULL,
    score integer NULL,
    sentiment_id int,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT sentiment_id FOREIGN KEY (sentiment_id)
        REFERENCES public.tb_sentiment_score (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

INSERT INTO public.tb_sentiment_score(id, name) VALUES(0, 'unknown');
INSERT INTO public.tb_sentiment_score(id, name) VALUES(1, 'very negative');
INSERT INTO public.tb_sentiment_score(id, name) VALUES(2, 'negative');
INSERT INTO public.tb_sentiment_score(id, name) VALUES(3, 'ambiguous');
INSERT INTO public.tb_sentiment_score(id, name) VALUES(4, 'positive');
INSERT INTO public.tb_sentiment_score(id, name) VALUES(5, 'very positive');

-- Initial scoring
-- Run this after all questions were imported
insert into tb_question_score(question_id, affirmative_score, undecided_score, negative_score) select id, 10, 5, 0 from tb_question;

-- Scoring view

DROP VIEW vw_question_scores;

CREATE VIEW vw_question_scores as
SELECT 
	CASE
		WHEN STRPOS('positive', SS.NAME) > 0 THEN
			(SELECT AFFIRMATIVE_SCORE
				FROM PUBLIC.TB_QUESTION_SCORE QS
				WHERE QS.QUESTION_ID = Q.ID)
		WHEN STRPOS('negative', SS.NAME) > 0 THEN
			(SELECT NEGATIVE_SCORE
				FROM PUBLIC.TB_QUESTION_SCORE QS
				WHERE QS.QUESTION_ID = Q.ID)
		WHEN SS.NAME = 'ambiguous' THEN
			(SELECT UNDECIDED_SCORE
				FROM PUBLIC.TB_QUESTION_SCORE QS
				WHERE QS.QUESTION_ID = Q.ID)
		ELSE 0
	END SCORE,
	(SELECT GREATEST(AFFIRMATIVE_SCORE, UNDECIDED_SCORE, NEGATIVE_SCORE)
		FROM PUBLIC.TB_QUESTION_SCORE QS
		WHERE QS.QUESTION_ID = Q.ID) MAX_SCORE,
	SS.NAME SENTIMENT_NAME,
	S.SENTIMENT_ID,
	T.NAME TOPIC_NAME,
	S.SESSION_ID,
	Q.question,
	S.answer,
	S.created_at,
	S.updated_at
FROM TB_QUESTIONNAIRE_STATUS S
INNER JOIN PUBLIC.TB_SENTIMENT_SCORE SS ON SS.ID = S.SENTIMENT_ID
INNER JOIN PUBLIC.TB_QUESTION Q ON Q.QUESTION = S.QUESTION
FULL JOIN PUBLIC.TB_TOPIC T ON T.ID = Q.TOPIC_ID AND T.NAME = S.TOPIC;


