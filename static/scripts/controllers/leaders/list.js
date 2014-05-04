var app = angular.module('forecast');

function LeadersListCtrl($scope, Users) {
    var result = Users.query(function() {
        $scope.leaders = result.objects;
    });
}

app.controller('LeadersListCtrl', ['$scope', 'Users', LeadersListCtrl]);
