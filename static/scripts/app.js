var app = angular.module('forecast', ['ngRoute', 'ngResource', 'ui.bootstrap', 'chieffancypants.loadingBar']);

app.config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $httpProvider.defaults.headers.common['X-TOKEN']= 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTM5OTU0ODU3NiwiaWF0IjoxMzk5NTQ0OTc2fQ.eyJlbWFpbCI6InZhc2lsY292c2t5QGdtYWlsLmNvbSJ9.XD4Et83MsQEO_ALVkKdPmz5SRGVGgntYpmmXZTZBHuk';

    $routeProvider
        .when('/', {
            templateUrl: '/static/views/landing.html',
            controller: 'MainCtrl',
        })
        .when('/games', {
            templateUrl: '/static/views/games-list.html',
            controller: 'GamesListCtrl'
        })
        .when('/leaderboard', {
            templateUrl: '/static/views/leaders-list.html',
            controller: 'LeadersListCtrl'
        })
        .when('/rules', {
            templateUrl: '/static/views/rules.html'
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
    return $resource('/api/games/:id', {
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

app.factory('Prediction', ['$resource', function($resource) {
    return $resource('/api/prediction/:id', {
            id: '@id'
        },
        {
            'query': {
                method: 'GET',
                isArray:false
            }
        });
}]);