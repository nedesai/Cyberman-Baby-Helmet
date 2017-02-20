app.directive('patients', ['$http', function($http){
	return {
		restrict: 'E',
		scope: {
			username: "="
		},
		controller: function($scope) {
			var results = $http.get("api/v1/patient?username=" + $scope.username);
			$scope.patients = results.patients;
		},
		templateUrl: 'static/js/directives/patients.html',
		link: function(scope, element, attrs) {
			scope.clickedpatient = function(id) {
				scope.obj.patientid = id;
				scope.obj.viewmodel = true;
			}
		}
	}
}]);