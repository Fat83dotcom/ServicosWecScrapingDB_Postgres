CREATE TABLE portalcnn(
	id_pk int primary key,
	dt_hr_pesquisa timestamp without time zone null,
	nome_sessao varchar(100) null,
	link_site varchar(255) null unique
	
);

CREATE TABLE materiasportal(
	id_pk int primary key,
	referencia_site int null references portalcnn(id_pk),
	dt_materia date null,
	link_materia text null,
	titulo_materia text null,
	texto_materia text null
);

CREATE TABLE portalG1(
	id_pk int primary key,
	dt_hr_pesquisa timestamp without time zone null,
	nome_sessao varchar(100) null,
	link_site varchar(255) null unique
);

CREATE TABLE materiasportalG1(
	id_pk int primary key,
	referencia_site int null references portalG1(id_pk),
	dt_materia date null,
	link_materia text null,
	titulo_materia text null,
	texto_materia text null
);

CREATE TABLE portalUOL(
	id_pk int primary key,
	dt_hr_pesquisa timestamp without time zone null,
	nome_sessao varchar(100) null,
	link_site varchar(255) null unique
);

CREATE TABLE materiasportalUOL(
	id_pk int primary key,
	referencia_site int null references portalUOL(id_pk),
	dt_materia date null,
	link_materia text null,
	titulo_materia text null,
	texto_materia text null
);

CREATE TABLE portalTerra(
	id_pk int primary key,
	dt_hr_pesquisa timestamp without time zone null,
	nome_sessao varchar(100) null,
	link_site varchar(255) null unique
);

CREATE TABLE materiasportalTerra(
	id_pk int primary key,
	referencia_site int null references portalTerra(id_pk),
	dt_materia date null,
	link_materia text null,
	titulo_materia text null,
	texto_materia text null
);

CREATE TABLE log_erro(
	id_pk serial primary key,
	dt_hr_erro timestamp without time zone null, 
	classe_erro varchar(255) null, 
	descricao_erro text null,
	nome_funcao_origem varchar(255) null
);

select * from log_erro

-- drop table materiasportal
-- drop table portalcnn

alter table portalcnn alter link_site drop not null;
alter table materiasportal alter referencia_site drop not null
alter table portalcnn add column nome_sessao varchar(100) null
alter table materiasportal add constraint fk_sessao_site foreign key (id_pk) references portalcnn(id_pk)
alter table "Core_logservicos" alter dt_hr_exec_func type timestamp without time zone
alter table materiasportal rename to materiasportalcnn

-- drop table portalcnn;
select * from portalcnn;
select * from materiasportalcnn;
select * from "Core_logservicos"

update "Core_logservicos" set func_portal='CNN'

select portalcnn.sessao_site, titulo_materia  from portalcnn inner join materiasportal 
on(id_pk=referenciasti)
where portalcnn.id_pk=3 group by portalcnn.sessao_site, titulo_materia;

select * from portalg1
select * from materiasportalg1
truncate table portalg1 cascade
truncate table materiasportalg1

select * from portalUOL
select * from materiasportalUOL


insert into portalcnn (id_pk, link_site) values
(0, 'd'),
(1, 'h'),
(2, 's'),
(3, 'n'),
(4, 't'),
(5, 'a'),
(6, 'v'),
(7, 'w'),
(8, 'f'),
(9, 'r');
insert into materiasportal (id_pk) values
(0),