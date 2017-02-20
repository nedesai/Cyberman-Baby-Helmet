app.directive('models', ['$http', function($http){
	return {
		restrict: 'E',
		scope: {
			username: "=",
			patientid: "="
		},
		controller: function($scope) {
			var results = $http.get("api/v1/model?username=" + $scope.username + "&patientid=" + $scope.patientid);
			$scope.models = results.models;
		},
		templateUrl: 'static/js/directives/models.html',
		link: function(scope, element, attrs) {
			scope.printmodel = function(url) {
				//$http.get(to octoprint api /url);
			}
		}
	}
}]);