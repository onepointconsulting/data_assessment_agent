select id, score, topic_id, preferred_question_order, yes_no_question, scored from tb_question 
where question ilike 'Are there any quality metrics or Key Performance Metrics (KPIs) in place?';

update tb_question set question = 'Did you implement right to forget as part of GDPR compliance?'
where question ilike 'How is right to forget as part of GDPR compliance implemented?';

update tb_question set yes_no_question = true
where question = 'Is there an existing published data strategy?';

update tb_question set scored = true
where question = 'Did you implement right to forget as part of GDPR compliance?';

select sr.* from tb_suggested_response sr inner join tb_question q 
on sr.question_id = q.id
where question = 'Are there any quality metrics or Key Performance Metrics (KPIs) in place?';

update tb_suggested_response set body = 'Even though there is a need, there are currently no plans to consolidate reporting.'
where id = 2524;

update tb_suggested_response set title = 'Affirmative' where id = 2483

insert into tb_suggested_response(title, subtitle, body, question_id, score)
	values('Affirmative', 'Metrics available', 'We have a wide range  of Key Performance Metrics (KPIs) in place.', 
	  (select id from tb_question where question = 'Are there any quality metrics or Key Performance Metrics (KPIs) in place?'), 10);
	  
insert into tb_suggested_response(title, subtitle, body, question_id, score)
	values('Undecided', 'Some metrics available', 'We have a limited range of Key Performance Metrics (KPIs) in place.', 
	  (select id from tb_question where question = 'Are there any quality metrics or Key Performance Metrics (KPIs) in place?'), 5);
	  
insert into tb_suggested_response(title, subtitle, body, question_id, score)
	values('Negative', 'No metrics available', 'We have no Key Performance Metrics (KPIs) in place.', 
	  (select id from tb_question where question = 'Are there any quality metrics or Key Performance Metrics (KPIs) in place?'), 0);
	  
	  
select * from tb_suggested_response where body = 'Yes, indeed, we have a private cloud in place.'
	  
select qs.* from public.tb_question_score qs
inner join tb_question q on qs.question_id = q.id
where q.question = 'Are there any quality metrics or Key Performance Metrics (KPIs) in place?';

update public.tb_question_score set affirmative_score = 10, negative_score = 0
where id = 833

insert into public.tb_question_score(question_id, affirmative_score, undecided_score, negative_score)
values((select id from tb_question where question = 'Are there gaps or misalignments to address between your data strategy and your business strategy?'), 0, 5, 10)

update public.tb_question_score qs set affirmative_score = 0, negative_score = 10
where id = 1013

SELECT Q.ID, Q.QUESTION, Q.SCORE, T.ID, T.NAME, T.DESCRIPTION, S.ID, S.TITLE, S.SUBTITLE, S.BODY
FROM TB_SUGGESTED_RESPONSE S
INNER JOIN TB_QUESTION Q ON Q.ID = S.QUESTION_ID
INNER JOIN TB_TOPIC T ON T.ID = Q.TOPIC_ID
WHERE Q.QUESTION = 'Are there any quality metrics or Key Performance Metrics (KPIs) in place?' AND T.NAME = 'Data Quality' order by S.TITLE desc

select t.name, count(*) from public.tb_question q
inner join tb_topic t on t.id = q.topic_id
where not (q.yes_no_question = false and q.scored = false)
group by t.name order by 2;