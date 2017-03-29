app.controller('CybermanController', ['$scope', 'SharedService', function($scope, SharedService) {
	
	
	// sharedInfo: {
	// 	username: "headmodel22",
	// 	viewmodel: false,
	// 	patientid: -1,
	// 	models: [] 
	// }
	
	$scope.info = SharedService.sharedInfo;
	
}]);
