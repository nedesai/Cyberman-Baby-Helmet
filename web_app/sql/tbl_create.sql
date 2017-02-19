DROP DATABASE model_db;
CREATE DATABASE model_db;
USE model_db;

CREATE TABLE User(
    username varchar(40) NOT NULL,
    firstname varchar(40),
    lastname varchar(40),
    email varchar(40),
    password varchar(256) NOT NULL,
    PRIMARY KEY(username)
);

CREATE TABLE Patient(
    patientid int NOT NULL AUTO_INCREMENT,
    firstname varchar(40),
    lastname varchar(40),
    dob date NOT NULL,
    PRIMARY KEY(patientid)
);

CREATE TABLE Model(
    modelid int NOT NULL AUTO_INCREMENT,
    patientid int NOT NULL,
    filename varchar(40) NOT NULL,
    filetype char(3) NOT NULL,
    description varchar(200),
    url varchar(1024) NOT NULL,
    uploaddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(modelid),
    FOREIGN KEY(patientid) REFERENCES Patient(patientid)
);

CREATE TABLE UserPatientLink(
    userpatientlinkid int NOT NULL AUTO_INCREMENT,
    username varchar(40) NOT NULL,
    patientid int NOT NULL,
    PRIMARY KEY(userpatientlinkid),
    FOREIGN KEY(username) REFERENCES User(username),
    FOREIGN KEY(patientid) REFERENCES Patient(patientid)
);
