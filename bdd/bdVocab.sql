CREATE DATABASE IF NOT EXISTS bdVocab;
USE bdVocab;

drop table if exists Posseder;
drop table if exists Avoir;
drop table if exists Utilisateur;
drop table if exists Liste;
drop table if exists Carnet;

drop table if exists VocaFrancais;
drop table if exists VocaAnglais;

CREATE TABLE if not exists Utilisateur (
  pseudo varchar(65) not NULL,
  password varchar(80) default null,
  CONSTRAINT pkUtilisateur PRIMARY KEY (pseudo)
) 
ENGINE=InnoDB;

CREATE TABLE if not exists Carnet (
  numCarnet varchar(80) not null,/* not null*/
  nom varchar(35) DEFAULT NULL,
  dateCreation datetime default null,
  CONSTRAINT pkCarnet PRIMARY KEY (numCarnet)
) 
ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS Posseder(
pseudo varchar(65) not null,
numCarnet varchar(80) not null,
CONSTRAINT pkPosseder primary key (pseudo, numCarnet),
CONSTRAINT fkPossederUtilisateur foreign key(pseudo) references Utilisateur(pseudo),
CONSTRAINT fkPossederCarnet foreign key(numCarnet) references Carnet(numCarnet)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Liste(
numListe varchar(55),
nom varchar(35) not null,
dateCreation datetime default null,
commentaire varchar(185),
numCarnet varchar(80), 
CONSTRAINT pkListe primary key(numListe),
CONSTRAINT fkListeCarnet foreign key(numCarnet) references Carnet(numCarnet)
)
ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS VocaFrancais(
numMF varchar(55),/*date qui se transforme en nombre en fonction des minute secondejour..*/
libelle varchar(75),
CONSTRAINT pkMotFrancais primary key (numMF)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS VocaAnglais(
numMA varchar(55),
libelle varchar(75),
CONSTRAINT pkMotAnglais primary key (numMA)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Avoir(
numMA varchar(55),
numMF varchar(55),
numListe varchar(55),
CONSTRAINT pkAvoir primary key(numMA, numMF, numListe),
CONSTRAINT fkAvoirVocaFrancais foreign key(numMF) references VocaFrancais(numMF),
CONSTRAINT fkAvoirVocaAnglais foreign key(numMA) references VocaAnglais(numMA),
CONSTRAINT fkAvoirListe foreign key(numListe) references Liste(numListe)
)
ENGINE=InnoDB;

insert into Utilisateur(pseudo, password) values('root','mdp');


select * from Avoir;
select * from VocaFrancais;
select * from VocaAnglais;
select * from Carnet;
select * from Posseder;
select * from Liste;
