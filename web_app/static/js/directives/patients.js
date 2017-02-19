app.directive('patients', ['http', function($http){
	return {
		restrict: 'E',
		scope: {
			username: "="
		},
		controller: function($scope) {
			$scope.patients = $http.get("api/patients/?username=" + $scope.username);
		},
		templateUrl: 'static/js/directives/patients.html',
		link: function(scope, elem, attrs) {
			scope.clickedpatient = function(id) {
				scope.obj.patientid = id;
				scope.obj.modelview = true;
			}
		}
	}
}]);