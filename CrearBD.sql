CREATE DATABASE tareas;
use tareas;

create table tareas(
	ID char(8) primary key,
    Titulo varchar(50) not null,
    Descripcion varchar(50) not null, 
    FechaIngreso varchar(10) not null,
    Estado int(1) not null
);

create table tareaSimple(
	ID char(8) primary key,
    FechaVencimiento varchar(10) not null,
    FOREIGN KEY (ID) REFERENCES tareas(ID)
);

create table tareaRecurrente(
	ID char(8) primary key,
    frecuencia varchar(50) not null,
    FOREIGN KEY (ID) REFERENCES tareas(ID)
);