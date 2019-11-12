$(window).on("load", function () {
    init_windowSize();
    load_dialog();
}).on("resize", function () {
    init_windowSize();
    load_dialog();
});

$(".chamran-btn-info").click(function () {    
    const dialog = $(".showProject");
    $("#project_id").attr('value', $(".chamran-btn-info").attr("id"));
    /*
     * reset All data
     */
    dialog.find(".techniques").html("");
    /*
     * end of reset
     */
    var id = $(this).attr("id");
    $.ajax({
        method: 'GET',
        url: '/researcher/show_project/',
        dataType: 'json',
        data: {'id': id},
        success: function (data) {
            dialog.find(".project-title").html(data.project_title_persian + " (" + data.project_title_english + ")");
            dialog.find(".establish-time .time-body").html(data.submission_date);
            dialog.find(".time-left .time-body").html(data.deadline);
            const keys = data.key_words;//[0].split(",");
            for (let i = 0; i < keys.length; i++) {
                dialog.find(".techniques").append(
                    "<span class='border-span'>" +
                    keys[i]
                    + "</span>"
                );
            }            
            setMajors(data);
            setValue(data);
        },
        error: function (data) {
            console.log("error");
        },
    });
});

function setRole(data) {
    role = "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "از لحاظ نکات اخلاقی (کار با نمونه انسانی، حیوانی، مواد رادیواکتیو و...)، پروژه شما با چه چالش هایی روبه رو است؟" +
        "</div>" +
        "<div class='answer'>" +
        data.policy +
        "</div></div>";
    $(".project-info-content").html(role);
}

function setResources(data) {
    resources = "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "جهت انجام پروژه خود به چه امکانات یا آزمایشگاه هایی احتیاج دارید؟" +
        "</div>" +
        "<div class='answer'>" +
        data.required_lab_equipment +
        "</div>" +
        "</div>" +
        "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "جهت انجام پروژه خود به چه تخصص ها و چه تکنیک ها آزمایشگاهی ای احتیاج دارید؟" +
        "</div>" +
        "<div class='answer required_technique'></div>"+
        "</div>" +
        "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "لطفا مراحل انجام پروژه خود را مشخص کنید." +
        "</div>" +
        "<div class='answer'>" +
        data.project_phase +
        "</div>" +
        "</div>" +
        "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "پروژه شما به چه مقدار بودجه نیاز دارد؟" +
        "</div>" +
        "<div class='answer'>" +
        data.required_budget +
        "</div>" +
        "</div>";
        const tech = data.required_technique;
        for (let i = 0; i < tech.length; i++) {
            $(".required_technique").append(
                "<span class='border-span'>" +
                tech[i]
                + "</span>"
            );
            console.log(tech[i]);
        }
    $(".project-info-content").html(resources);
}

function setApproach(data) {
    approach = "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "طفا راه حل خود را برای حل این مشکل به طور خلاصه توضیح دهید." +
        "</div>" +
        "<div class='answer'>" +
        data.approach +
        "</div>" +
        "</div>" +
        "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "این راه حل چه مشکلاتی می‌تواند داشته باشد؟" +
        "</div>" +
        "<div class='answer'>" +
        data.potential_problems +
        "</div></div>"
    $(".project-info-content").html(approach);
}

function setMajors(data) {
    majors = "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "لطفا مشکل اصلی که پروژه به حل آن پرداخته را توضیح و اهمیت آن را تبیین کنید." +
        "</div>" +
        "<div class='answer'>" +
        data.main_problem_and_importance +
        "</div></div>" +
        "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "در صورت حل این مشکل، چه پیشرفتی در شیوه های درمانی / تجهیزات پزشکی / خدمات درمانی یا ... حاصل می شود؟" +
        "</div>" +
        "<div class='answer'>" +
        data.progress_profitability +
        "</div></div>" +
        "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "برآورد شما از سود مالی این پروژه چگونه است؟" +
        "</div>" +
        "<div class='answer'>" +
        data.predict_profit +
        "</div></div>";
    $(".project-info-content").html(majors);
}

function setValue(data) {
    $("#v-pills-settings-tab").click(function () {
        setRole(data);
    });
    $("#v-pills-messages-tab").click(function () {
        setResources(data);
    });
    $("#v-pills-profile-tab").click(function () {
        setApproach(data);
    });
    $("#v-pills-home-tab").click(function () {
        setMajors(data);
    });
}

$(document).ready(function () {
    // variable
    edu_count = 0;
    exe_count = 0;
    stu_count = 0;
    init_dialog_btn(".message-body button, .message-body-sm button", ".message-show");
    init_dialog_btn(".add-new-technique", ".add-technique");
    init_dialog_btn(".new-review-request", ".review-request");
    init_dialog_btn(".send-answer", ".thanks_response");
    init_dialog_btn(".start-question", ".confirmation");
    select_technique(".select-technique");
    init_dialog_btn(".education-btn", ".scientific_form");
    init_dialog_btn(".executive-btn", ".executive_form");
    init_dialog_btn(".research-btn", ".research_form");
    init_dialog_btn(".technique", ".technique-dialog-main");
    input_focus();
    search_input(".search_message");
    question();
    $(".new-review-request").click(function(){    
        $("#technique_name").attr('value', $(this).closest(".active-question").find(".technique-title").html());
    });
    $('input#upload-input').change(function (event) {
        $("img.profile").fadeIn("fast").attr('src', URL.createObjectURL(event.target.files[0]));
    });
    if ($(window).width() < 575.98) {
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
    } else {
        init_windowSize();
        init_dialog_btn(".chamran-btn-info", ".showProject");
        $(".form-submit").click(function () {
            blur_div_toggle(".top-bar");
            blur_div_toggle(".side-bar");
            $(".mainInfo-body").css("display", "none");
        });

        // education_record();
        // executive_record();
        // studious_record();

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

var scientificForm = $('#ajax-sci-form');
scientificForm.submit(function (event) {
    event.preventDefault();
    scientificForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    scientificForm.find("button[type='reset']").attr("disabled", "true");
    scientificForm.find("label").addClass("progress-cursor");
    scientificForm.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = scientificForm.attr('url');
    var data = $(this).serialize();
    scientificForm.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        success: function (data) {
            scientificForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            scientificForm.find("button[type='reset']").prop("disabled", false);
            scientificForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            scientificForm.find("label").removeClass("progress-cursor");
            scientificForm.closest(".fixed-back").find(".card").removeClass("wait");

            if (data.success === "successful") {
                $(".scientific_form").css("display", "none");
                $(".main").removeClass("blur-div");
                show_scientific_record();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                scientificForm[0].reset();
            }
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            console.log(obj);
            scientificForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            scientificForm.find("button[type='reset']").prop("disabled", false);
            scientificForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            scientificForm.find("label").removeClass("progress-cursor");
            scientificForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.grade) {
                $("#edu-section").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.grade + "</li>" +
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
            if (obj.place) {
                $("#edu-city").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.place + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#edu-city").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.graduated_year) {
                $("#year").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.graduated_year + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#year").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
        },
    })
});

var researchForm = $('.ajax-std-form');
researchForm.submit(function (event) {
    event.preventDefault();
    researchForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    researchForm.find("button[type='reset']").attr("disabled", "true");
    researchForm.find("label").addClass("progress-cursor");
    researchForm.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = researchForm.attr('url');
    var data = $(this).serialize();
    researchForm.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
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
            if (obj.responsible) {
                $("#liable").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.responsible + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#liable").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.title) {
                $("#subject").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.title + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#subject").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.presenter) {
                $("#admin").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.presenter + "</li>" +
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

var executive_form = $('.ajax-exe-form');
executive_form.submit(function (event) {
    event.preventDefault();
    executive_form.find("button[type='submit']").addClass("loading-btn").attr("disabled", "true").css("color", "transparent");
    executive_form.find("button[type='reset']").attr("disabled", "true");
    executive_form.find("label").addClass("progress-cursor");
    executive_form.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = executive_form.attr('url');
    var data = $(this).serialize();
    executive_form.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        success: function (data) {
            executive_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            executive_form.find("button[type='reset']").prop("disabled", false);
            executive_form.find("input").prop("disabled", false).removeClass("progress-cursor");
            executive_form.find("label").removeClass("progress-cursor");
            executive_form.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".executive_form").css("display", "none");
                $(".main").removeClass("blur-div");
                show_executive_record();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                executive_form[0].reset();
            }
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            executive_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            executive_form.find("button[type='reset']").prop("disabled", false);
            executive_form.find("input").prop("disabled", false).removeClass("progress-cursor");
            executive_form.find("label").removeClass("progress-cursor");
            executive_form.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.post) {
                $("#duty").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.post + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#duty").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.start) {
                $("#from").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.start + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#from").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.end) {
                $("#until").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.end + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#until").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.place) {
                $("#workplace").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.place + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#workplace").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
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
        },
    })
});

var technique_review = $('#technique_review');
technique_review.submit(function (event) {
    event.preventDefault();
    technique_review.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    technique_review.find("button[type='reset']").attr("disabled", "true");
    technique_review.find("label").addClass("progress-cursor");
    technique_review.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = technique_review.attr('url');
    // var data = $(this).serialize();
    var data = new FormData(technique_review.get(0));
    technique_review.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        // dataType: 'json',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data) {
            technique_review.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            technique_review.find("button[type='reset']").prop("disabled", false);
            technique_review.find("input").prop("disabled", false).removeClass("progress-cursor");
            technique_review.find("label").removeClass("progress-cursor");
            technique_review.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".fixed-back").css("display", "none");
                $(".main").removeClass("blur-div");
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                technique_review[0].reset();
            }
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            technique_review.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            technique_review.find("button[type='reset']").prop("disabled", false);
            technique_review.find("input").prop("disabled", false).removeClass("progress-cursor");
            technique_review.find("label").removeClass("progress-cursor");
            technique_review.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.request_body) {
                $("#request-body").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.request_body + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                    $("input#request-body").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.request_confirmation_method) {
                $(".review-request-method").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.request_confirmation_method + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
            }
            if (obj.new_resume) {
                $("#upload-new-resume").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.new_resume + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                    $("input#upload-new-resume").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
        }
    })
})

var add_technique_form = $('.ajax-add-technique-form');
add_technique_form.submit(function (event) {
    event.preventDefault();
    add_technique_form.find("button[type='submit']").addClass("loading-btn").attr("disabled", "true").css("color", "transparent");
    add_technique_form.find("button[type='reset']").attr("disabled", "true");
    add_technique_form.find("label").addClass("progress-cursor");
    add_technique_form.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = add_technique_form.attr('url');
    // var data = $(this).serialize();
    var data = new FormData(add_technique_form.get(0));
    add_technique_form.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        // dataType: 'json',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data) {
            add_technique_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            add_technique_form.find("button[type='reset']").prop("disabled", false);
            add_technique_form.find("input").prop("disabled", false).removeClass("progress-cursor");
            add_technique_form.find("label").removeClass("progress-cursor");
            add_technique_form.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".add-technique").css("display", "none");
                $(".main").removeClass("blur-div");
                // show_add_technique_record();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                add_technique_form[0].reset();
            }
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            add_technique_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            add_technique_form.find("button[type='reset']").prop("disabled", false);
            add_technique_form.find("input").prop("disabled", false).removeClass("progress-cursor");
            add_technique_form.find("label").removeClass("progress-cursor");
            add_technique_form.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.technique) {
                $("#technique-name").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.technique + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#technique-name").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.resume) {
                $("#resume").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.resume + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#resume").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.confirmation_method) {
                $(".technique_validation").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.confirmation_method + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
            }
        },
    })
});

var comment_form = $('#comment-form');
comment_form.submit(function(event){
    event.preventDefault();
    comment_form.find("button[type='submit']").css("color", "transparent").addClass("loading-btn").attr("disabled", "true");
    comment_form.find("label").addClass("progress-cursor");
    var $thisURL = comment_form.attr('url');    
    var data = new FormData(comment_form.get(0));
    $.ajax({
        method: 'POST',        
        url: $thisURL,
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data) {
            comment_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);            
            comment_form.find("label").removeClass("progress-cursor");
            comment_form.closest(".fixed-back").find(".card").removeClass("wait");
            iziToast.success({
                rtl: true,
                message: "پیام با موفقیت ارسال شد!",
                position: 'bottomLeft'
            });
            comment_form[0].reset();
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            comment_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);            
            comment_form.find("label").removeClass("progress-cursor");
            comment_form.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.description) {
                $("#description").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.description + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("textarea#description").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
        },
    });
});

$(".add-new-technique").click(function(event) {
    console.log("add-new-technique clicked!!!");
    $.ajax({
        method: 'GET',
        url: '/researcher/show_technique/',
        dataType: 'json',
        success: function (data){
            console.log(data);
        },
    });
});