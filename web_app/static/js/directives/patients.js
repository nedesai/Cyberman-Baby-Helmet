app.directive('patients', ['$http', 'SharedService', function($http, SharedService){
	return {
		restrict: 'E',
		templateUrl: 'static/js/directives/patients.html',
		controller: function($scope) {
			$http.get("api/v1/patient?username=" + scope.directive_info.username).then(
				function(response) {
					$scope.patients = response.data.patients;
				}
			);
		},
		link: function(scope, element, attrs) {

			scope.directive_info = SharedService.sharedInfo;

			$http.get("api/v1/patient?username=" + scope.directive_info.username).then(
				function(response) {
					scope.patients = response.data.patients;
				}
			);

			scope.clickedpatient = function(id) {
				scope.directive_info.patientid = id;
				scope.directive_info.viewmodel = true;
			}

			scope.addnewpatient = function(firstname, lastname, dob) {
				var input = {username: scope.directive_info.username, firstname: firstname, lastname: lastname, dob: dob};
				$http.post("api/v1/patient", input).then(
					function(response) {
						scope.patients.push(input);
					}
				);
				scope.input_firstname = '';
				scope.input_lastname = '';
				scope.input_dob = '';
			}
		}
	}
}]);
