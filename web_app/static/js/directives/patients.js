app.directive('patients', ['$http', 'SharedService', function($http, SharedService){
	return {
		restrict: 'E',
		templateUrl: 'static/js/directives/patients.html',
		link: function(scope, element, attrs) {

			scope.directive_info = SharedService.sharedInfo;

			function get_patients() {
				$http.get("api/v1/patient?username=" + scope.directive_info.username).then(
					function(response) {
						scope.directive_info.patients = response.data.patients;
					}
				);
			}

			if(scope.directive_info.username == ""){
				$http.get('api/v1/login').then(
					function(success){
						scope.directive_info.username  = success.data.success.username;
						scope.directive_info.firstname = success.data.success.firstname;
						scope.directive_info.lastname  = success.data.success.lastname;
						get_patients();
					}
				);
			}

			scope.clickedpatient = function(id) {
				scope.directive_info.patientid = id;
				scope.directive_info.viewmodel = true;
			}

			scope.addnewpatient = function(firstname, lastname, dob) {
				var input = {username: scope.directive_info.username, firstname: firstname, lastname: lastname, dob: dob};
				$http.post("api/v1/patient", input).then(
					function(response) {
						scope.directive_info.patients.push(input);
						console.log(scope.patients);
					}
				);
				scope.input_firstname = '';
				scope.input_lastname = '';
				scope.input_dob = '';
			}
		}
	}
}]);
