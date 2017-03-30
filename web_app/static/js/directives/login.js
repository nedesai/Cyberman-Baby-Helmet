app.directive('login', ['$http', 'SharedService', function($http, SharedService){
	return {
		restrict: 'E',
		scope: {
		},
		templateUrl: 'static/js/directives/login.html',
		link: function(scope, element, attrs) {

			scope.directive_info = SharedService.sharedInfo;

			scope.errors = [];

			scope.login = function(){
				
				var dataobj = {
					username: String(scope.username),
					password: String(scope.password)
				};
				$http.post('api/v1/login', dataobj).then(
					function(success){
						scope.directive_info.logged_in = true;
						scope.directive_info.username = response.data.username;
					},
					function(error){
						scope.errors = error.data.error;
					}
				);

			}
		}
	}
}]);