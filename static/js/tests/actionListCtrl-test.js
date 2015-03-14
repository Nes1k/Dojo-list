describe("Test kontrolera actionList", function() {
	var mockScope;

	beforeEach(function() {
		angular.mock.module('dojoApp');
	});

	beforeEach(function(){
		angular.mock.inject(function($httpBackend){
			backend = $httpBackend;
			backend.expect('GET', '/list/').respond([
				{"id": 1, "name": "Inbox", "todo": 0},
				{"id": 2, "name": "Zakupy", "todo": 0}
			])
		})
	})

	beforeEach(function() {
		angular.mock.inject(function($rootScope, Restangular){
			baseList = Restangular.service('list');
			$rootScope.data= {};
			baseList.getList().then(function(data){
				$rootScope.data.list = data;
			})
			backend.flush();
			mockScope = $rootScope.$new();
		})
	});

	beforeEach(function() {
		angular.mock.inject(function($controller, $route, $location, $routeParams){
			mockRoute = $route;
			mockLocation = $location;
			mockRouteParmas = $routeParams;
			$controller('actionListCtrl',{
				$scope: mockScope,
				$route: mockRoute,
				$location: mockLocation,
				$route: mockRouteParmas,
				baseList: baseList
			})
		})
	});

	beforeEach(function() {
		backend.expect('GET', '/list/1/actions/').respond([
			{"id": 1, "text": "Sok", "done": false }
		])
		backend.flush();
	});

	it("przetworzenie danych", function() {
		expect(mockScope.data.list).toBeDefined();
		expect(mockScope.data.list.length).toEqual(2);
	});

	it("przygotowanie listę akcji", function() {
		expect(mockScope.actions.length).toEqual(1);
	});

	it("dodanie akcji", function() {
		backend.expect('POST', '/list/1/actions/').respond([
			{"id": 13, "text": "Pomidor", "done": false }
		])
		mockScope.action = {text: 'Pomidor'};
		mockScope.addAction(mockScope.action);
		backend.flush();
		expect(mockScope.actions.length).toEqual(2);
		expect(mockScope.action).toEqual({});
	});

	it("wybieranie akcji do edycji", function() {
		mockScope.editAction(1);
		expect(mockScope.edited).toEqual(1)
	});

	it("zapisanie akcji", function() {
		backend.expect('PUT', '/list/1/actions/1/').respond(201, 'succes');
		mockScope.edited = 0;
		mockScope.saveAction(mockScope.actions[mockScope.edited]);
		backend.flush();
		expect(mockScope.edited).toEqual('')
	});

	it("usuwanie akcji", function() {
		backend.expect('DELETE', '/list/1/actions/1/').respond(201, 'succes');
		mockScope.deleteAction(mockScope.actions[0]);
		backend.flush()
		expect(mockScope.actions.length).toEqual(0);
	});
});