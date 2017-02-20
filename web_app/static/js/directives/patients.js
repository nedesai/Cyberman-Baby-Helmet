app.directive('patients', ['$http', function($http){
	return {
		restrict: 'E',
		scope: {
			username: "="
		},
		controller: function($scope) {
			$http.get("api/v1/patient?username=" + $scope.username).then(
				function(response) {
					$scope.patients = response.data.patients;
				}
			);
		},
		templateUrl: 'static/js/directives/patients.html',
		link: function(scope, element, attrs) {
			scope.clickedpatient = function(id) {
				scope.obj.patientid = id;
				scope.obj.viewmodel = true;
			}
			scope.addnewpatient = function(firstname, lastname, dob) {
				var input = {username: $scope.username, firstname: firstname, lastname: lastname, dob: dob};
				http.post("api/v1/patient", input).then(
					function(response) {
						$scope.patients.push(input);
					}
				);
			}
		}
	}
}]);