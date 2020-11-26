create database sgp;

/*Areas do conhecimento*/
insert into area(area) values ('Ciências Humanas e suas Tecnologias');
insert into area(area) values ('Matemática e suas Tecnologias');
insert into area(area) values ('Linguagens, Códigos e suas Tecnologias');
insert into area(area) values ('Ciências da Natureza e suas Tecnologias');

/*Disciplinas*/
insert into disciplina(disciplina) values ('Química');
insert into disciplina(disciplina) values ('Física');
insert into disciplina(disciplina) values ('Biologia');
insert into disciplina(disciplina) values ('História');
insert into disciplina(disciplina) values ('Geografia');
insert into disciplina(disciplina) values ('Filisofia');
insert into disciplina(disciplina) values ('Sociologia');
insert into disciplina(disciplina) values ('Português');
insert into disciplina(disciplina) values ('Matemática');
insert into disciplina(disciplina) values ('Inglês');

/*Categoria*/
insert into categoria(categoria,disciplina_id) values ('Morfologia',8);
insert into categoria(categoria,disciplina_id) values ('Verbos',8);
insert into categoria(categoria,disciplina_id) values ('Karl Marx e as Classes Sociais',7);
insert into categoria(categoria,disciplina_id) values ('Etnocentrismo e diversidade cultura',7);
insert into categoria(categoria,disciplina_id) values ('Vegetação',5);
insert into categoria(categoria,disciplina_id) values ('Equações', 9);

/*SubCategoria*/
insert into subcategoria(subcategoria, categoria_id) values ('Manifesto Comunista', 1);

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

select q.enunciado, a.alternativa from questao q inner join alternativa a on q.id = a.questao_id where a.correta = 1;
select * from questao;
desc questao;
select * from disciplina;
select * from categoria;
select * from subcategoria;
select * from questao;
select * from alternativa;
select * from prova;
select * from configuracoes;
select * from professor;
SELECT * FROM sgp.professor_disciplina;
select * from area;
select * from texto;
select * from auth_user;