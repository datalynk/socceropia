var app = angular.module('forecast');

function LeadersListCtrl($scope, Leaders) {
    var result = Leaders.query(function() {
        $scope.leaders = result.objects;
    });
}

app.controller('LeadersListCtrl', ['$scope', 'Leaders', LeadersListCtrl]);
