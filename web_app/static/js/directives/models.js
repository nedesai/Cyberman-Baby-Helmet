app.directive('models', ['$http', 'SharedService', function($http, SharedService){
	return {
		restrict: 'E',
		scope: {
			control: "=" 
		},
		templateUrl: 'static/js/directives/models.html',
		link: function(scope, element, attrs) {

			console.log("hi");
			console.log(scope.control);

			scope.directive_info = SharedService.sharedInfo;

			scope.model_index = 1;

			scope.success = "";
			scope.errors = [];
			scope.uploading = false;

			// Load the Models
			$http.get("api/v1/model?username=" + String(scope.directive_info.username) + "&patientid=" + String(scope.directive_info.patientid)).then(
				function(response) {
					scope.directive_info.models = response.data.models;
					for(var x = 0; x < scope.directive_info.models.length; ++x){
						scope.directive_info.models[x]['lastmodified'] = new Date(scope.directive_info.models[x]['lastmodified']);
					}
				},
				function(error) {
					scope.errors = error.data.errors;
				}
			);

			// Toggle the display of the form and turn off success message
			scope.uploadToggle = function() {
				scope.add_model = !scope.add_model;
				scope.success = "";
			}

			scope.clearMessages = function() {
				scope.success = "";
				scope.errors = [];
			}

			scope.fileUpload = function() {
				scope.clearMessages();
				scope.uploading = true;
				$http({
					method: 'POST',
					url: 'api/v1/model',
					headers: {
						'Content-Type': 'multipart/form-data'
					},
					data: {
						username:    String(scope.directive_info.username),
						patientid:   String(scope.directive_info.patientid),
						name:				 String(scope.upload_name),
						description: String(scope.upload_description),
						file:							scope.file
					},
					transformRequest: function (data, headersGetter) {
						var formData = new FormData();
						angular.forEach(data, function (value, key) {
							formData.append(key, value);
						});

						var headers = headersGetter();
						delete headers['Content-Type'];

						return formData;
					}
				}).then(
					function(success) {
						document.getElementById("add-model").reset();
						var new_model = success.data;
						new_model['lastmodified'] = new Date(new_model['lastmodified'] + " GMT");
						scope.directive_info.models.unshift(new_model);
						scope.uploading = false;
						scope.success = "Added Model " + new_model['filename']+new_model['filetype'];
					},
					function(error) {
						scope.uploading = false;
						scope.errors = error.data.errors;
					}
				);
			}

			scope.clickModel = function(ind) {
				scope.directive_info.model_index = ind;
				console.log(ind);
				console.log(scope.directive_info.models[ind].fbx_url);
			}

			scope.printmodel = function(url) {
				// $http.get(to octoprint api /url);
			}
		}
	}
}]);