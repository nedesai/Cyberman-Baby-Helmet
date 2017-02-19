USE model_db;

INSERT INTO User (username, firstname, lastname, email, password) VALUES
('headmodel22', 'Dr. Head', 'Modelberg', 'head@model.com', 'testpass123'),
('babyhelmet44', 'Dr. Bobby', 'McHelmet', 'baby@helmet.com', 'password44');

INSERT INTO Patient (firstname, lastname, dob) VALUES
('Alice', 'Alicestein', '2016-03-27'),
('Betty', 'Beyster', '2016-05-06'),
('Chad', 'Chadson', '2016-03-15'),
('Daniel', 'Danson', '2016-12-01'),
('John', 'Johnson', '2016-01-22'),
('Paul', 'Paulson', '2016-05-13');

INSERT INTO Model (patientid, filename, filetype, url, description) VALUES
('5', 'model_1', 'fbx', 'test.com', 'test description'),
('5', 'model_2', 'fbx', 'test.com', 'test description'),
('6', 'model_3', 'fbx', 'test.com', 'test description'),
('1', 'model_4', 'fbx', 'test.com', 'test description'),
('2', 'model_5', 'fbx', 'test.com', 'test description'),
('2', 'model_6', 'fbx', 'test.com', 'test description'),
('4', 'model_7', 'fbx', 'test.com', 'test description'),
('4', 'model_8', 'fbx', 'test.com', 'test description'),
('4', 'model_9', 'fbx', 'test.com', 'test description'),
('1', 'model_10', 'fbx', 'test.com', 'test description'),
('5', 'model_11', 'fbx', 'test.com', 'test description'),
('3', 'model_12', 'fbx', 'test.com', 'test description');

INSERT INTO UserPatientLink (username, patientid) VALUES
('headmodel22', '1'),
('headmodel22', '2'),
('babyhelmet44', '3'),
('headmodel22', '4'),
('headmodel22', '5'),
('babyhelmet44', '6');