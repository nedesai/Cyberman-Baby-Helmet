app.controller('CybermanController', ['$scope', 'SharedService', function($scope, SharedService) {
	
	$scope.info = SharedService.sharedInfo;
	
}]);
