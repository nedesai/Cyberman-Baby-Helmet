/* Part-A: CREATE TABLES */

DROP DATABASE test_db;
CREATE DATABASE test_db;
USE test_db;

CREATE TABLE User(
    username varchar(40),
    firstname varchar(40),
    lastname varchar(40),
    email varchar(40),
    password varchar(256),
    PRIMARY KEY(username)
);

CREATE TABLE Patient(
    patientid int NOT NULL AUTO_INCREMENT,
    firstname varchar(40),
    lastname varchar(40),
    PRIMARY KEY(albumid)
);

CREATE TABLE Model(
    modelid int NOT NULL AUTO_INCREMENT,
    patientid int,
    filename varchar(40),
    filetype char(3),
    uploaddate timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(picid),
    FOREIGN KEY(patientid) REFERENCES Patient(patientid)
);

CREATE TABLE UserPatientLink(
    userpatientlinkid int NOT NULL AUTO_INCREMENT,
    username varchar(40),
    patientid int,
    PRIMARY KEY(userpatientlinkid),
    FOREIGN KEY(username) REFERENCES User(username),
    FOREIGN KEY(patientid) REFERENCES Patient(patientid)
);
