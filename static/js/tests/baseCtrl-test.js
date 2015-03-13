describe("Test podstawowego kontrolera", function() {
	var mockScope = {};
	var controller;

	beforeEach(function() {
		angular.mock.module('dojoApp');
	});

	beforeEach(function(){
		angular.mock.inject(function($httpBackend){
			backend = $httpBackend;
			backend.expect('GET', '/list/').respond([{"id": 1, "name": "Inbox", "todo": 0}, {"id": 2, "name": "Zakupy", "todo": 0}])
		})
	})

	beforeEach(function() {
		angular.mock.inject(function($controller, $rootScope, $location, Restangular){
			mockScope = $rootScope.$new();
			mockLocation = $location;
			baseList = Restangular.service('list');
			controller = $controller('baseCtrl', {
				$scope: mockScope,
				$location: mockLocation,
				baseList: baseList
			})
			backend.flush();
		})
	});

	it("wykonanie żądzania Ajax", function() {
		backend.verifyNoOutstandingExpectation();
	});

	it("przetworzenie danych", function() {
		expect(mockScope.data.list).toBeDefined();
		expect(mockScope.data.list.length).toEqual(2);
	});

	it("wybieranie listy do edycji", function() {
		mockScope.setEditedList(3);
		expect(mockScope.edited).toEqual(3);
	});

	it("zapisywanie zmian", function() {
		backend.expect('PUT', '/list/1/').respond(201, 'succes');
		mockScope.edited = 0;
		mockScope.saveChanges(mockScope.data.list[mockScope.edited]);
		backend.flush()
		expect(mockScope.edited).toEqual('')
	});

	it("dodawanie listy", function() {
		backend.expect('POST', '/list/').respond({"id": 3, "name": "Projekt", "todo": 0})
		mockScope.list = {};
		mockScope.list.name = 'Projekt'
		mockScope.addList(mockScope.list.name)
		backend.flush()
		expect(mockScope.data.list.length).toEqual(3)
		expect(mockScope.list.name).toEqual('')
	});

	it("usuwanie listy", function() {
		backend.expect('DELETE', '/list/2/').respond(201, 'succes')
		mockScope.deleteList(mockScope.data.list[1]);
		backend.flush();
		expect(mockScope.data.list.length).toEqual(1)
	});

	it("zmiana url", function() {
		mockScope.redirect(1)
		expect(mockLocation.path()).toEqual('/list/1')
	});
});