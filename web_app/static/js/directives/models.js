app.directive('models', ['$http', 'SharedService', function($http, SharedService){
	return {
		restrict: 'E',
		scope: {
			username: "=",
			patientid: "="
		},
		controller: function($scope) {
			
		},
		templateUrl: 'static/js/directives/models.html',
		link: function(scope, element, attrs) {
			
			scope.directive_info = SharedService.sharedInfo;

			$http.get("api/v1/model?username=" + scope.directive_info.username + "&patientid=" + scope.directive_info.patientid).then(
				function(response) {
					scope.directive_info.models = response.data.models;
				},
				function(response) {
					scope.error = response.data.error;
				}
			);

			scope.printmodel = function(url) {
				//$http.get(to octoprint api /url);
			}


		}
	}
}]);