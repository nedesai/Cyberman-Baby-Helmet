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

INSERT INTO Model (patientid, filetype, url, fbx_url, description, filename) VALUES
('2', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test1'),
('5', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test2'),
('6', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test3'),
('3', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test4'),
('1', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test5'),
('1', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test6'),
('6', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test7'),
('6', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test8'),
('1', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test9'),
('2', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test10'),
('1', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test11'),
('6', 'fbx', 'test.com/my_model.stl', 'test.com/my_model.fbx', 'test description', 'test12');

