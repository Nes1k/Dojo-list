(function(){
	angular.module('dojoApp', ['restangular'])
		.config(['RestangularProvider',function(RestangularProvider) {
			RestangularProvider.setRequestSuffix('/')
		}])
		.factory('baseList', ['Restangular', function(Restangular){
			return Restangular.service('list');
		}])
		.controller('baseCtrl', ['$scope', 'baseList', function($scope, baseList){
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
		}])
})()