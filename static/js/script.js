function back() {
    $(".login-div").css("display","block");
    $(".forget-pass").css("display","block");
    $(".signUp-div").css("display","none");
    $(".email").css("display","none");
    $(".new-user").html("کاربر جدید هستید؟ <a href='#' onclick='signUp()' class='sign-up'>عضویت</a>");
    $("button").text("ورود").removeClass("signUp-btn").addClass("Enter-btn");
}
function signUp() {
    $(".login-div").css("display","none");
    $(".forget-pass").css("display","none");
    $(".signUp-div").css("display","block");
    $(".email").css("display","block");
    $(".new-user").html("<a href='#' class='back-login' onclick='back()'><i class='fas fa-arrow-left'></i> بازگشت</a>");
    $("button").text("عضویت").removeClass("Enter-btn").addClass("signUp-btn");
}
function input_focus(){
    if( $("input,textarea").prop("disabled") ) {
        $(this).each(function () {
            var inputLabel = "label[for='"+$(this).attr("id")+"']";
            $(inputLabel).css({
                "font-size":"13px",
                "top":"3px",
                "right":"5px",
                "color":"#8d8d8d"
            });
        });
    }
    $("input,textarea").each(function () {
        var inputLabel = "label[for='"+$(this).attr("id")+"']";
        if($(this).val() !== ''){
            $(inputLabel).css({
                    "font-size":"12px",
                    "top":"3px",
                    "right":"5px",
                    "color":"#6f7285"
                });
        }
        if( $(this).hasClass("error") ) {
            $(inputLabel).css("color","#ff4545");
        }
    }).on("focus", function () {
        var inputLabel = "label[for='"+$(this).attr("id")+"']";
        if($(this).hasClass("solid-label")) {
            return false;
        } else if($(this).hasClass("error")) {
            var errorDiv = $(this).next(".error");
            $(this).on("change", function () {
            if( $(this).hasClass("error") ) {
                $(this).removeClass("error");
                $(errorDiv).remove();
            }
        });
        } else{
            $(inputLabel).css({
                "font-size":"12px",
                "top":"3px",
                "right":"5px",
                "color":"#3CCD1C"
            });
            $(this).css("color","#3ccd1c");
        }
    }).on("focusout", function () {
        var inputLabel = "label[for='"+$(this).attr("id")+"']";
        if($(this).hasClass("solid-label")){
            return false;
        } else if($(this).hasClass("error")) {

        } else {
            $(inputLabel).css("color","#6f7285");
            if($(this).val() === ''){
                $(inputLabel).css({
                    "font-size":"13px",
                    "top":"31px",
                    "right":"10px",
                    "color":"#6f7285"
                });
            }else {
                $(this).css("color","#8d8d8d");
                $(inputLabel).css("color","#8d8d8d");
            }
        }
    });
}
$(window).on("load", function () {
    input_focus();
});
$(document).ready(function(){
    input_focus();
    $("input:radio[name='user-type']").change(function () {
        $user_id = $("input[type='radio']:checked+label").attr("for");
        if($user_id === "researcher"){
            $(".exper").removeClass("select");
            $(".industry").removeClass("select");
        } else if($user_id === "expert"){
            $(".researcher").removeClass("select");
            $(".industry").removeClass("select");
        } else if($user_id === "industry"){
            $(".researcher").removeClass("select");
            $(".expert").removeClass("select");
        }
    });
    $(".researcher").hover(function () {
       $(this).addClass("select");
    }, function () {
        if($("input[type='radio']:checked+label").attr("for") !== "researcher") {
            $(this).removeClass("select");
        }
    });
    $(".expert").hover(function () {
        $(this).addClass("select");
    }, function () {
        if($("input[type='radio']:checked+label").attr("for") !== "expert") {
            $(this).removeClass("select");
        }
    });
    $(".industry").hover(function () {
        $(this).addClass("select");
    }, function () {
        if($("input[type='radio']:checked+label").attr("for") !== "industry") {
            $(this).removeClass("select");
        }
    });
});

var myForm = $('.sign-up-ajax');
myForm.submit(function (event) {
    event.preventDefault();
    // var formData = $(this).serialize();
    // var major = $("#edu-subject").val();
    // var degree = $("#edu-section").val();
    // var university = $("#university").val();
    // var city = $("#edu-city").val();
    // var date_of_graduation = $("#edu-year").val();
    var $thisURL = myForm.attr('data-url');
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: $(this).serialize(),
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            alert(data.success)
        },
        error: function (data) {
            console.log(data)
        },
    })
});