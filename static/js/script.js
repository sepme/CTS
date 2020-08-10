function back() {
    $(".login-div").css("display", "block");
    $(".forget-pass").css("display", "block");
    $(".signUp-div").css("display", "none");
    $(".email").css("display", "none");
    $(".new-user").html("کاربر جدید هستید؟ <a href='#' onclick='signUp()' class='sign-up'>عضویت</a>");
    $("button").text("ورود").removeClass("signUp-btn").addClass("Enter-btn");
}

function signUp() {
    $(".login-div").css("display", "none");
    $(".forget-pass").css("display", "none");
    $(".signUp-div").css("display", "block");
    $(".email").css("display", "block");
    $(".new-user").html("<a href='#' class='back-login' onclick='back()'><i class='fas fa-arrow-left'></i> بازگشت</a>");
    $("button").text("عضویت").removeClass("Enter-btn").addClass("signUp-btn");
}

// function input_focus() {
//     if ($("input,textarea").prop("disabled")) {
//         $(this).each(function () {
//             let inputLabel = "label[for='" + $(this).attr("id") + "']";
//             $(inputLabel).css({
//                 "font-size": "13px",
//                 "top": "3px",
//                 "right": "5px",
//                 "color": "#8d8d8d"
//             });
//         });
//     }
//     $("input,textarea").each(function () {
//         let inputLabel = "label[for='" + $(this).attr("id") + "']";
//         if ($(this).val() !== '') {
//             $(inputLabel).css({
//                 "font-size": "12px",
//                 "top": "3px",
//                 "right": "5px",
//                 "color": "#6f7285"
//             });
//         }
//         if ($(this).hasClass("error")) {
//             $(inputLabel).css("color", "#ff4545");
//         }
//     }).on("focus", function () {
//         let inputLabel = "label[for='" + $(this).attr("id") + "']";
//         if ($(this).hasClass("solid-label")) {
//             return false;
//         } else if ($(this).hasClass("error")) {
//             let errorDiv = $(this).next(".error");
//             $(this).on("change", function () {
//                 if ($(this).hasClass("error")) {
//                     $(this).removeClass("error");
//                     $(errorDiv).remove();
//                 }
//             });
//         } else {
//             $(inputLabel).css({
//                 "font-size": "12px",
//                 "top": "3px",
//                 "right": "5px",
//                 "color": "#3CCD1C"
//             });
//             $(this).css("color", "#3ccd1c");
//         }
//     }).on("focusout", function () {
//         let inputLabel = "label[for='" + $(this).attr("id") + "']";
//         if ($(this).hasClass("solid-label")) {
//             return false;
//         } else if ($(this).hasClass("error")) {
//
//         } else {
//             $(inputLabel).css("color", "#6f7285");
//             if ($(this).val() === '') {
//                 $(inputLabel).css({
//                     "font-size": "13px",
//                     "top": "31px",
//                     "right": "10px",
//                     "color": "#6f7285"
//                 });
//             } else {
//                 $(this).css("color", "#8d8d8d");
//                 $(inputLabel).css("color", "#8d8d8d");
//             }
//         }
//     });
// }

// $(window).on("load", function () {
//     input_focus();
// });
function sha256(ascii) {
    function rightRotate(value, amount) {
        return (value >>> amount) | (value << (32 - amount));
    }

    let mathPow = Math.pow;
    let maxWord = mathPow(2, 32);
    let lengthProperty = 'length';
    let i, j;
    let result = '';

    let words = [];
    let asciiBitLength = ascii[lengthProperty] * 8;

    let hash = sha256.h = sha256.h || [];
    let k = sha256.k = sha256.k || [];
    let primeCounter = k[lengthProperty];

    let isComposite = {};
    for (let candidate = 2; primeCounter < 64; candidate++) {
        if (!isComposite[candidate]) {
            for (i = 0; i < 313; i += candidate) {
                isComposite[i] = candidate;
            }
            hash[primeCounter] = (mathPow(candidate, .5) * maxWord) | 0;
            k[primeCounter++] = (mathPow(candidate, 1 / 3) * maxWord) | 0;
        }
    }

    ascii += '\x80';
    while (ascii[lengthProperty] % 64 - 56) ascii += '\x00';
    for (i = 0; i < ascii[lengthProperty]; i++) {
        j = ascii.charCodeAt(i);
        if (j >> 8) return;
        words[i >> 2] |= j << ((3 - i) % 4) * 8;
    }
    words[words[lengthProperty]] = ((asciiBitLength / maxWord) | 0);
    words[words[lengthProperty]] = (asciiBitLength);

    for (j = 0; j < words[lengthProperty];) {
        let w = words.slice(j, j += 16);
        let oldHash = hash;
        hash = hash.slice(0, 8);

        for (i = 0; i < 64; i++) {
            let i2 = i + j;
            let w15 = w[i - 15], w2 = w[i - 2];

            let a = hash[0], e = hash[4];
            let temp1 = hash[7]
                + (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25))
                + ((e & hash[5]) ^ ((~e) & hash[6]))
                + k[i]
                + (w[i] = (i < 16) ? w[i] : (
                    w[i - 16]
                    + (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3)
                        + w[i - 7]
                        + (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))
                    ) | 0
                ));
            let temp2 = (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22))
                + ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]));

            hash = [(temp1 + temp2) | 0].concat(hash);
            hash[4] = (hash[4] + temp1) | 0;
        }

        for (i = 0; i < 8; i++) {
            hash[i] = (hash[i] + oldHash[i]) | 0;
        }
    }

    for (i = 0; i < 8; i++) {
        for (j = 3; j + 1; j--) {
            let b = (hash[i] >> (j * 8)) & 255;
            result += ((b < 16) ? 0 : '') + b.toString(16);
        }
    }
    return result;
}

$(document).ready(function () {
    if (window.location.href.indexOf("login") !== -1) {
        let owl = $('.owl-carousel').owlCarousel({
            loop: false,
            margin: 10,
            nav: false,
            dots: false,
            items: 1,
            touchDrag: false,
            mouseDrag: false,
            autoHeight: true,
        });
        $('.next-slide').click(function () {
            owl.trigger('next.owl.carousel');
        });
        $('.prev-slide').click(function () {
            owl.trigger('prev.owl.carousel');
        });
        $('[data-toggle="tooltip"]').tooltip();
        if (window.location.href.indexOf("/login/#signup") !== -1) {
            owl.trigger('next.owl.carousel');
        }
    }

    // input_focus();
    $("input:radio[name='user-type']").change(function () {
        let $user_id = $("input[type='radio']:checked+label").attr("for");
        if ($user_id === "researcher") {
            $(".expert").removeClass("select");
            $(".industry").removeClass("select");
        } else if ($user_id === "expert") {
            $(".researcher").removeClass("select");
            $(".industry").removeClass("select");
        } else if ($user_id === "industry") {
            $(".researcher").removeClass("select");
            $(".expert").removeClass("select");
        }
    });
    $(".researcher").hover(function () {
        $(this).addClass("select");
    }, function () {
        if ($("input[type='radio']:checked+label").attr("for") !== "researcher") {
            $(this).removeClass("select");
        }
    });
    $(".expert").hover(function () {
        $(this).addClass("select");
    }, function () {
        if ($("input[type='radio']:checked+label").attr("for") !== "expert") {
            $(this).removeClass("select");
        }
    });
    $(".industry").hover(function () {
        $(this).addClass("select");
    }, function () {
        if ($("input[type='radio']:checked+label").attr("for") !== "industry") {
            $(this).removeClass("select");
        }
    });
});

let signupForm = $('.sign-up-ajax');
signupForm.submit(function (event) {
    event.preventDefault();
    $(".owl-carousel").css('display', "none");
    $(".check-verification-code").css("display", "block");
});

$("#verificationBtn").click(function () {
    if (sha256($("input#IntroductionCode").val()) === "1e74c3aed9796ffe939afea37b5d5f00c35e14be634c0c06d970a902b55d2c25") {
        $(".check-verification-code").css("display", "none");
        $(".loading").css('display', "block");
        $(".email").find("div.error").remove();
        $("input#email").removeClass("error").css("color", "").prev().css("color", "");
        $("input#email").next().css("color", "");
        $(".captcha-error").html("");
        let formData = signupForm.serialize().toString();
        let $thisURL = signupForm.attr('data-url');
        $.ajax({
            method: 'POST',
            url: $thisURL,
            dataType: 'json',
            data: signupForm.serialize().toString(),
            // headers: {'X-CSRFToken': '{{ csrf_token }}'},
            // contentType: 'application/json; charset=utf-8',
            success: function (data) {
                $('.circle-loader').toggleClass('load-complete');
                $('.checkmark').toggle();
                $('.loading h6').html("<span class='green'>ایمیل با موفقیت ارسال شد!</span>" +
                    "<br><br>" +
                    "<span>جهت تکمیل ثبت نام ایمیل خود را بررسی کنید!</span>");
            },
            error: function (data) {
                console.log(data);
                $(".loading").css('display', "none");
                $(".owl-carousel").css('display', "block");
                let obj = JSON.parse(data.responseText);
                if (obj.email !== undefined) {
                    $(".email").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.email + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $("input#email").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                }

                // $(".user-type-container").addClass("error-container");
                if ($(".account_error").text().length !== 0) {
                    $(".account_error").html("");
                }
                if (obj.account_type !== undefined) {
                    $(".account_error").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.account_type + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $(".user-type-container").find("label").click(function () {
                        if ($(this).closest(".user-type-container").hasClass("error-container")) {
                            $(this).closest(".user-type-container").removeClass("error-container");
                            $(".account_error").html("");
                        }
                    });
                    $(".user-type").find("svg > g").attr("fill", "#ff4545");
                    $(".user-type-container").addClass("error-container");
                }
                $("#id_captcha_1").find("div.error").remove();
                if (obj.captcha !== undefined) {
                    $(".captcha-error").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.captcha + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $("input#id_captcha_1").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                    $("input#id_captcha_1").next().css("color", "rgb(255, 69, 69)");
                }
                display_error(signupForm);
            },
        });
    } else {
        iziToast.error({
            rtl: true,
            message: "کد وارد شده اشتباه است!",
            position: 'bottomLeft'
        });
    }
});

$("#backToSignup").click(function () {
    $(".owl-carousel").css('display', "block");
    $(".check-verification-code").css("display", "none");
});

let loginForm = $('.login-ajax');
loginForm.submit(function (event) {
    $(".loading").css('display', "block");
    // $(".registration").css('display', "none");
    $(".owl-carousel").css('display', "none");
    event.preventDefault();
    // let formData = $(this).serialize().toString();
    let $thisURL = loginForm.attr('data-url');
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: $(this).serialize().toString(),
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            if (data.success === 'successful') {
                $('.circle-loader').toggleClass('load-complete');
                $('.checkmark').toggle();
                $('.loading h6').html("خوش آمدید!");
                setTimeout(
                    function () {
                        if (data.next)
                            window.location.href = data.next;
                        else
                            window.location.href = "/" + data.type;
                    }, 1000);
            } else {
                $(".loading").css('display', "none");
                $(".owl-carousel").css('display', "block");
                $(".password").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + data.error + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#password").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
        },
        error: function (data) {
            $(".loading").css('display', "none");
            $(".owl-carousel").css('display', "block");
            let obj = JSON.parse(data.responseText);
            if (obj.username !== undefined) {
                $(".username").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.username + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#username").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.password !== undefined) {
                $(".password").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.password + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#password").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            display_error(loginForm);
        },
    })
});

let recoverPassForm = $('.recover-pass');
recoverPassForm.submit(function (event) {
    $(".loading").css('display', "block");
    $(".recover-pass-container").css('display', "none");
    event.preventDefault();
    $(".error").html("");
    $("input#email").removeClass("error");
    let $thisURL = recoverPassForm.attr('data-url');
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: $(this).serialize().toString(),
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            $('.circle-loader').toggleClass('load-complete');
            $('.checkmark').toggle();
            $('.loading h6').html("ایمیل با موفقیت ارسال شد!<br>جهت بازیابی رمزعبور ایمیل خود را بررسی کنید!");
        },
        error: function (data) {
            $(".loading").css('display', "none");
            $(".recover-pass-container").css('display', "block");
            let obj = JSON.parse(data.responseText);
            $(".email").append("<div class='error'>" +
                "<span class='error-body'>" +
                "<ul class='errorlist'>" +
                "<li>" + obj.username + "</li>" +
                "</ul>" +
                "</span>" +
                "</div>");
            $("input#email").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            display_error(recoverPassForm);
        },
    })
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('#refresh-captcha').click(function () {
    let $form = $(this).parents('form');
    let thisElement = $(this);
    thisElement.find(".fa-sync-alt").addClass("fa-spin");
    $.getJSON("/captcha/refresh/", {}, function (result) {
        $('.captcha').attr('src', result['image_url']);
        $('#id_captcha_0').val(result['key']);
        thisElement.find(".fa-sync-alt").removeClass("fa-spin");
    });

    return false;
});