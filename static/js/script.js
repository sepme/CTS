function back() {
    $(".username").css("display","block");
    $(".password").css("display","block");
    $(".forget-pass").css("display","block");
    $(".signUp-div").css("display","none");
    $(".email").css("display","none");
    $(".new-user").html("کاربر جدید هستید؟ <a href='#' onclick='signUp()' class='sign-up'>عضویت</a>");
    $("button").text("ورود").removeClass("signUp-btn").addClass("Enter-btn");
}
function signUp() {
    $(".username").css("display","none");
    $(".password").css("display","none");
    $(".forget-pass").css("display","none");
    $(".signUp-div").css("display","flex");
    $(".email").css("display","block");
    $(".new-user").html("<a href='#' class='back-login' onclick='back()'><i class='fas fa-arrow-left'></i> بازگشت</a>");
    $("button").text("عضویت").removeClass("Enter-btn").addClass("signUp-btn");
}
$(document).ready(function(){
  $email = $(".email input");
  $("input").on('focus', function() {
      $className = "."+ $(this).closest("div").attr("class");
    $($className + ' i').css("color","#3CCD1C");
    if($(window).width() < 600) {
      $($className+ " label").css({
        "font-size":"15px",
        "top":"0px",
        "right":"5px",
        "color":"#3CCD1C"
      });
    }else {
      $( $className + " label").css({
        "font-size":"12px",
        "top":"0px",
        "right":"25px",
        "color":"#3CCD1C"
      });
    }
  }).on('focusout', function() {
      $className = "."+ $(this).closest("div").attr("class");
    $($className + ' i').css("color","#bdbdbd");
    $($className +" label").css({
      "color":"#bdbdbd"
    });
    if($(this).val() === '') {
      if($(window).width() < 600) {
        $($className +" label").css({
          "font-size":"13px",
          "top":"28px",
          "right":"10px"
        });
      }else {
        $($className +" label").css({
          "font-size":"13px",
          "top":"28px",
          "right":"35px"
        });
      }
    }
  });
  $email.on("focus", function () {
      $('.email i').css("color","#3CCD1C");
      $(".email label").css({
          "font-size":"15px",
          "top":"0px",
          "right":"25px",
          "color":"#3CCD1C"
      });
  }).on("focusout", function () {
      $('.email i').css("color","#bdbdbd");
      $(".email label").css("color","#bdbdbd");
    if($email.val() === ''){
        $(".email label").css({
            "font-size":"17px",
            "top":"28px",
            "right":"35px"
        });
    }else {

    }
  });
  $("input:radio[name='user-type']").change(function () {
      $user_id = $("input[type='radio']:checked+label").attr("for");
      if($user_id === "researcher"){
          $(".expert img").attr("src","img/mind.png");
          $(".industry img").attr("src","img/settings.png");
      } else if($user_id === "expert"){
          $(".researcher img").attr("src","img/research.png");
          $(".industry img").attr("src","img/settings.png");
      } else if($user_id === "industry"){
          $(".researcher img").attr("src","img/research.png");
          $(".expert img").attr("src","img/mind.png");
      }
  });
  $(".researcher").mouseover(function () {
     $(".researcher img").attr("src","img/research_hover.png");
  }).mouseleave(function () {
      if($("input[type='radio']:checked+label").attr("for") !== "researcher") {
          $(".researcher img").attr("src","img/research.png");
      }
  });
  $(".expert").mouseover(function () {
      $(".expert img").attr("src","img/mind_hover.png");
  }).mouseleave(function () {
      if($("input[type='radio']:checked+label").attr("for") !== "expert") {
          $(".expert img").attr("src","img/mind.png");
      }
  });
  $(".industry").mouseover(function () {
      $(".industry img").attr("src","img/settings_hover.png");
  }).mouseleave(function () {
      if($("input[type='radio']:checked+label").attr("for") !== "industry") {
          $(".industry img").attr("src","img/settings.png");
      }
  });
});