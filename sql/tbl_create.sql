DROP DATABASE model_db;
CREATE DATABASE model_db;
USE model_db;

CREATE TABLE User(
    username varchar(40) NOT NULL,
    firstname varchar(40),
    lastname varchar(40),
    email varchar(40),
    password varchar(256) NOT NULL,
    createddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lastmodified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(username)
);

CREATE TABLE Patient(
    patientid int NOT NULL AUTO_INCREMENT,
    username varchar(40) NOT NULL,
    firstname varchar(40),
    lastname varchar(40),
    dob date NOT NULL,
    lastmodified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(patientid),
    FOREIGN KEY(username) REFERENCES User(username)
);

CREATE TABLE Model(
    modelid int NOT NULL AUTO_INCREMENT,
    patientid int NOT NULL,
    filetype char(3) NOT NULL,
    description varchar(200),
    url varchar(1024) NOT NULL,
    createddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lastmodified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(modelid),
    FOREIGN KEY(patientid) REFERENCES Patient(patientid)
);