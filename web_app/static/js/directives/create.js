app.directive('create', ['$http', 'SharedService', function($http, SharedService, location){
	return {
		restrict: 'E',
		scope: {
		},
		templateUrl: 'static/js/directives/create.html',
		link: function(scope, element, attrs) {

			scope.directive_info = SharedService.sharedInfo;

			scope.errors = [];

			scope.create = function(){
				
				var dataobj = {
					username: String(scope.create_username),
					firstname: String(scope.create_firstname),
					lastname: String(scope.create_lastname),
					email: String(scope.create_email),
					password1: String(scope.create_password1),
					password2: String(scope.create_password2)
				};
				scope.directive_info.log_in = true;
				/*
				$http.post('api/v1/register', dataobj).then(
					function(success){
						scope.directive_info.log_in = true;
					},
					function(error){
						scope.errors = [];
						scope.errors.push(error.data.errors);
					}
				);*/
			}
		}
	}
}]);
