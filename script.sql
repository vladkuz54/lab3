drop database if exists lab3;
create database lab3;

use lab3;

drop table if exists temperature;
drop table if exists humidity;
drop table if exists light;

create table temperature (
	id int auto_increment primary key,
    value float not null,
    latitude float not null,
    longitude float not null,
    timestamp datetime not null
) engine = InnoDB;

create table humidity (
	id int auto_increment primary key,
    value float not null,
    latitude float not null,
    longitude float not null,
    timestamp datetime not null
) engine = InnoDB;

create table light (
	id int auto_increment primary key,
    value float not null,
    latitude float not null,
    longitude float not null,
    timestamp datetime not null
) engine = InnoDB;