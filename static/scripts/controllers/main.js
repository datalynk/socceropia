var app = angular.module('forecast');

function MainCtrl($scope, $location) {
    $scope.settings = window.settings;
}

app.controller('MainCtrl', ['$scope', '$location', MainCtrl]);