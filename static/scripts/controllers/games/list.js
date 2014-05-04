var app = angular.module('forecast');

function GamesListCtrl($scope, $modal, Games, Forecast) {
    var result = Games.query(function() {
        var _ = window._,
            games = result.objects,
            grouped;

        grouped = _.chain(games)
            .map(function(game) {
                var d = new Date(game.date);
                var m = moment(d);
                return {
                    id: game.id,
                    host: game.team_host.name,
                    guest: game.team_guest.name,
                    date: m.format('dddd MMMM D, YYYY'),
                    time: m.format('h:mm'),
                    host_i: game.team_host.name.replace(' ', '-'),
                    guest_i: game.team_guest.name.replace(' ', '-')
                };
            })
            .groupBy(function(game) {
                return game.date;
            })
            .value();

        $scope.games = grouped;
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