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

INSERT INTO Model (patientid, filetype, model_url, fbx_url, description, name, filename) VALUES
('2', '.obj', 'https://s3.amazonaws.com/babyhead/2_batman70.obj', 'https://s3.amazonaws.com/babyhead/2_PI_Modified.fbx', 'head model bob', "Child's Head", 'PI_Modified'),
('5', '.obj', 'https://s3.amazonaws.com/babyhead/5_batman70.obj', 'https://s3.amazonaws.com/babyhead/5_batman70.fbx', 'hand model joe', "Batman", 'batman70'),
('6', '.obj', 'https://s3.amazonaws.com/babyhead/6_batman70.obj', 'https://s3.amazonaws.com/babyhead/6_PI_Modified.fbx', 'foot model jack', "Head", 'PI_Modified'),
('3', '.obj', 'https://s3.amazonaws.com/babyhead/3_batman70.obj', 'https://s3.amazonaws.com/babyhead/3_batman70.fbx', 'arm model jake', "Batman Figure", 'batman70'),
('1', '.obj', 'https://s3.amazonaws.com/babyhead/1_batman70.obj', 'https://s3.amazonaws.com/babyhead/1_PI_Modified.fbx', 'finger model neeral', "Son's Head", 'PI_Modified'),
('1', '.obj', 'https://s3.amazonaws.com/babyhead/1_batman70.obj', 'https://s3.amazonaws.com/babyhead/1_batman70.fbx', 'toe model zach', "Batman Actionfigure", 'batman70'),
('6', '.obj', 'https://s3.amazonaws.com/babyhead/6_batman70.obj', 'https://s3.amazonaws.com/babyhead/6_PI_Modified.fbx', 'eye model robert', "Neeral's Baby Head", 'PI_Modified'),
('6', '.obj', 'https://s3.amazonaws.com/babyhead/6_batman70.obj', 'https://s3.amazonaws.com/babyhead/6_batman70.fbx', 'ear model kuong', "Child's Playtoy", 'batman70'),
('1', '.obj', 'https://s3.amazonaws.com/babyhead/1_batman70.obj', 'https://s3.amazonaws.com/babyhead/1_PI_Modified.fbx', 'chest model eric', "Deformed Head Model", 'PI_Modified'),
('2', '.obj', 'https://s3.amazonaws.com/babyhead/2_batman70.obj', 'https://s3.amazonaws.com/babyhead/2_batman70.fbx', 'stomach model john', "Test Model", 'batman70'),
('1', '.obj', 'https://s3.amazonaws.com/babyhead/1_batman70.obj', 'https://s3.amazonaws.com/babyhead/1_PI_Modified.fbx', 'teeth model bill', "Zach's Head", 'PI_Modified'),
('6', '.obj', 'https://s3.amazonaws.com/babyhead/6_batman70.obj', 'https://s3.amazonaws.com/babyhead/6_batman70.fbx', 'hair model billy', "Batman Figurine", 'batman70');

