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

CREATE TABLE public.tb_topic
(
    id serial NOT NULL,
    name character varying(256) NOT NULL,
    description character varying(4096),
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
    answer character varying(4096) NOT NULL,
    score integer NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

