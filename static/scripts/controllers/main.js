var app = angular.module('forecast');

function MainCtrl($scope, $location, $modal, settings) {
  $scope.settings = window.settings;
  
  $scope.signinForm = function() {
    var $modalInstance = $modal.open({
      templateUrl: '/static/views/signin.html'
    });
  }

}

app.controller('MainCtrl', ['$scope', '$location', '$modal', 'settings', MainCtrl]);