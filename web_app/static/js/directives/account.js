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

			scope.update = function(){
				
				var dataobj = {
					//username: String(scope.username_confirm),
					//password: String(scope.password_confirm),
					username: String(scope.directive_info.username),
					firstname: String(scope.update_firstname),
					lastname: String(scope.update_lastname),
					email: String(scope.update_email),
					password1: String(scope.update_password1),
					password2: String(scope.update_password2)
				};

				$http.put('api/v1/register', dataobj).then(
					function(success){
						scope.success.push("Updated Account!");
					},
					function(error){
						scope.errors = [];
						scope.errors.push(error.data.errors);
					}
				);
			}
		}
	}
}]);
