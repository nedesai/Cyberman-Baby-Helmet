app.directive('login', ['$http', 'SharedService', '$location', function($http, SharedService, location){
	return {
		restrict: 'E',
		scope: {
		},
		templateUrl: 'static/js/directives/login.html',
		link: function(scope, element, attrs) {

			scope.directive_info = SharedService.sharedInfo;

			// Login errors
			scope.errors = [];

			// Call to api to get credentials
			scope.login = function(){
				var dataobj = {
					username: String(scope.login_username),
					password: String(scope.login_password)
				};
				$http.post('api/v1/login', dataobj).then(
					function(success){
						window.location = '/';
					},
					function(error){
						scope.errors = [];
						scope.errors.push(error.data.error);
					}
				);
			}
		}
	}
}]);
