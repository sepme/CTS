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
    init_dialog_btn(".paper-btn", ".paper_form");
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
        // research_record();
        // paper_record();
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

$(document).ready(function () {

    /*
    * I didn't find a better place to put this;
    * so please move this part to a section you prefer.
    * By the way, it has a big problem (expect those told earlier in comments),
    * after clicking on 'show-btn' of a new research question, 'attachments' and
    * 'answers' of the previous one is still shown (in the case the previous one had it).
    */

    $(".show-btn").click(function () {
        const dialog = $(".show-question");
        var id = $(this).attr("id");
        $.ajax({
            method: 'GET',
            url: '/expert/show_research_question/',
            dataType: 'json',
            data: {id: id},
            success: function (data) {
                if (data.question_status === "waiting") {
                    dialog.find(".question-status").html("در حال بررسی");
                } else if (data.question_status === "not_answered") {
                    dialog.find(".question-status").html("فعال");
                } else if (data.question_status === "answered") {
                    dialog.find(".question-status").html("پاسخ داده شده");
                }
                dialog.find(".card-head").html(data.question_title);
                dialog.find(".question-date").html(data.question_date);
                dialog.find("#question-body").html(data.question_body);

                if (data.question_attachment_type) {
                    dialog.find(".attach-file").attr("href", data.question_attachment_path);
                    dialog.find(".attach-name").html(data.question_attachment_name);

                    if (data.question_attachment_type === 'pdf') {
                        dialog.find(".attachment").addClass("pdf-file");
                    } else if (data.question_attachment_type === 'doc' || data.question_attachment_type === 'docx') {
                        dialog.find(".attachment").addClass("doc-file");
                    } else if (data.question_attachment_type === 'jpg' || data.question_attachment_type === 'jpeg') {
                        dialog.find(".attachment").addClass("jpg-file");
                    } else if (data.question_attachment_type === 'png') {
                        dialog.find(".attachment").addClass("png-file");
                    } /* else delete the attachments row */
                }

                var answer_list_obj = data.question_answers_list;
                if (answer_list_obj.length != 0) {
                    show_question_answers(answer_list_obj);
                } /* else show a box within "there is no answers!" */

            },
            error: function (data) {

            },
        });
    });
});

function education_record() {
    var myForm = $('.ajax-sci-form');
    myForm.submit(function (event) {
        event.preventDefault();
        myForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
            .attr("disabled", "true");
        myForm.find("button[type='reset']").attr("disabled", "true");
        myForm.find("label").addClass("progress-cursor");
        myForm.closest(".fixed-back").find(".card").addClass("wait");
        var $thisURL = myForm.attr('data-url');
        var data = $(this).serialize();
        myForm.find("input").attr("disabled", "true").addClass("progress-cursor");
        $.ajax({
            method: 'POST',
            url: $thisURL,
            dataType: 'json',
            data: data,
            // headers: {'X-CSRFToken': '{{ csrf_token }}'},
            // contentType: 'application/json; charset=utf-8',
            success: function (data) {
                myForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                    .prop("disabled", false);
                myForm.find("button[type='reset']").prop("disabled", false);
                myForm.find("input").prop("disabled", false).removeClass("progress-cursor");
                myForm.find("label").removeClass("progress-cursor");
                myForm.closest(".fixed-back").find(".card").removeClass("wait");
                if (data.success === "successful") {
                    $(".scientific_form").css("display", "none");
                    $(".main").removeClass("blur-div");
                    show_scientific_record();
                    iziToast.success({
                        rtl: true,
                        message: "اطلاعات با موفقیت ذخیره شد!",
                        position: 'bottomLeft'
                    });
                    myForm[0].reset();
                }
            },
            error: function (data) {
                var obj = JSON.parse(data.responseText);
                myForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                    .prop("disabled", false);
                myForm.find("button[type='reset']").prop("disabled", false);
                myForm.find("input").prop("disabled", false).removeClass("progress-cursor");
                myForm.find("label").removeClass("progress-cursor");
                myForm.closest(".fixed-back").find(".card").removeClass("wait");
                if (obj.city) {
                    $("#edu-city").closest("div").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.city + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $("input#edu-city").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                }
                if (obj.date_of_graduation) {
                    $("#edu-year").closest("div").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.date_of_graduation + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $("input#edu-year").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                }
                if (obj.degree) {
                    $("#edu-section").closest("div").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.degree + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $("input#edu-section").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                }
                if (obj.major) {
                    $("#edu-subject").closest("div").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.major + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $("input#edu-subject").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                }
                if (obj.university) {
                    $("#university").closest("div").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.university + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $("input#university").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                }
            },
        })
    })
}

var executiveForm = $('.ajax-executive-form');
executiveForm.submit(function (event) {
    event.preventDefault();
    executiveForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    executiveForm.find("button[type='reset']").attr("disabled", "true");
    executiveForm.find("label").addClass("progress-cursor");
    executiveForm.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = executiveForm.attr('data-url');
    var data = $(this).serialize();
    executiveForm.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            executiveForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            executiveForm.find("button[type='']").prop("disabled", false);
            executiveForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            executiveForm.find("label").removeClass("progress-cursor");
            executiveForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".executive_form").css("display", "none");
                $(".main").removeClass("blur-div");
                show_executive_record();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                executiveForm[0].reset();
            }
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            executiveForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            executiveForm.find("button[type='']").prop("disabled", false);
            executiveForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            executiveForm.find("label").removeClass("progress-cursor");
            executiveForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.city) {
                $("#exe-city").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.city + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#exe-city").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.data_end_post) {
                $("#until").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.data_end_post + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#until").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.data_start_post) {
                $("#from").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.city + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#from").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.executive_post) {
                $("#duty").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.executive_post + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#duty").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.organization) {
                $("#workplace").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.organization + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#workplace").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
        },
    })
});

var researchForm = $('.ajax-research-form');
researchForm.submit(function (event) {
    event.preventDefault();
    researchForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    researchForm.find("button[type='reset']").attr("disabled", "true");
    researchForm.find("label").addClass("progress-cursor");
    researchForm.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = researchForm.attr('data-url');
    var data = $(this).serialize();
    researchForm.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            researchForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            researchForm.find("button[type='reset']").prop("disabled", false);
            researchForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            researchForm.find("label").removeClass("progress-cursor");
            researchForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".research_form").css("display", "none");
                $(".main").removeClass("blur-div");
                show_research_record();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                researchForm[0].reset();
            }
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            researchForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            researchForm.find("button[type='reset']").prop("disabled", false);
            researchForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            researchForm.find("label").removeClass("progress-cursor");
            researchForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.co_researcher) {
                $("#liable").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.co_researcher + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#liable").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.research_title) {
                $("#research_title").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.research_title + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#research_title").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.researcher) {
                $("#admin").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.researcher + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#admin").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.status) {
                $("#rank").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.status + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#rank").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
        },
    })
});

var paperForm = $('.ajax-paper-form');
paperForm.submit(function (event) {
    event.preventDefault();
    paperForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    paperForm.find("button[type='reset']").attr("disabled", "true");
    paperForm.find("label").addClass("progress-cursor");
    paperForm.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = paperForm.attr('data-url');
    var data = $(this).serialize();
    paperForm.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            paperForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            paperForm.find("button[type='reset']").prop("disabled", false);
            paperForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            paperForm.find("label").removeClass("progress-cursor");
            paperForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".paper_form").css("display", "none");
                $(".main").removeClass("blur-div");
                show_paper_record();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                paperForm[0].reset();
            }
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            paperForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            paperForm.find("button[type='reset']").prop("disabled", false);
            paperForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            paperForm.find("label").removeClass("progress-cursor");
            paperForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.citation) {
                $("#referring-num").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.citation + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#referring-num").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.date_published) {
                $("#publish-date").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.date_published + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#publish-date").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.published_at) {
                $("#published-at").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.published_at + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#published-at").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.research_title) {
                $("#article-name").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.research_title + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#article-name").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.impact_factor) {
                $("#impact-factor").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.impact_factor + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#impact-factor").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
        },
    })
});


var ResearchQuestionForm = $('.ajax-new-rq-form');
ResearchQuestionForm.submit(function (event) {
    event.preventDefault();
    ResearchQuestionForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    ResearchQuestionForm.find("button[type='reset']").attr("disabled", "true");
    ResearchQuestionForm.find("label").addClass("progress-cursor");
    ResearchQuestionForm.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = ResearchQuestionForm.attr('data-url');
    var data = $(this).serialize();
    ResearchQuestionForm.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            ResearchQuestionForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            ResearchQuestionForm.find("button[type='reset']").prop("disabled", false);
            ResearchQuestionForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            ResearchQuestionForm.find("label").removeClass("progress-cursor");
            ResearchQuestionForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".add-question").css("display", "none");
                $(".main").removeClass("blur-div");
                show_new_research_question();
                iziToast.success({
                    rtl: true,
                    message: "سوال پژوهشی با موفیت ذخیره شد. " +
                        "لطفا منتظر تایید آن توسط ادمین بمانید.",
                    position: 'bottomLeft'
                });
                ResearchQuestionForm[0].reset();
            }
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            ResearchQuestionForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            ResearchQuestionForm.find("button[type='reset']").prop("disabled", false);
            ResearchQuestionForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            ResearchQuestionForm.find("label").removeClass("progress-cursor");
            ResearchQuestionForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.question_title) {
                    $("#question-title").closest("div").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.city + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $("input#question-title").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                }
                if (obj.question_title) {
                    $("#question-body").closest("div").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.city + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $("input#question-body").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                }
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