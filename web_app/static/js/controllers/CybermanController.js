app.controller('CybermanController', ['$scope', 'SharedService', '$http', function($scope, SharedService, $http) {
	
	$scope.info = SharedService.sharedInfo;

	// Update nav when clicked
	$scope.setView = function(ind) {
		$scope.info.viewmodel = false;
		$scope.info.edit = (ind == 1);
		$scope.info.menuIndex = ind;
	}
	
	$scope.logout = function(){
		$http.post('api/v1/logout').then(
			function(success){
				window.location = '/';
			}
		);
	};

}]);
