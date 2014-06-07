(function(){

    var success = function(response) {
        return {
            status: "success",
            data: response
        };
    };

    var fail = function(response) {
        return {
            status: "fail",
            data: response
        };
    }

    var error = function(message) {
        return {
            status: "error",
            message: message
        }
    }

    var app = angular.module('forecastMock', ['ngMockE2E']);

    app.run(['$httpBackend', function($httpBackend) {
        $httpBackend.whenGET('/api/user').respond({
            data: {
                name: 'Igor V'
            }
        });

        $httpBackend.whenGET('/api/leaderboard').respond({
            data: {
                objects: [
                    {name: 'User 1', score: 10},
                    {name: 'User 2', score: 20},
                    {name: 'User 3', score: 30},
                    {name: 'User 4', score: 40},
                    {name: 'User 5', score: 50}   
                ]
            }
        });

        var games = {
            objects: [
                {
                    game: {
                        id: 1,
                        team_host: {
                            id: 10,
                            name: "Brazil"
                        },
                        team_guest: {
                            id: 20,
                            name: "Argentina"
                        },
                        date: "2014-06-12 12:15",
                        locked: false
                    },
                    forecast: {
                        forecast: 1,
                        team_host_goals: 2,
                        team_guest_goals: 0
                    }
                },
                {
                    game: {
                        id: 1,
                        team_host: {
                            id: 10,
                            name: "Russia"
                        },
                        team_guest: {
                            id: 20,
                            name: "Colombia"
                        },
                        date: "2014-06-12 12:15",
                        locked: true
                    },
                    forecast: {
                        forecast: 1,
                        team_host_goals: 2,
                        team_guest_goals: 0
                    }
                },
                {
                    game: {
                        id: 1,
                        team_host: {
                            id: 10,
                            name: "Russia"
                        },
                        team_guest: {
                            id: 20,
                            name: "Colombia"
                        },
                        date: "2014-06-12 12:15",
                        locked: true
                    },
                    forecast: {
                        forecast: 1,
                        team_host_goals: 2,
                        team_guest_goals: 0,
                        points: 3
                    },
                    result: {
                        team_host_goals: 0,
                        team_guest_goals: 0
                    }
                },
                {
                    game: {
                        id: 1,
                        team_host: {
                            id: 10,
                            name: "Italy"
                        },
                        team_guest: {
                            id: 20,
                            name: "USA"
                        },
                        date: "2014-06-12 12:15",
                        locked: true
                    },
                    forecast: null,
                    result: {
                        team_host_goals: 0,
                        team_guest_goals: 0
                    }
                }   
            ]
        }
        $httpBackend.whenGET('/api/prediction').respond(success(games));

        $httpBackend.whenPOST('/api/prediction').respond(
            success({})
        );

        $httpBackend.whenGET(/^views/).passThrough();
        $httpBackend.whenGET(/^directive/).passThrough();
        
    }]);

}());