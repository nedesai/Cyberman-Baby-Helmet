var app = angular.module("Cyberman", ['ngRoute']);

app.config(function($routeProvider) {
	$routeProvider
		.otherwise({
			redirectTo: '/'
		});
})