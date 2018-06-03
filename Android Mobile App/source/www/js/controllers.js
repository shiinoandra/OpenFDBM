angular.module('app.controllers', [])

.factory('connSettings', function(){
  return { ipaddr: '',  port: '' };
})


.controller('homeCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {


}])

.controller('settingsCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterNam
function ($scope, $stateParams) {


}])

.controller('aboutCtrl', ['$scope', '$stateParams', // The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams) {


}])

.controller('directionCtrl', ['$scope', '$rootScope','$http','$stateParams','connSettings',
function ($scope,  $rootScope,$http,$stateParams,connSettings) {
  $scope.directions = [{
    id: 'front',
    label: 'Front',
  }, {
    id: 'left',
    label: 'Left',
  },{
  id: 'right',
  label: 'Right',
}];
$scope.direction="";
$scope.selectedItem = $scope.directions[0].id;
$scope.switchmodel ='';

$scope.updateDirection = function(){
  var el = angular.element( document.querySelector( '#directionPie' ) );
  el.removeClass("front");
  el.removeClass("left");
  el.removeClass("right");
  el.addClass($scope.selectedItem);

  $scope.conn =connSettings;



  $http.get("http://"+$scope.conn.ipaddr+":"+$scope.conn.port+"/"+$scope.selectedItem)
  .then(function(response) {
      $scope.response = response.data;
      console.log($scope.response.status);
      if($scope.response.status=="ok")
      {
        console.log("ok");
        $scope.status_msg ="<h3  style='color:green;'>CONNECTION SUCCESSFUL</h3>";
      }
      else {
        $scope.status_msg ="<h3 style='color:red;'>CONNECTION ERROR</h3>";
        console.log($scope.status_msg);

      }
  })
  .catch(function (e)
  {
    $scope.status_msg ="<h3 class='danger'>CONNECTION ERROR</h3>";
    console.log($scope.status_msg);


  });

  $scope.direction = $scope.selectedItem;
  //$rootScope.lastselected = $scope.selectedItem.id;
  console.log($scope.direction);

}

$scope.switch = function(){
  $scope.selectedItem="front";
  $scope.conn =connSettings;

    var el = angular.element( document.querySelector( '#directionPie' ) );
    var direl = angular.element( document.querySelector( '#dirselect' ) );

    $http.get("http://"+$scope.conn.ipaddr+":"+$scope.conn.port+"/switch")
    .then(function(response) {
        $scope.response = response.data;
        console.log($scope.response.status);
        if($scope.response.status=="ok")
        {
          console.log("ok");
          $scope.status_msg ="<h3  style='color:green;'>CONNECTION SUCCESSFUL</h3>";
        }
        else {
          $scope.status_msg ="<h3 style='color:red;'>CONNECTION ERROR</h3>";
          console.log($scope.status_msg);

        }
    })
    .catch(function (e)
    {
      $scope.status_msg ="<h3 class='danger'>CONNECTION ERROR</h3>";
      console.log($scope.status_msg);


    });
    if($scope.switchmodel == true)
    {
      el.addClass("front")
      direl.removeAttr("disabled");

      // if($rootScope.lastselected != null)
      // {
      //   el.addClass("front");
      // }
      // else
      // {
      //   el.addClass("front");
      // }
    }
    else {
      direl.attr('disabled', 'disabled');

      el.removeClass("front");
      el.removeClass("left");
      el.removeClass("right");
    }

  }





}])


.controller('connCtrl', ['$scope', '$rootScope','$http','$stateParams','connSettings',
function ($scope, $rootScope,$http,$stateParams,connSettings) {

  $scope.conn =connSettings;
    $scope.conn.ipaddr =$scope.ip_addr;
    $scope.conn.port =$scope.port;

  $scope.testConn = function()
  {
    $scope.conn =connSettings;

      $scope.conn.ipaddr =$scope.ip_addr;
      $scope.conn.port =$scope.port;

      $http.get("http://"+$scope.ip_addr+":"+$scope.port+"/test_connection")
      .then(function(response) {

          $scope.response = response.data;
          console.log($scope.response.status);
          if($scope.response.status=="ok")
          {
            console.log("ok");
            $scope.status_msg ="<h3  style='color:green;'>CONNECTION SUCCESSFUL</h3 >";
          }
          else {
            $scope.status_msg ="<h3 style='color:red;'>CONNECTION ERROR</h3>";
            console.log($scope.status_msg);

          }
      })
      .catch(function (e)
      {
        $scope.status_msg ="<h3 class='danger'>CONNECTION ERROR</h3>";
        console.log($scope.status_msg);


      });


  }


}])
