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
('2', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'head model bob', 'bob_head_model'),
('5', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'hand model joe', 'joe_hand_model'),
('6', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'foot model jack', 'jack_food_model'),
('3', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'arm model jake', 'jake_arm_model'),
('1', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'finger model neeral', 'neeral_finger_model'),
('1', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'toe model zach', 'zach_toe_model'),
('6', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'eye model robert', 'robert_eye_model'),
('6', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'ear model kuong', 'kuong_ear_model'),
('1', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'chest model eric', 'eric_chest_model'),
('2', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'stomach model john', 'john_stomach_model'),
('1', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'teeth model bill', 'bill_teeth_model'),
('6', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'hair model billy', 'billy_hair_model');

