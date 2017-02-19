app.directive('models', ['$http', function($http){
	f
	return {
		restrict: 'E',
		scope: {
			username: "=",
			patientid: "="
		},
		controller: function($scope) {
			$scope.models = $http.get("api/models/?username=" + $scope.username + "&patientid=" + $scope.patientid);
		},
		templateUrl: 'static/js/directives/models.html',
		link: function(scope, element, attrs) {
			scope.printmodel = function(url) {
				//$http.get(to octoprint api /url);
			}
		}
	}
}]);