-- 废弃了
-- grant all privileges on test.* to 'www'@'%' identified by 'www';

-- create
create database test;
use test;

-- create & grant user
create user 'www'@'%' identified by 'www';
grant all privileges on test.* to 'www'@'%';

-- create table
create table pets (
    id varchar(50) not null,
    name varchar(100) not null,
    gender bool not null,
    birth varchar(10) not null,
    createdAt bigint not null,
    updatedAt bigint not null,
    version bigint not null,
    primary key (id)
) engine=innodb;