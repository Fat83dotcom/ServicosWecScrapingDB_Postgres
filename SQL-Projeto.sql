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

-- drop table materiasportal
-- drop table portalcnn

alter table portalcnn alter link_site drop not null;
alter table materiasportal alter referencia_site drop not null
alter table portalcnn add column nome_sessao varchar(100) null
alter table materiasportal add constraint fk_sessao_site foreign key (id_pk) references portalcnn(id_pk)
alter table "Core_logservicos" alter dt_hr_exec_func type timestamp without time zone

-- drop table portalcnn;
select * from portalcnn;
select * from materiasportal;
select * from "Core_logservicos"

update "Core_logservicos" set func_portal='CNN'

select portalcnn.sessao_site, titulo_materia  from portalcnn inner join materiasportal 
on(id_pk=referenciasti)
where portalcnn.id_pk=3 group by portalcnn.sessao_site, titulo_materia;


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
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10),
(11),
(12),
(13),
(14),
(15),
(16),
(17),
(18),
(19),
(20),
(21),
(22),
(23),
(24),
(25),
(26),
(27),
(28),
(29),
(30),
(31),
(32),
(33),
(34),
(35),
(36),
(37),
(38),
(39),
(40),
(41),
(42),
(43),
(44),
(45),
(46),
(47),
(48),
(49),
(50),
(51),
(52),
(53),
(54),
(55),
(56),
(57),
(58),
(59),
(60),
(61),
(62),
(63),
(64),
(65),
(66),
(67),
(68),
(69),
(70),
(71),
(72),
(73),
(74),
(75),
(76),
(77),
(78),
(79),
(80),
(81),
(82),
(83),
(84),
(85),
(86),
(87),
(88),
(89),
(90),
(91),
(92),
(93),
(94),
(95),
(96),
(97),
(98),
(99),
(100),
(101),
(102),
(103),
(104),
(105),
(106),
(107),
(108),
(109),
(110),
(111),
(112),
(113),
(114),
(115),
(116),
(117),
(118),
(119),
(120),
(121),
(122),
(123),
(124),
(125),
(126),
(127),
(128),
(129);


