var app = angular.module('forecast');

function HeaderController($scope, $location) {

    $scope.isActive = function(url) {
        return url == $location.path();
    }

}

app.controller('HeaderController', ['$scope', '$location', HeaderController]);