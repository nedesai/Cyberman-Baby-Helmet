var app = angular.module("Cyberman", []);

app.config(['$interpolateProvider', function($interpolateProvider) {
	$interpolateProvider.startSymbol('{*');
	$interpolateProvider.endSymbol('*}');
}]);

app.filter('description', function(){
	return function(text){
		if(text.length <= 43) return text;
		if(text[44] == '.') return text.slice(0, 45);
		return text.slice(0, 40) + "...";
	}
});


app.directive('script', ['$http', 'SharedService', function($http, SharedService) {
	return {
		restrict: 'E',
		replace: true,
		scope: {
			control: "="
		},
		link: function(scope, elem, attr) {

			console.log(scope.control);

			scope.internalControl = scope.control || {};

			scope.info = SharedService.sharedInfo;

			scope.internalControl.load = function(){
				console.log("function called");
				// var model_file = "'~/tempmodel/" + scope.info.patientid + "_" + scope.info.models[scope.info.model_index].filename + scope.info.models[scope.info.model_index].filetype + "'";
				// var model_file = "'../static/assets/" + scope.info.models[scope.info.model_index].filename + scope.info.models[scope.info.model_index].filetype + "'";
				// code = code.replace("'<modeltoload>'", model_file);
				// var f = new Function(code);
				// f();
			}

			function loadModel(){
				//var model_file = "'../static/" + scope.info.patientid + "_" + scope.info.models[scope.info.model_index].filename + scope.info.models[scope.info.model_index].filetype + "'";
				var model_file = "'../static/assets/" + scope.info.models[scope.info.model_index].filename + scope.info.models[scope.info.model_index].filetype + "'";

				code = code.replace("'<modeltoload>'", model_file);
				var f = new Function(code);
				f();
			}

			if (attr.type === 'text/javascript-lazy') {
				var code = elem.text();
				if(scope.info.models.length === 0 || scope.info.models.length < scope.info.model_index) {
					// Load the Models if not there
					$http.get("api/v1/model?username=" + String(scope.info.username) + "&patientid=" + String(scope.info.patientid)).then(
						function(response) {
							scope.info.models = response.data.models;
							for(var x = 0; x < scope.info.models.length; ++x){
								scope.info.models[x]['lastmodified'] = new Date(scope.info.models[x]['lastmodified']);
							}
							loadModel();
						},
						function(error) {
							scope.errors = error.data.errors;
						}
					);
				}
				else{
					loadModel();
				}
				
			}
		}
	};
}]);

// Information share acroess directives
app.factory('SharedService', function() {
	return {
		sharedInfo: {
			username: "",
			firstname: "",
			lastname: "",
			zip_file: "NO_ZIPFILE_FOUND",
			zip_url: "#",
			model_index: 0,
			log_in: true,
			viewmodel: false,
			edit: false,
			patientid: -1,
			patients: [],
			models: [],
			menuItems: ['Home', 'Edit'],
			menuIndex: 0
			//modelid, obj/stl filename, fbx link, title, description, date
		}
	};
});

