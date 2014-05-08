var app = angular.module('forecast');

ICONS_URL_BASE = '/static/icons/48';

function GamesListCtrl($scope, $modal, $log, Prediction) {
  var p = Prediction.query(function() {
    var objects = p.objects,
        grouped;

    grouped = _.chain(objects)
      .map(function(obj) {
        var d = new Date(obj.game.date),
            m = moment(d);
        
        return {
          id: obj.game.id,
          host: obj.game.team_host.name,
          guest: obj.game.team_guest.name,
          date: m.format('dddd MMMM D, YYYY'), 
          time: m.format('h:mm'),
          forecast: obj.forecast
        };
      })
      .groupBy(function(obj) {
        return obj.date
      })
      .value();

    $scope.games = grouped;

  });


  $scope.iconUrl = function(countryName) {
    var country = countryName.replace(' ', '-'),
        url = ICONS_URL_BASE + '/' + country + '.png';
    return url;
  }

  $scope.iconByForecast = function(game) {
    var forecast = game.forecast.forecast;
    //$log.log($game); return '';
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
    var modalInstance = $modal.open({
      templateUrl: '/static/views/games-forecast-modal.html',
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

    modalInstance.result.then(function(game) {
        Prediction.save({
          game_id: game.id,
          forecast: game.forecast.forecast,
          team_host_goals: game.forecast.team_host_goals,
          team_guest_goals: game.forecast.team_guest_goals
        });
    });
  }

};

function ForecastCtrl($scope, $modalInstance, parentScope) {
  var oldForecast;

  $scope.game = parentScope.game;
  $scope.iconUrl = parentScope.iconUrl;
  oldForecast = angular.copy($scope.game.forecast);

  $scope.cancel = function() {
    $scope.game.forecast = oldForecast;
    $modalInstance.dismiss('close');
  }

  $scope.save = function() {
    $modalInstance.close($scope.game);
  }

}

app.controller('GamesListCtrl', ['$scope', '$modal', '$log', 'Prediction', GamesListCtrl]);
app.controller('ForecastCtlr', ['$scope', '$modalInstance', 'parentScope', ForecastCtrl]);
