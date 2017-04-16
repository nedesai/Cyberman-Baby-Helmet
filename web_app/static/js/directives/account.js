app.directive('account', ['$http', 'SharedService', function($http, SharedService, location){
	return {
		restrict: 'E',
		scope: {
		},
		templateUrl: 'static/js/directives/account.html',
		link: function(scope, element, attrs) {

			scope.directive_info = SharedService.sharedInfo;

			scope.errors = [];
			scope.success = [];

			// inputs to form
			scope.update_firstname = "";
			scope.update_lastname = "";
			scope.update_email = "";
			scope.update_password1 = "";
			scope.update_password2 = "";


			// Send put request to update user information
			scope.update = function(){
				
				var dataobj = {
					username: String(scope.directive_info.username),
					password: String(scope.password_confirm),
					firstname: String(scope.update_firstname),
					lastname: String(scope.update_lastname),
					email: String(scope.update_email),
					password1: String(scope.update_password1),
					password2: String(scope.update_password2)
				};

				// Resent response messages
				scope.errors = [];
				scope.success = [];
				// Return message saying up to date if fields empty
				if (dataobj.firstname == "" && dataobj.lastname == "" && dataobj.email == "" && 
						dataobj.password1 == "" && dataobj.password2 == ""){
					
					scope.success.push("Nothing to update");
				}
				else{
					$http.put('api/v1/register', dataobj).then(
						function(success){

							var updated = "Successfully updated ";
							var fields = success.data.updated;
							
							for(var x = 0; x < fields.length; ++x){
								if(fields[x] == "Firstname"){
									scope.directive_info.firstname = scope.update_firstname;
								}
								if(fields[x] == "Lastname"){
									scope.directive_info.lastname = scope.update_lastname;
								}
							}

							// Clear form entries
							scope.password_confirm = "";
							scope.update_firstname = "";
							scope.update_lastname  = "";
							scope.update_email     = "";
							scope.update_password1 = "";
							scope.update_password2 = "";

							// Notify use which fields were updated
							if(fields.length == 1) updated += fields[0];
							else if(fields.length == 2) updated += (fields[0] + " and "+ fields[1]);
							else{
								for(var i = 0; i < fields.length; ++i) {
									if(i != fields.length-1) updated += (fields[i] + ", ");
									else updated += ("and " + fields[i]);
								}
							}
							scope.success.push(updated);
							if(success.data.messages.length) {
								for(var m = 0; m < success.data.messages.length; ++m){
									scope.success.push(success.data.messages[m]);
								}
							}
						},
						function(error){
							scope.errors = error.data.errors;
						}
					);
				}
			}
		}
	}
}]);
