create database sgp;

/*Areas do conhecimento*/
insert into area(area) values ('Ciências Humanas e suas Tecnologias');
insert into area(area) values ('Matemática e suas Tecnologias');
insert into area(area) values ('Linguagens, Códigos e suas Tecnologias');
insert into area(area) values ('Ciências da Natureza e suas Tecnologias');

/*Disciplinas*/
insert into disciplina(disciplina, area_id) values ('Química',4);
insert into disciplina(disciplina,area_id) values ('Física',4);
insert into disciplina(disciplina,area_id) values ('Biologia',4);
insert into disciplina(disciplina,area_id) values ('História',1);
insert into disciplina(disciplina,area_id) values ('Geografia',1);
insert into disciplina(disciplina,area_id) values ('Filisofia',1);
insert into disciplina(disciplina,area_id) values ('Sociologia',1);
insert into disciplina(disciplina,area_id) values ('Português',3);
insert into disciplina(disciplina,area_id) values ('Matemática',2);
insert into disciplina(disciplina,area_id) values ('Inglês',3);

/*Assuntos*/
insert into assunto(assunto,disciplina_id) values ('Morfologia',8);
insert into assunto(assunto,disciplina_id) values ('Verbos',8);
insert into assunto(assunto,disciplina_id) values ('Karl Marx e as Classes Sociais',7);
insert into assunto(assunto,disciplina_id) values ('Etnocentrismo e diversidade cultura',7);
insert into assunto(assunto,disciplina_id) values ('Vegetação',5);

/*Profesosres
12459865401
Roberto Carlos
roberto@gmail.com
caralho123
10/10/1995
geografia

54789654132
Ana Carla Souza
ana@hotmail.com
caralho123
03/05/1998
Socilogia
*/

/*Questões*/



insert into configuracoes(cabecalho,rodape,tipo_fonte,tamanho) values ('ola', 'mundo','TH',19);


select * from questao;
select * from disciplina;
select * from assunto;
select * from alternativa;
select * from prova;
select * from configuracoes;
select * from professor;
SELECT * FROM sgp.professor_disciplina;
select * from area;
select * from auth_user;