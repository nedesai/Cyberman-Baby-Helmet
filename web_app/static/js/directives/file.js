// Directive to bind file to be able to send an angular post request
app.directive('file', function () {
	return {
		scope: {
			file: '='
		},
		link: function (scope, el, attrs) {
			el.bind('change', function (event) {
				var file = event.target.files[0];
				scope.file = file ? file : undefined;
				scope.$apply();
			});
		}
	};
});