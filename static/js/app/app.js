(function(){
	angular.module('dojoApp', ['ngRoute', 'restangular'])
		.config(['RestangularProvider',function(RestangularProvider) {
			RestangularProvider.setRequestSuffix('/')
		}])
		.config(['$routeProvider',function($routeProvider) {
			$routeProvider
				.when('/list/:id',{
				})
				.otherwise({})
		}])
		.factory('baseList', ['Restangular', function(Restangular){
			return Restangular.service('list');
		}])
		.controller('baseCtrl', function($scope, $location, baseList){
			$scope.data = {};
			$scope.edited = '';

			baseList.getList().then(function(list){
				$scope.data.list = list;
				$scope.data.inbox = list[0].id;
			})

			$scope.setEditedList = function(id){
				$scope.edited = id;
			}

			$scope.saveChanges = function(item){
				item.put().then(function(){
					$scope.edited = '';
				})
			}

			$scope.addList = function(list){
				baseList.post(list).then(function(new_list){
					$scope.data.list.push(new_list)
					$scope.list.name = '';
				})
			}

			$scope.deleteList = function(list){
				list.remove().then(function(){
					$scope.data.list.splice($scope.data.list.indexOf(list), 1);
				})
			}
			$scope.redirect = function(id){
				$location.path('list/' + id)
			}
		})
		.controller('actionListCtrl', function($scope, $route, $location, $routeParams, baseList){
			$scope.edited = '';

			$scope.$on('$routeChangeSuccess', function(){
				if($location.path().indexOf('/list/') == 0){
					var id = $routeParams['id']
				} else {
					var id = 1;
				}
				baseList.one(id).getList('actions').then(function(data){
					$scope.actions = data;
				})
			});
			$scope.addAction = function(item){
				$scope.actions.post(item).then(function(data){
					$scope.actions.push(data);
					$scope.action ={};
				})
			}

			$scope.saveAction = function(item){
				item.put().then(function(){
					$scope.edited = '';
				})
			}

			$scope.editAction= function(id){
				$scope.edited = id;
			}

			$scope.doneAction = function(item){
				item.put();
			}

			$scope.deleteAction = function(item){
				item.remove().then(function(){
					$scope.actions.splice($scope.actions.indexOf(item), 1);
				})
			}
		})
})()