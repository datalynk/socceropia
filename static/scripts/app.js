var app = angular.module('forecast', [
    'forecastApi',
    'ngRoute',
    'ui.bootstrap',
    'chieffancypants.loadingBar']);

app.constant('ICONS_URL_BASE', 'icons/48');

app.directive('soFlag', ['ICONS_URL_BASE', function(ICONS_URL_BASE) {
    return {
        restrict: 'E',
        scope: {
            name: "=countryName"
        },
        link: function(scope, element, attrs) {
            var countryName = (scope.name || attrs.countryName || '').replace(' ', '-');
            var imgUrl = ICONS_URL_BASE + '/' + countryName + '.png';
            element.append($('<img />').attr('src', imgUrl));
        }
    }
}]);

app.directive('soForecastIcon', function() {
    return {
        restrict: 'E',
        scope: {
            forecast: "=forecast",
            game: "=game"
        },
        templateUrl: 'directive/forecast-icon.html'
    }
});

app.directive('userForecast', function() {
    return {
        restrict: 'A',
        scope: {
            game: "=userForecast",
        },
        templateUrl: 'directive/user-forecast.html'
    }
});

app.constant('settings', window.settings);

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'views/landing.html',
            controller: 'MainCtrl',
        })
        .when('/games', {
            templateUrl: 'views/games-list.html',
            controller: 'GamesListCtrl'
        })
        .when('/leaderboard', {
            templateUrl: 'views/leaders-list.html',
            controller: 'LeadersListCtrl'
        })
        .when('/rules', {
            templateUrl: 'views/rules.html'
        })
        .otherwise({
            redirectTo: '/'
        });
}]);