USE model_db;

INSERT INTO User (username, firstname, lastname, email, password) VALUES
('headmodel22', 'Dr. Head', 'Modelberg', 'head@model.com', 'testpass123'),
('babyhelmet44', 'Dr. Bobby', 'McHelmet', 'baby@helmet.com', 'password44');

INSERT INTO Patient (username, firstname, lastname, dob) VALUES
('headmodel22', 'Alice', 'Alicestein', '2016-03-27'),
('babyhelmet44', 'Betty', 'Beyster', '2016-05-06'),
('babyhelmet44', 'Chad', 'Chadson', '2016-03-15'),
('headmodel22', 'Daniel', 'Danson', '2016-12-01'),
('babyhelmet44', 'John', 'Johnson', '2016-01-22'),
('headmodel22', 'Paul', 'Paulson', '2016-05-13');

INSERT INTO Model (patientid, filetype, url, description) VALUES
('2', 'fbx', 'test.com', 'test description'),
('5', 'fbx', 'test.com', 'test description'),
('6', 'fbx', 'test.com', 'test description'),
('3', 'fbx', 'test.com', 'test description'),
('1', 'fbx', 'test.com', 'test description'),
('1', 'fbx', 'test.com', 'test description'),
('6', 'fbx', 'test.com', 'test description'),
('6', 'fbx', 'test.com', 'test description'),
('1', 'fbx', 'test.com', 'test description'),
('2', 'fbx', 'test.com', 'test description'),
('1', 'fbx', 'test.com', 'test description'),
('6', 'fbx', 'test.com', 'test description');