app.directive('models', ['$http', function($http){
	return {
		restrict: 'E',
		scope: {
			username: "=",
			patientid: "="
		},
		controller: function($scope) {
			$http.get("api/v1/model?username=" + $scope.username + "&patientid=" + $scope.patientid).then(
				function(response) {
					$scope.models = response.data.models;
				},
				function(response) {
					$scope.error = response.data.error;
				}
			);
		},
		templateUrl: 'static/js/directives/models.html',
		link: function(scope, element, attrs) {
			scope.printmodel = function(url) {
				//$http.get(to octoprint api /url);
			}
		}
	}
}]);