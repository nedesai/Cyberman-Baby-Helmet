app.directive('patients', ['$http', 'SharedService', function($http, SharedService){
	return {
		restrict: 'E',
		templateUrl: 'static/js/directives/patients.html',
		link: function(scope, element, attrs) {

			scope.directive_info = SharedService.sharedInfo;
			scope.delete_index = -1;
			scope.delete_id = -1;

			// Load patients array of patients
			function get_patients() {
				$http.get("api/v1/patient?username=" + scope.directive_info.username).then(
					function(response) {
						scope.directive_info.patients = response.data.patients;
					}
				);
			}

			// If no username specified, make call to api to get information
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

			// Update view to show information for that patient
			scope.clickedpatient = function(id) {
				scope.directive_info.patientid = id;
				scope.directive_info.viewmodel = true;
			}

			scope.clearAddInput = function(){
				scope.input_firstname = '';
				scope.input_lastname = '';
				scope.input_dob = '';
			}

			// Upload patient array and send call to api
			scope.addnewpatient = function(firstname, lastname, dob) {
				var input = {username: scope.directive_info.username, firstname: firstname, lastname: lastname, dob: dob};
				$http.post("api/v1/patient", input).then(
					function(response) {
						scope.directive_info.patients.push(input);
						console.log(scope.patients);
					}
				);
				scope.clearAddInput();
			}

			scope.setDelete = function(index, id) {
				scope.delete_id = Number(id);
				scope.delete_index = Number(index);
			}

			scope.clearDelete = function() {
				scope.delete_id = -1;
				scope.delete_index = -1;
			}

			scope.deletepatient = function(index, id) {

				var delete_route = 'api/v1/patient/' + String(scope.directive_info.username) + '/' + String(id);

				$http.delete(delete_route).then(
					function(success){
						scope.directive_info.patients.splice(index, 1);
						scope.clearDelete();
					},
					function(error){
						scope.clearDelete();
					}
				);
			}
		}
	}
}]);
