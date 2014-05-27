var app = angular.module('forecast');

function HeaderController($scope, $location, api) {
    $scope.user = {name: 'abc'};
    
    var q = api.user.query().$promise;
    q.then(function(response) {
        $scope.user = response.data;
    });

    $scope.isActive = function(url) {
        return url == $location.path();
    }
}

app.controller('HeaderCtrl', ['$scope', '$location', 'api', HeaderController]);