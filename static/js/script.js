$(document).ready(function(){
  $username = $(".username input");
  $password = $(".password input");
  $username.on('focus', function() {
    if($(window).width() < 600) {
      $(".username label").css({
        "font-size":"15px",
        "top":"149px",
        "right":"5px",
        "color":"#3CCD1C"
      });
    } else {
      $(".username label").css({
        "font-size":"15px",
        "top":"149px",
        "right":"25px",
        "color":"#3CCD1C"
      });
    }
    $('.username i').css("color","#3CCD1C");
  }).on('focusout', function() {
    $('.username i').css("color","#bdbdbd");
    $(".username label").css({
      "color":"#bdbdbd"
    });
    if($username.val() === '') {
      if($(window).width() < 600) {
        $(".username label").css({
          "font-size":"17px",
          "top":"177px",
          "right":"10px",
          "color":"#bdbdbd"
        });
      } else {
        $(".username label").css({
          "font-size":"17px",
          "top":"177px",
          "right":"35px",
          "color":"#bdbdbd"
        });
      }
    }
  });
  $password.on('focus', function() {
    $('.password i').css("color","#3CCD1C");
    if($(window).width() < 600) {
      $(".password label").css({
        "font-size":"15px",
        "top":"209px",
        "right":"5px",
        "color":"#3CCD1C"
      });
    }else {
      $(".password label").css({
        "font-size":"15px",
        "top":"209px",
        "right":"25px",
        "color":"#3CCD1C"
      });
    }
  }).on('focusout', function() {
    $('.password i').css("color","#bdbdbd");
    $(".password label").css({
      "color":"#bdbdbd"
    });
    if($password.val() === '') {
      if($(window).width() < 600) {
        $(".password label").css({
          "font-size":"17px",
          "top":"237px",
          "right":"10px"
        });
      }else {
        $(".password label").css({
          "font-size":"17px",
          "top":"237px",
          "right":"35px"
        });
      }
    }
  });
});
