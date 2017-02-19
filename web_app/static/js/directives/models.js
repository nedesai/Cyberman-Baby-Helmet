app.directive('models', ['http', function($http){
	return {
		restrict: 'E',
		scope: {
			username: "=",
			patientid: "="
		},
		//controller,
		templateUrl: 'static/js/directives/models.html',
		link: function(scope, elem, attrs) {
			scope.func = function(flag) {
				scope.obj = flag;
			}
		}
	}
}]);