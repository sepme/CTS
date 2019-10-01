$(window).on("load", function () {
    init_windowSize();
    load_dialog();
    // $(".page-loader").css("display", "none");
    // $(".main").removeClass("blur-div");
}).on("resize", function () {
    init_windowSize();
    load_dialog();
});
$(document).ready(function () {
    $('*').persiaNumber();
    input_focus();
    question_dialog_init();
    question_page_init();
    init_dialog_btn(".chamran-btn-info", ".showProject");
    init_dialog_btn(".message-body button, .message-body-sm button", ".message-show");
    init_dialog_btn(".show-btn", ".show-question");
    init_dialog_btn(".add-new-question", ".add-question");
    init_dialog_btn(".education-btn", ".scientific_form");
    init_dialog_btn(".executive-btn", ".executive_form");
    init_dialog_btn(".research-btn", ".research_form");
    init_dialog_btn(".article-btn", ".paper_form");
    init_dialog_btn(".technique", ".technique-dialog-main");
    search_input(".search_message");
    if ($(window).width() < 575.98) {
        // toggle slide-bar => all views
        $(".main").removeClass("blur-div");
        $("#toggle").click(function () {
            if ($(this).hasClass("on")) {
                $(this).removeClass("on");
                $(".side-bar").css("right", "-500px");
                $(".content").removeClass("blur-div");
            } else {
                $(this).addClass("on");
                $(".side-bar").css("right", "0");
                $(".content").addClass("blur-div");
            }
        });
        // nav-tabs change => index view
        $(".nav-link").click(function () {
            $(".nav-link").removeClass("active");
            $(this).addClass("active");
            $(".nav").animate({
                scrollLeft: $(this).offset().left
            }, "slow");
        });

    } else {
        // loading();
        $(function () {
            $('[data-toggle="tooltip"]').tooltip();
        });
        init_windowSize();
        init_dialog_btn(".researcher-card-button-show", ".researcher-info-dialog");
        $(".form-submit").click(function () {
            blur_div_toggle(".top-bar");
            blur_div_toggle(".side-bar");
            $(".mainInfo-body").css("display", "none");
        });
        $("i.fa-plus").click(function () {
            if ($("input#Uni").val() !== '') {
                div = document.createElement("div");
                $(div).addClass("uni-item");
                $(div).html("<i class='fas fa-times'></i><span>" + $("input#Uni").val() + "</span>");
                $(".selected_uni").append(div);
                $("input#Uni").val('').focus();
            }
        });
        $(".fa-times").click(function () {
            $($(".fa-times").closest(div)).remove();
        });
        $('input#upload-input').change(function (event) {
            $("img.profile").fadeIn("fast").attr('src', URL.createObjectURL(event.target.files[0]));
        });
        education_record();
        // executive_record();
        // studious_record();
        // article_record();
        $(".chamran_btn.technique").click(function () {
            $(".main").addClass("blur-div");
            $(".dialog-main").css("display", "block");
            close_dialog(".technique-dialog-main");
        });
        // $(".main").addClass("blur-div");
        // $(".dialog-main").css("display","block");
        $(".technique-list-item").click(function () {
            $(this).toggleClass("active");
            $(this).children("span").children(".fa-chevron-left").toggleClass("rotate--90");
            $(this).children(".sub-technique-list").toggleClass("display-toggle");
        });
        $("ul#project-list li a").click(function () {
            if (!$(this).hasClass("active")) {
                $("ul#project-list li a").removeClass("active");
                $(this).addClass("active");
            }
        });
    }
});

var executiveForm = $('.ajax-executive-form');
executiveForm.submit(function (event) {
    event.preventDefault();
    var $thisURL = executiveForm.attr('data-url');
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: $(this).serialize(),
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            console.log(data)
        },
        error: function (data) {
            console.log(data)
        },
    })
});

var researchForm = $('.ajax-research-form');
researchForm.submit(function (event) {
    event.preventDefault();
    var $thisURL = researchForm.attr('data-url');
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: $(this).serialize(),
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            console.log(data)
        },
        error: function (data) {
            console.log(data)
        },
    })
});

var paperForm = $('.ajax-paper-form');
paperForm.submit(function (event) {
    event.preventDefault();
    var $thisURL = paperForm.attr('data-url');
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: $(this).serialize(),
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            console.log(data)
        },
        error: function (data) {
            console.log(data)
        },
    })
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

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