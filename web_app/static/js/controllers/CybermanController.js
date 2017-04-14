app.controller('CybermanController', ['$scope', 'SharedService', '$http', function($scope, SharedService, $http) {
	
	$scope.info = SharedService.sharedInfo;

	// Update nav when clicked
	$scope.setView = function(ind) {
		$scope.info.edit = ind == 1;
		$scope.info.menuIndex = ind;
		}
	
	$scope.logout = function(){
		console.log("logout clicked");
		$http.post('api/v1/logout').then(
			function(success){
				window.location = '/';
			}
		);
	};

}]);
