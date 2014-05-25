(function() {
    var app = angular.module('forecastApi', [
        'ngResource'
    ]);

    app.factory('api', ['$resource', function($resource) {
        
        var makeBaseApi = function(name) {
            return $resource('/api/' + name + '/:id', {
                id: '@id'
            }, {
                query: {
                    method: 'GET',
                    isArray: false
                }
            });
        };

        return {
            user: $resource('/api/user'),
            games: makeBaseApi('games'),
            leaders: makeBaseApi('leaderboard'),
            forecast: makeBaseApi('forecast'),
            prediction: makeBaseApi('prediction')
        };

    }]);
})();