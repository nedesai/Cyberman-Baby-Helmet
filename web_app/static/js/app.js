var app = angular.module("Cyberman", []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{*');
  $interpolateProvider.endSymbol('*}');
}]);



app.factory('SharedService', function() {
	return {
		sharedInfo: {
			username: "",
			log_in: true,
			viewmodel: false,
			patientid: -1,
			patients: [],
			models: [] 
			//modelid, obj/stl filename, fbx link, title, description, date
		}
	};
});

