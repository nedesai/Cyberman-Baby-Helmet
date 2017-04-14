app.directive('models', ['$http', 'SharedService', function($http, SharedService){
	return {
		restrict: 'E',
		scope: {
			username: "=",
			patientid: "="
		},
		templateUrl: 'static/js/directives/models.html',
		link: function(scope, element, attrs) {
			
			scope.directive_info = SharedService.sharedInfo;

			$http.get("api/v1/model?username=" + String(scope.directive_info.username) + "&patientid=" + String(scope.directive_info.patientid)).then(
				function(response) {
					scope.directive_info.models = response.data.models;
				},
				function(response) {
					scope.error = response.data.error;
				}
			);

			scope.fileUpload = function() {
				$http({
					method: 'POST',
					url: 'api/v1/model',
					headers: {
						'Content-Type': 'multipart/form-data'
					},
					data: {
						name:				 String(scope.upload_name),
						description: String(scope.upload_description),
						upload:							scope.file
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
				})
				.success(function (data) {

				})
				.error(function (data, status) {

				});
			}

			// scope.printmodel = function(url) {
			// 	$http.get(to octoprint api /url);
			// }
		}
	}
}]);