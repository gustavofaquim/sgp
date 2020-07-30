create database sgp;


insert into disciplina(disciplina) values ('Química');
insert into disciplina(disciplina) values ('Física');
insert into disciplina(disciplina) values ('Biologia');
insert into disciplina(disciplina) values ('História');
insert into disciplina(disciplina) values ('Geografia');
insert into disciplina(disciplina) values ('Filisofia');
insert into disciplina(disciplina) values ('Sociologia');
insert into area(area) values ('Ciências Humanas e suas Tecnologias');
insert into configuracoes(cabecalho,rodape,tipo_fonte,tamanho) values ('ola', 'mundo','TH',19);

select * from configuracoes;
select * from professor;
select * from questao;
select * from auth_user;