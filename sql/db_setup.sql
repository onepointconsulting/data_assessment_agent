CREATE DATABASE data_assessment_questionnaire
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


DROP TABLE IF EXISTS public.tb_questionnaire_status;
DROP TABLE IF EXISTS public.tb_question;
DROP TABLE IF EXISTS public.tb_topic;
DROP TABLE IF EXISTS public.tb_sentiment_score;

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
    PRIMARY KEY (id),
    CONSTRAINT topic_id FOREIGN KEY (topic_id)
        REFERENCES public.tb_topic (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE public.tb_questionnaire_status
(
    id serial NOT NULL,
    session_id character varying(36) NOT NULL,
    topic character varying(256) NOT NULL,
    question character varying(1024) NOT NULL,
    answer character varying(4096) NULL,
    score integer NULL,
    affirmative_sentiment_score int,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE public.tb_sentiment_score
(
    id int NOT NULL,
    name character varying(15) NOT NULL
);

ALTER TABLE tb_sentiment_score ADD CONSTRAINT name_unique UNIQUE (name);

INSERT INTO public.tb_sentiment_score(id, name) VALUES(1, 'very negative');
INSERT INTO public.tb_sentiment_score(id, name) VALUES(2, 'negative');
INSERT INTO public.tb_sentiment_score(id, name) VALUES(3, 'ambiguous');
INSERT INTO public.tb_sentiment_score(id, name) VALUES(4, 'positive');
INSERT INTO public.tb_sentiment_score(id, name) VALUES(5, 'very positive');
INSERT INTO public.tb_sentiment_score(id, name) VALUES(6, 'unknown');

