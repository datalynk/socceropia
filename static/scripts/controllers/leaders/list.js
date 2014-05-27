var app = angular.module('forecast');

function LeadersListCtrl($scope, api) {
    
    $scope.leaders = [];

    api.leaders.query(function(result) {
        $scope.leaders = result.data.objects;
    });

}

app.controller('LeadersListCtrl', ['$scope', 'api', LeadersListCtrl]);
