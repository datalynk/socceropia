var app = angular.module('forecast');

function GamesListCtrl($scope, $modal, Games, Forecast) {
    var result = Games.query(function() {
        $scope.games = {'Thursday June 12': [{'time': '12345', host: 'Brazil', guest: 'Croatia', id:1}]};
    });

    $scope.forecast = function(game) {
      $scope.game = game;
      var modalInstance = $modal.open({
        templateUrl: '/views/games-forecast-modal.html',
        controller: ForecastCtrl,
        resolve: {
            game: function() {
                return game;
            }
        }
      });

      modalInstance.result.then(function(forecast) {
        Forecast.save(forecast);
      });

    }

};

var ForecastCtrl = function($scope, $modalInstance, game) {
    $scope.game = game;
    $scope.forecast = {'user_id': 1, 'game_id': game.id};

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    }

    $scope.save = function() {
        $modalInstance.close($scope.forecast);
    }

    $scope.clear_score = function() {
        $scope.forecast.team_host_goals = null;
        $scope.forecast.team_guest_goals = null;
    }
};

app.controller('GamesListCtrl', ['$scope', '$modal', 'Games', 'Forecast', GamesListCtrl]);