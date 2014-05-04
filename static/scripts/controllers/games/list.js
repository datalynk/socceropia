var app = angular.module('forecast');

function GamesListCtrl($scope, $modal, Games, Forecast) {
    var result = Games.query(function() {
        var _ = window._,       // TODO: shoule be angularjs module
            games = result.objects,
            grouped;

        var icons = ['http://icons-ak.wxug.com/i/c/j/clear.gif',
                        'http://icons-ak.wxug.com/i/c/j/partlycloudy.gif',
                        'http://icons-ak.wxug.com/i/c/j/mostlycloudy.gif',
                        'http://icons-ak.wxug.com/i/c/j/rain.gif',
                        'http://icons-ak.wxug.com/i/c/j/tstorms.gif',
                        'http://icons-ak.wxug.com/i/c/j/mostlycloudy.gif'];

        grouped = _.chain(games)
            .map(function(game) {
                var d = new Date(game.date);
                var m = moment(d);
                return {
                    id: game.id,
                    host: game.team_host.name,
                    guest: game.team_guest.name,
                    date: m.format('dddd MMMM D, YYYY'),    // TODO: shoule be angularjs module
                    time: m.format('h:mm'),
                    host_i: game.team_host.name.replace(' ', '-'),
                    guest_i: game.team_guest.name.replace(' ', '-'),
                    weather: icons[_.random(0, icons.length-1)]
                };
            })
            .groupBy(function(game) {
                return game.date;
            })
            .value();

        $scope.games = grouped;
    });

    var fresult = Forecast.query(function() {
        var _ = window._;
        $scope.forecasts = {};
        _.each(fresult.objects, function(f) {
            var id = f.id;
            var gameId = f.game_id;
            $scope.forecasts[gameId] = {
                id: f.id,
                team_guest_goals: f.team_guest_goals,
                team_host_goals: f.team_host_goals,
                forecast: f.forecast
            }
        });
    });

    $scope.hasForecast = function(game) {
        var gameId = game.id;
        var forecasts = $scope.forecasts;
        return true;
    }

    $scope.do_forecast = function(game) {
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
    $scope.error = '';
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

    $scope.isValid = function() {
        var b = $scope.forecast.forecast;
        var i = $scope.isNumbersInvalid();
        return b && !i;
    }


    $scope.analyze = function() {
        if (forecast.team_host_goals == '' || forecast.team_guest_goals == '') {
            $scope.error = '';
            return false;
        }
        if (forecast.forecast == 1 && forecast.team_host_goals <= forecast.team_guest_goals) {
            $scope.error = 'Team ' + game.host + ' should score more goals than team ' + game.guest;
            return true;
        }
        else if (forecast.forecast == 2 && forecast.team_guest_goals <= forecast.team_host_goals) {
            $scope.error = 'Team ' + game.guest + ' should score more goals than team ' + game.host;
            return true;
        }
        else if (forecast.forecast == 3 && forecast.team_host_goals != forecast.team_guest_goals) {
            $scope.error = 'Please enter valid number for draw';
            return true;
        }
        $scope.error = '';
        return false;
    }

    $scope.isNumbersInvalid = function() {
        var forecast = $scope.forecast;
        if (forecast.forecast == 1 && forecast.team_host_goals <= forecast.team_guest_goals) {
            $scope.error = 'Team ' + game.host + ' should score more goals than team ' + game.guest;
            return true;
        }
        else if (forecast.forecast == 2 && forecast.team_guest_goals <= forecast.team_host_goals) {
            $scope.error = 'Team ' + game.guest + ' should score more goals than team ' + game.host;
            return true;
        }
        else if (forecast.forecast == 3 && forecast.team_host_goals != forecast.team_guest_goals) {
            $scope.error = 'Please enter valid number for draw';
            return true;
        }
        $scope.error = '';
        return false;
    }
};

app.controller('GamesListCtrl', ['$scope', '$modal', 'Games', 'Forecast', GamesListCtrl]);