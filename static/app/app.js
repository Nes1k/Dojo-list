(function(){
	angular.module('dojoApp', ['ngRoute', 'restangular'])
		.config(['RestangularProvider',function(RestangularProvider) {
			RestangularProvider.setRequestSuffix('/')
		}])
		.config(['$routeProvider',function($routeProvider) {
			$routeProvider
				.when('/:id',{

				})
		}])
		.factory('baseList', ['Restangular', function(Restangular){
			return Restangular.service('list');
		}])
		.controller('baseCtrl', ['$scope', '$location', 'baseList', function($scope, $location, baseList){
			$scope.data = {};
			$scope.edited = '';

			baseList.getList().then(function(list){
				$scope.data.list = list;
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
				$location.path('/' + id)
			}
		}])
		.controller('actionListCtrl', ['$scope', 'baseList', function($scope, baseList){
			baseList.one('1').getList('actions').then(function(data){
				$scope.actions = data;
			})
		}])
})()