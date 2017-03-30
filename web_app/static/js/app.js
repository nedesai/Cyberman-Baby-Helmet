/*
var app = angular.module("Cyberman", ['ngRoute']);

app.config(['$interpolateProvider', function($interpolateProvider, $routeProvider) {
  $interpolateProvider.startSymbol('{*');
  $interpolateProvider.endSymbol('*}');
  $routeProvider
	.otherwise({
		redirectTo: '/'
	});
}]);
*/

var app = angular.module("Cyberman", []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{*');
  $interpolateProvider.endSymbol('*}');
}]);



app.factory('SharedService', function() {
	return {
		sharedInfo: {
			username: "headmodel22",
			viewmodel: false,
			logged_in: true,
			patientid: -1,
			models: [] 
			//modelid, obj/stl filename, fbx link, title, description, date
		}
	};
});

