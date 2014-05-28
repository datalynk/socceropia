var app = angular.module('forecast');

ICONS_URL_BASE = 'icons/48';

function GamesListCtrl($scope, $modal, $log, api) {
  
  function groupGames(games) {
    return _.chain(games)
      .map(function(obj) {
        var d = new Date(obj.game.date),
            m = moment(d);
        
        return {
          id: obj.game.id,
          host: obj.game.team_host.name,
          guest: obj.game.team_guest.name,
          timestamp: m.format('X'),
          date: m.format('dddd MMMM D, YYYY'), 
          time: m.format('h:mm'),
          forecast: obj.forecast || {},
          result: obj.result,
          locked: obj.game.locked
        };

      })
      .groupBy(function(obj) {
        return obj.date
      })
      .pairs()
      .sortBy(function(p) {
        return p[1][0].timestamp;
      })
      .value();
  }

  var p = api.prediction.query(function() {
    var objects = p.data.objects,
        arr, upcoming, past;

    arr = _.partition(objects, function(e) {
      return e.result != null;
    });

    past = groupGames(arr[0]);
    upcoming = groupGames(arr[1]);

    $scope.games = upcoming;
    $scope.pastGames = past;

  });


  $scope.iconUrl = function(countryName) {
    var country = countryName.replace(' ', '-'),
        url = ICONS_URL_BASE + '/' + country + '.png';
    return url;
  }

  $scope.iconByForecast = function(game) {
    var forecast = game.forecast.forecast
        ;

    if (forecast == 1) {
      return $scope.iconUrl(game.host);
    }
    else if (forecast == 2) {
      return $scope.iconUrl(game.guest);
    }
    else {
      $log.log('Icon for DRAW missed');
      return $scope.iconUrl('Moldova');
    }
  }

  $scope.openForecastDialog = function(game) {
    if (game.locked) {
      return;
    }

    var modalInstance = $modal.open({
      templateUrl: 'views/games-forecast-modal.html',
      controller: ForecastCtrl,
      resolve: {
        parentScope: function() {
          return {
            'game': game,
            'iconUrl': $scope.iconUrl
          };
        }
      }
    });

    modalInstance.result.then(function(modifiedGame) {
        game.forecast = modifiedGame.forecast;
        api.prediction.save({
          game_id: modifiedGame.id,
          forecast: modifiedGame.forecast.forecast,
          team_host_goals: modifiedGame.forecast.team_host_goals,
          team_guest_goals: modifiedGame.forecast.team_guest_goals
        });
    });
  }

};

function ForecastCtrl($scope, $modalInstance, parentScope, settings) {
  $scope.game = angular.copy(parentScope.game);
  $scope.iconUrl = parentScope.iconUrl;

  $scope.isScoreValid = function() {
    var forecast = $scope.game.forecast,
        resultEnum = {
          TEAM_HOST_WIN: 1,
          TEAM_GUEST_WIN: 2,
          TEAM_DRAW: 3
        },
        result = false
        ;

    switch (forecast.forecast) {
      case resultEnum.TEAM_HOST_WIN:
        result = forecast.team_host_goals > forecast.team_guest_goals;
        break;
      case resultEnum.TEAM_GUEST_WIN:
        result = forecast.team_guest_goals > forecast.team_host_goals;
        break;
      case resultEnum.TEAM_DRAW:
        result = forecast.team_host_goals == forecast.team_guest_goals;
        break;
      default:
        result = false;
    }

    return result;
  }

  $scope.cancel = function() {
    $modalInstance.dismiss('close');
  }

  $scope.save = function() {
    $modalInstance.close($scope.game);
  }

  $scope.team_host_range = _.range(0, 10);
  $scope.team_guest_range = _.range(0, 10);
}

app.controller('GamesListCtrl', ['$scope', '$modal', '$log', 'api', GamesListCtrl]);
app.controller('ForecastCtlr', ['$scope', '$modalInstance', 'parentScope', 'settings', ForecastCtrl]);
