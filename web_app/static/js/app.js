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

app.directive('script', function() {
	return {
		restrict: 'E',
		scope: {
			model: "="
		},
		link: function(scope, elem, attr) {
			if (attr.type === 'text/javascript-lazy') {
				console.log(scope.model);
				var code = elem.text();
				var f = new Function(code);
				f();
			}
		}
	};
});

// Information share acroess directives
app.factory('SharedService', function() {
	return {
		sharedInfo: {
			username: "",
			firstname: "",
			lastname: "",
			zip_file: "NO_ZIPFILE_FOUND",
			zip_url: "#",
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

