USE model_db;

INSERT INTO User (username, firstname, lastname, email, password) VALUES
('headmodel22', 'Dr. Head', 'Modelberg', 'head@model.com', 'sha512$6159012d003f421ab7820f733a2e071c$43b6493220dd1a787a9ca1694fa58f2bcca789df333728dcdb62c68a45bbeab43c3923519886a41278d664f18ed624701e9bf1d12ec0b3ff50bfc201cef5bb37'),
('babyhelmet44', 'Dr. Bobby', 'McHelmet', 'baby@helmet.com', 'sha512$6151faf457f6433d95eb2acce9df8557$2239bcc574b5d1579a6cbd8c9fb93a86c828ab6b09cfe3cfc1f58bad12da7d7455b6bb266b993e8ebe7da0fcebc7b4f7809e3e3f844fbcc2b4927023a11f2887');

INSERT INTO Patient (username, firstname, lastname, dob) VALUES
('headmodel22', 'Alice', 'Alicestein', '2016-03-27'),
('babyhelmet44', 'Betty', 'Beyster', '2016-05-06'),
('babyhelmet44', 'Chad', 'Chadson', '2016-03-15'),
('headmodel22', 'Daniel', 'Danson', '2016-12-01'),
('babyhelmet44', 'John', 'Johnson', '2016-01-22'),
('headmodel22', 'Paul', 'Paulson', '2016-05-13');

INSERT INTO Model (patientid, filetype, url, fbx_url, description, filename) VALUES
('2', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'head model bob', 'child_head_model'),
('5', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'hand model joe', 'batman_model'),
('6', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'foot model jack', 'child_head_model'),
('3', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'arm model jake', 'batman_model'),
('1', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'finger model neeral', 'child_head_model'),
('1', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'toe model zach', 'batman_model'),
('6', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'eye model robert', 'child_head_model'),
('6', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'ear model kuong', 'batman_model'),
('1', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'chest model eric', 'child_head_model'),
('2', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'stomach model john', 'batman_model'),
('1', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/PI_Modified.fbx', 'teeth model bill', 'child_head_model'),
('6', 'fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'https://s3.amazonaws.com/babyhead/batman70.fbx', 'hair model billy', 'batman_model');

