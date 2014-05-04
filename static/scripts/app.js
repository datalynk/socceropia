var app = angular.module('forecast', ['ngRoute', 'ngResource', 'ui.bootstrap', 'chieffancypants.loadingBar']);

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: '/views/landing.html',
            controller: 'MainCtrl',
        })
        .when('/games', {
            templateUrl: '/views/games-list.html',
            controller: 'GamesListCtrl'
        })
        .when('/leaderboard', {
            templateUrl: '/views/leaders-list.html',
            controller: 'LeadersListCtrl'
        })
        .when('/rules', {
            templateUrl: '/views/rules.html'
        })
        .otherwise({
            redirectTo: '/'
        });
}]);


// modules
angular.module('_', []).factory('_', function() {
    return window._;
});

// resources
app.factory('Games', ['$resource', function($resource) {
    return $resource('/api/game/:id', {
            id: '@id'
        },
        {
            'query': {
                method: 'GET',
                isArray:false
            }
        });
}]);

app.factory('Users', ['$resource', function($resource) {
    return $resource('/api/user/:id', {
            id: '@id'
        },
        {
            'query': {
                method: 'GET',
                isArray:false
            }
        });
}]);

app.factory('Forecast', ['$resource', function($resource) {
    return $resource('/api/forecast/:id', {
            id: '@id'
        },
        {
            'query': {
                method: 'GET',
                isArray:false
            }
        });
}]);