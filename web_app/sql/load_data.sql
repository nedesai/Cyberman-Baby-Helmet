USE model_db;

INSERT INTO User (username, firstname, lastname, email, password) VALUES
('headmodel22', 'Dr. Head', 'Modelberg', 'head@model.com', 'testpass123'),
('babyhelmet44', 'Dr. Bobby', 'McHelmet', 'baby@helmet.com', 'password44');

INSERT INTO Patient (firstname, lastname) VALUES
('Alice', 'Alicestein'),
('Betty', 'Beyster'),
('Chad', 'Chadson'),
('Daniel', 'Danson'),
('John', 'Johnson'),
('Paul', 'Paulson');

INSERT INTO Model (patientid, filename, filetype) VALUES
('5', 'model_1', 'fbx'),
('2', 'model_2', 'fbx'),
('1', 'model_3', 'fbx'),
('6', 'model_4', 'fbx'),
('3', 'model_5', 'fbx'),
('1', 'model_6', 'fbx'),
('6', 'model_7', 'fbx'),
('5', 'model_8', 'fbx'),
('4', 'model_9', 'fbx'),
('6', 'model_10', 'fbx'),
('2', 'model_11', 'fbx'),
('4', 'model_12', 'fbx');

INSERT INTO UserPatientLink (username, patientid) VALUES
('headmodel22', '1'),
('headmodel22', '2'),
('babyhelmet44', '3'),
('headmodel22', '4'),
('headmodel22', '5'),
('babyhelmet44', '6');