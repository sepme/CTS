$(document).ready(function(){
  var sideBar = $(".side-bar");
  $(".menu").click(function() {
    if(sideBar.hasClass('min')) {
      sideBar.removeClass('min');
      sideBar.css("width","250px");
      $(".menu").css("right","250px");
      $(".chamranteam").attr("src","img/logoName.png");
    }else {
      sideBar.addClass('min');
      sideBar.css("width","120px");
      $(".menu").css("right","120px");
      // $(".chamranteam").attr("src","img/logo.png");

    }
  });
});
