app.directive('models', ['$http', 'SharedService', function($http, SharedService){
	return {
		restrict: 'E',
		scope: {
			username: "=",
			patientid: "="
		},
		//templateUrl: 'static/js/directives/preview.html',
		templateUrl: 'static/js/directives/models.html',
		link: function(scope, element, attrs) {
			
			scope.directive_info = SharedService.sharedInfo;
			scope.errors = [];
			scope.uploading = false;

			$http.get("api/v1/model?username=" + String(scope.directive_info.username) + "&patientid=" + String(scope.directive_info.patientid)).then(
				function(response) {
					scope.directive_info.models = response.data.models;
				},
				function(response) {
					scope.errors = response.data.error;
				}
			);

			scope.fileUpload = function() {
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
							console.log(key + " " + value);
							formData.append(key, value);
						});

						var headers = headersGetter();
						delete headers['Content-Type'];

						return formData;
					}
				}).then(
					function(data) {
						scope.upload_name = "";
						scope.upload_description = "";
						scope.uploading = false;
					},
					function(error) {
						scope.uploading = false;
						scope.errors = error.data.errors;
					}
				);
			}

			scope.printmodel = function(url) {
				// $http.get(to octoprint api /url);
			}
		}
	}
}]);