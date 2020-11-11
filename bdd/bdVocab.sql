CREATE DATABASE IF NOT EXISTS bdVocab;
USE bdVocab;

drop table if exists Posseder;
drop table if exists Contenir;
drop table if exists Avoir;
drop table if exists Appartenir;
drop table if exists Utilisateur;
drop table if exists Liste;
drop table if exists Carnet;

drop table if exists VocaFrancais;
drop table if exists VocaAnglais;

CREATE TABLE if not exists Utilisateur (
  numUtil int(210) auto_increment,
  pseudo varchar(35) DEFAULT NULL,
  password varchar(35) default null,
  CONSTRAINT pkUtilisateur PRIMARY KEY (numUtil)
) 
ENGINE=InnoDB;

CREATE TABLE if not exists Carnet (
  numCarnet int(210) auto_increment,
  nom varchar(35) DEFAULT NULL,
  dateCreation datetime default null,
  CONSTRAINT pkCarnet PRIMARY KEY (numCarnet)
) 
ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS Posseder(
numUtil int(210) not null,
numCarnet int(210) not null,
CONSTRAINT pkPosseder primary key (numUtil, numCarnet),
CONSTRAINT fkPossederUtilisateur foreign key(numUtil) references Utilisateur(numUtil),
CONSTRAINT fkPossederCarnet foreign key(numCarnet) references Carnet(numCarnet)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Liste(
numListe int(210) not null,
nom varchar(35) not null,
dateCreation datetime not null,
commentaire varchar(185),
numCarnet int(210), 
CONSTRAINT pkListe primary key(numListe),
CONSTRAINT fkListeCarnet foreign key(numCarnet) references Carnet(numCarnet)
)
ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS VocaFrancais(
numMF int(210),
libelle varchar(75),
dateCreation datetime not null,
CONSTRAINT pkMotFrancais primary key (numMF)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS VocaAnglais(
numMA int(210),
libelle varchar(75),
dateCreation datetime not null,
CONSTRAINT pkMotAnglais primary key (numMA)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Avoir(
numMA int(210),
numMF int(210),
numListe int(210) not null,
CONSTRAINT pkAvoir primary key(numMA, numMF, numListe),
CONSTRAINT fkAvoirVocaFrancais foreign key(numMF) references VocaFrancais(numMF),
CONSTRAINT fkAvoirVocaAnglais foreign key(numMA) references VocaAnglais(numMA),
CONSTRAINT fkAvoirListe foreign key(numListe) references Liste(numListe)
)
ENGINE=InnoDB;

insert into Utilisateur(pseudo, password) values('root','mdp');

