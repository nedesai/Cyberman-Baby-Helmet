var app = angular.module("Cyberman", ['ngRoute']);


app.config(['$interpolateProvider', function($interpolateProvider, $routeProvider) {
  $interpolateProvider.startSymbol('{*');
  $interpolateProvider.endSymbol('*}');
  $routeProvider
	.otherwise({
		redirectTo: '/'
	});
}]);

