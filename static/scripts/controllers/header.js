var app = angular.module('forecast');

function HeaderController($scope, $location, settings) {
    $scope.user = settings.user;
    $scope.isActive = function(url) {
        return url == $location.path();
    }

}

app.controller('HeaderCtrl', ['$scope', '$location', 'settings', HeaderController]);