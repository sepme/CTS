$(window).on("load", function () {
    init_windowSize();
    load_dialog();
    // $("*").persiaNumber();
}).on("resize", function () {
    init_windowSize();
    load_dialog();
});


function CountDown(min, hour, day) {
    let day_div = $(".preview-question .left-time-counter .day .count");
    let hour_div = $(".preview-question .left-time-counter .hour .count");
    let min_div = $(".preview-question .left-time-counter .minute .count");

    let new_day = day_div.html();
    let new_hour = hour_div.html();
    let new_min = min_div.html();

    function counter() {
        new_min = new_min - 1;
        if (new_min === -1) {
            new_hour = new_hour - 1;
            new_min = 59;
        }
        min_div.html(new_min);
        if (new_hour === -1) {
            new_day = new_day - 1;
            new_hour = 23;
        }
        hour_div.html(new_hour);
        day_div.html(new_day);
        // $("*").persiaNumber();
    }

    // $("*").persiaNumber();
    setInterval(counter, 1000 * 60);
}

CountDown();
$(".preview-project").click(function () {
    const dialog = $(".showProject");
    if ($(this).attr('value') == "myproject")
        return;
    $("#project_id").attr('value', $(".chamran-btn-info").attr("id"));
    $("#apply_project_id").attr('value', $(".chamran-btn-info").attr("id"));
    /*
     * reset All data
     */
    dialog.find(".techniques").html("");
    /*
     * end of reset
     */
    var id = $(this).attr("id");
    console.log("id");
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
                dialog.find(".keywords").append(
                    "<span class='border-span'>" +
                    keys[i]
                    + "</span>"
                );
            }
            if (data.status == "waiting" || data.status == "involved") {
                console.log(data.status);
                $('.vote').remove();
                $('.apply').remove();
            }
            setMajors(data);
            setValue(data);
            setComment(data.comments);
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
        "<div class='answer'>" +
        data.required_technique +
        "</div>" +
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

function setComment(data) {
    let comments_code = "";
    for (let i = 0; i < data.length; i++) {
        if (data[i].sender_type === "expert") { //expert
            let comment_body_classes = "comment-body";
            if (data[i].attachment !== "None") {
                comment_body_classes += " attached";
            }
            comments_code += "<div class='expert-comment' dir='ltr' id='" + data[i].pk + "' >" +
                "<div class='" + comment_body_classes + "'>" +
                "   <span class='comment-tools'>" +
                // "       <i class='fas fa-reply'>" +
                // "           <div class='reply'></div>" +
                // "       </i>" +
                "</span>";
            if (data[i].attachment !== "None") {
                comments_code += "<a href='/" + data[i].attachment + "' class='attached-file'>" +
                    "   <i class='fas fa-paperclip'></i>" +
                    "   <span>" + data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1) + "</span>" +
                    "</a>";
            }
            comments_code += "<pre>" + data[i].description + "</pre>" +
                "   </div>" +
                "</div>";
        } else if (data[i].sender_type === "researcher") { //researcher
            let comment_body_classes = "comment-body";
            if (data[i].attachment !== "None") {
                comment_body_classes += " attached";
            }
            comments_code += "<div class='my-comment' id='" + data[i].pk + "' >" +
                "<div class='" + comment_body_classes + "' dir='ltr'>" +
                "   <span class='comment-tools'>" +
                "       <div class='btn-group dropright'>" +
                "           <button type='button' class='dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
                "               <i class='fas fa-cog'></i>" +
                "           </button>" +
                "           <div class='dropdown-menu'>" +
                // "               <div class='dropdown-item'>" +
                // "                   <i class='fas fa-pen'></i>" +
                // "                   <span>ویرایش پیام</span>" +
                // "               </div>" +
                "               <div class='dropdown-item'>" +
                "                   <i class='fas fa-trash-alt'></i>" +
                "                   <span>حذف پیام</span>" +
                "               </div>" +
                "           </div>" +
                "       </div>" +
                // "       <i class='fas fa-reply'>" +
                // "           <div class='reply'></div>" +
                // "       </i>" +
                "   </span>";
            if (data[i].attachment !== "None") {
                comments_code += "<a href='/" + data[i].attachment + "' class='attached-file'>" +
                    "   <i class='fas fa-paperclip'></i>" +
                    "   <span>" + data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1) + "</span>" +
                    "</a>";
            }
            comments_code += "<pre>" + data[i].description + "</pre>" +
                "   </div>" +
                "</div>";
        } else { //system
            comments_code += "<div class='my-comment'>" +
                "<div class='comment-body' dir='ltr'>" +
                "<pre>" +
                data[i].description +
                "</pre>" +
                "</div>" +
                "</div>";
        }
    }
    $('.comments').html(comments_code);
    $(".comments .fa-trash-alt").closest(".dropdown-item").click(function () {
        deleteComment($(this).closest('.my-comment'));
    });
}

$(".trash").click(function (event) {
    let comment_id = $(this).attr('id');
    $.ajax({
        method: 'POST',
        url: "/researcher/delete_comment",
        dataType: 'json',
        data: {comment_id: comment_id},
        success: function (data) {
            console.log("seccessful");
        },
        error: function (data) {
            console.log("Error");
        }
    });
});

$(document).ready(function () {
    // variable
    init_setup();
    edu_count = 0;
    exe_count = 0;
    stu_count = 0;
    init_dialog_btn(".message-body button, .message-body-sm button", ".message-show");
    init_dialog_btn(".add-new-technique", ".add-technique");
    init_dialog_btn(".new-review-request", ".review-request");
    init_dialog_btn(".send-answer", ".thanks_response");
    init_dialog_btn(".start-question", ".confirmation");
    init_dialog_btn(".education-btn", ".scientific_form");
    init_dialog_btn(".executive-btn", ".executive_form");
    init_dialog_btn(".research-btn", ".research_form");
    init_dialog_btn(".technique", ".technique-dialog-main");
    input_focus();
    search_input(".search_message");
    question();
    $('.content').scroll(function () {
        if ($(".content").scrollTop() > 300) {
            $("a.top-button").addClass('show');
        } else {
            $("a.top-button").removeClass('show');
        }
    });
    $(".new-review-request").click(function () {
        $("#technique_id").attr('value', $(this).attr('id'));
    });
    $('input#upload-input').change(function (event) {
        $("img.profile").fadeIn("fast").attr('src', URL.createObjectURL(event.target.files[0]));
    });
    if ($(window).width() < 575.98) {
        $(".main").removeClass("blur-div");
        $("#toggle").click(function () {
            if ($(".side-bar").hasClass("show")) {
                $(".side-bar").removeClass("show");
                $(this).removeClass("on");
                $(".content").removeClass("blur-div");
            } else {
                $(".side-bar").addClass("show");
                $(this).addClass("on");
                $(".content").addClass("blur-div");
            }
        });
    } else {
        init_windowSize();
        init_dialog_btn(".preview-project", ".showProject");
        // $(".form-submit").click(function () {
        //     blur_div_toggle(".top-bar");
        //     blur_div_toggle(".side-bar");
        //     $(".mainInfo-body").css("display", "none");
        // });

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


$(".submit-button").click(function (event) {
    event.preventDefault();
    let voteForm = $(this).closest("form");
    let data = voteForm.serialize();
    console.log(data);
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        success: function (data) {

        },
        error: function (data) {

        },
    })
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
    var data = $(this).serialize().toString();
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
                $(".scientific_form").removeClass("show");
                $(".main").removeClass("blur-div");
                show_scientific_record(data.pk);
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
    var data = $(this).serialize().toString();
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
                $(".research_form").removeClass("show");
                $(".main").removeClass("blur-div");
                show_research_record(data.pk);
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
    var data = $(this).serialize().toString();
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
                $(".executive_form").removeClass("show");
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

// Techniques Search Input
if (window.location.href.indexOf("researcher/technique/") > -1) {
    $("#technique-name").on("focus", function () {
        if ($(this).hasClass("expand")) {
            console.log("f");
            $(this).closest("div").find(".all-techniques").css("border-color", "#3CCD1C");
        }
    }).on("focusout", function () {
        if ($(this).hasClass("expand")) {
            console.log("o");
            $(this).closest("div").find(".all-techniques").css("border-color", "#bdbdbd");
        }
    });
}

var technique_review = $('#technique_review');
technique_review.submit(function (event) {
    event.preventDefault();
    technique_review.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    technique_review.find("button[type='reset']").attr("disabled", "true");
    technique_review.find("label").addClass("progress-cursor");
    technique_review.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = technique_review.attr('url');
    // var data = $(this).serialize().toString();
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
            console.log(data);
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
});

function show_add_technique_record(title) {
    let newTechnique = "" +
        "<div class='card box flow-root-display w-100'>" +
        "    <div class='box-header text-right'>" +
        "        <h6>" + title + "</h6>" +

        "    </div>" +
        "    <div class='box-body'>" +
        "        <div class='row'>" +
        "            <div class='col-md-6 col-8'>" +
        "                <div class='row'>" +
        "                    <div class='col-6'>" +
        "                        <div class='date text-center'>" +
        "                            <div class='label'>ثبت</div>" +
        "                            <div class='value'>" +
        "                                <span>امروز</span>" +
        "                            </div>" +
        "                        </div>" +
        "                    </div>" +
        "                    <div class='col-6 text-center'>" +
        "                        <div class='label'>سطح تسلط</div>" +
        "                        <div class='value'>" +
        "                            <span>" +
        "در حال بررسی...                               " +
        "                            </span>" +
        "                        </div>" +
        "                    </div>" +
        "                </div>" +
        "            </div>" +
        "        </div>" +
        "    </div>" +
        "</div>";
    $(".techniques-list .no-project-container").remove();
    $(".techniques-list").append(newTechnique);
}

let add_technique_form = $('.ajax-add-technique-form');
add_technique_form.submit(function (event) {
    event.preventDefault();
    add_technique_form.find("button[type='submit']").addClass("loading-btn").attr("disabled", "true").css("color", "transparent");
    add_technique_form.find("button[type='reset']").attr("disabled", "true");
    add_technique_form.find("label").addClass("progress-cursor");
    add_technique_form.closest(".fixed-back").find(".card").addClass("wait");
    let $thisURL = add_technique_form.attr('url');
    // var data = $(this).serialize().toString();
    let data = new FormData(add_technique_form.get(0));
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
            console.log(data);
            // Todo : Plz send link of techniques for me here Ali Agha! :D
            add_technique_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            add_technique_form.find("button[type='reset']").prop("disabled", false);
            add_technique_form.find("input").prop("disabled", false).removeClass("progress-cursor");
            add_technique_form.find("label").removeClass("progress-cursor");
            add_technique_form.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".add-technique").css("display", "none");
                $(".main").removeClass("blur-div");
                show_add_technique_record(data.title);
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

function addComment(data) {
    new_comment = "<div class='my-comment' id='" + data.pk + "' >" +
        "<div class='comment-body' dir='ltr'>" +
        "<span class='comment-tools'>"
    // "<i class='fas fa-trash-alt'></i>" +
    // "<i class='fas fa-pen'>" +
    // "</i>" +
    // "<i class='fas fa-reply'><div class='reply'></div>" +
    // "</i>"
    ;
    if (data.attachment !== "None") {
        new_comment += "<a href='/" +
            data.attachment +
            "'><i class='fas fa-paperclip'></i></a>";
    }
    new_comment += "</span>" +
        "<span>" +
        data.description +
        "</span>" +
        "</div>" +
        "</div>";
    $(".comments").append(new_comment);
}

var comment_form = $('#comment-form');
comment_form.submit(function (event) {
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
            addComment(data);
            iziToast.success({
                rtl: true,
                message: "پیام با موفقیت ارسال شد!",
                position: 'bottomLeft'
            });
            comment_form[0].reset();
            $(".comments .fa-trash-alt").closest(".dropdown-item").click(function () {
                deleteComment($(this).closest('.my-comment'));
            });
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

var apply_form = $(".apply_Project");
apply_form.submit(function (event) {
    event.preventDefault();
    var url = apply_form.attr('url');
    var data = $(this).serialize().toString();
    $.ajax({
        method: "POST",
        dataType: "json",
        data: data,
        url: url,
        success: function (data) {
            $("input#most_hours").removeClass("error");
            $("input#least_hours").removeClass("error");
            $(".apply").hide();
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            if (obj.least_hours) {
                $("#least_hours").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.least_hours + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#least_hours").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.most_hours) {
                $("#most_hours").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.most_hours + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#most_hours").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
        }
    })
});

$(".add-new-technique").click(function (event) {
    $.ajax({
        method: 'GET',
        url: '/researcher/show_technique/',
        dataType: 'json',
        data: {'id': "None"},
        success: function (data) {
            let source = [];
            for (let i = 0; i <= Object.keys(data).length - 1; i++) {
                let item = {};
                item["title"] = Object.keys(data)[i];
                item["key"] = i + 1;
                if (Object.values(data)[i].length) {
                    item["folder"] = true;
                    let children = [];
                    for (let j = 0; j < Object.values(data)[i].length; j++) {
                        let child_item = {};
                        child_item["title"] = Object.values(data)[i][j];
                        child_item["key"] = i + "." + j;
                        children.push(child_item);
                    }
                    item["children"] = children;
                }
                source.push(item);
            }

            $("#fancy-tree").fancytree({
                extensions: ["glyph"],
                checkbox: false,
                selectMode: 1,
                checkboxAutoHide: true,
                clickFolderMode: 2,
                lazyLoad: function (event, data) {
                    data.result = {url: 'https://cdn.rawgit.com/mar10/fancytree/72e03685/demo/ajax-sub2.json'};
                },
                select: function (event, data) {

                },
                activate: function (event, data) {
                    let node = data.node;
                    $("input#technique-name").val(node.title);
                    express();
                    input_focus();
                    let inputLabel = "label[for='#technique-name']";
                    $(inputLabel).css({
                        "color": "#8d8d8d"
                    });
                },
                source: source,
                glyph: {
                    preset: "awesome5",
                    map: {
                        _addClass: "",
                        checkbox: "fas fa-square",
                        checkboxSelected: "fas fa-check-square",
                        checkboxUnknown: "fas fa-square",
                        radio: "fas fa-circle",
                        radioSelected: "fas fa-circle",
                        radioUnknown: "fas fa-dot-circle",
                        dragHelper: "fas fa-arrow-right",
                        dropMarker: "fas fa-long-arrow-right",
                        error: "fas fa-exclamation-triangle",
                        expanderClosed: "fas fa-chevron-left",
                        expanderLazy: "fas fa-angle-right",
                        expanderOpen: "fas fa-chevron-down",
                        loading: "fas fa-spinner fa-pulse",
                        nodata: "fas fa-meh",
                        noExpander: "",
                        // Default node icons.
                        // (Use tree.options.icon callback to define custom icons based on node data)
                        doc: "fas fa-screwdriver",
                        docOpen: "fas fa-screwdriver",
                        folder: "fas fa-folder",
                        folderOpen: "fas fa-folder-open"
                    }
                },
            });
        },
    });
});

function ShowPreviousProject(project) {
    show_project = "<div class='card project-item'>" +
        "<span class='header'>" +
        project.project_title +
        "<span class='sub-header'>(" +
        project.started +
        " قبل )</span></span>" +
        "<span><i class='fas fa-calendar-alt'></i>این پروژه به  <span>8 ساعت</span> وقت در هفته نیاز دارد!</span>" +
        "<span><i class='fas fa-hourglass-end'></i>تا اتمام پروژه <span>" + project.finished + "</span> فرصت باقی است!</span>" +
        "<span><i class='fas fa-hourglass-end'></i>درأمد : <span>" + project.income + "</span> کسب کرده اید.</span>" +
        "<span><i class='fas fa-hourglass-end'></i>تکنیک های مورد استفاده : <span>" + project.technique + "</span></span>" +
        "<button type='button' class='chamran-btn-info' id='" + project.PK + "'>مشاهده</button>" +
        "</div>";
    return show_project;
}

$("#done-project").click(function (event) {
    $(".new-projects").attr("style", "display :none");
    $(".your-project").attr("style", "display :none");
    $(".done-project").attr("style", "display :block");
    // $.ajax({
    //     method: 'GET',
    //     url: '/researcher/doneProject/',
    //     dataType: 'json',
    //     success: function (data) {
    //         console.log(data);
    //         var adding = "";
    //         for (var key in data.project_list) {
    //             const element = data.project_list[key];
    //             adding = adding + ShowPreviousProject(element);
    //         }
    //         console.log(adding);
    //         $(".done-project").html(adding);
    //     },
    //     error: function (data) {
    //         console.log('You don\'t have any project.');
    //     },
    // });
});

function ShowMyProject(project) {
    show_project = "<div class='card project-item'>" +
        "<span class='header'>" +
        project.project_title +
        "<span class='sub-header'>(" +
        project.started +
        " قبل )</span></span>" +
        "<span><i class='fas fa-calendar-alt'></i>این پروژه به  <span>8 ساعت</span> وقت در هفته نیاز دارد!</span>" +
        "<span><i class='fas fa-hourglass-end'></i>تا اتمام پروژه <span>" + project.finished + "</span> فرصت باقی است!</span>" +
        "<button type='button' class='chamran-btn-info my-project' id='" + project.PK + "'>مشاهده</button>" +
        "</div>";
    return show_project;
}

$("#your-project").click(function (event) {
    $(".new-projects").attr("style", "display :none");
    $(".done-project").attr("style", "display :none");
    $(".your-project").attr("style", "display :block");
    // $.ajax({
    //     method: 'GET',
    //     url: '/researcher/myProject/',
    //     dataType: 'json',
    //     success: function (data) {
    //         console.log(data);
    //         var adding = "";
    //         for (var key in data.project_list) {
    //             const element = data.project_list[key];
    //             adding = adding + ShowMyProject(element);
    //         }
    //         $(".your-project").html(adding);
    //         // $(".your-project").append(adding);
    //     },
    //     error: function (data) {
    //         console.log('You don\'t have any project.');
    //     },
    // });
});

$(".my-project").click(function () {
    const dialog = $(".showProject");
    let projectId = $(this).attr("id");
    $.ajax({
        method: 'GET',
        url: '/researcher/myProject/',
        data: {id: projectId},
        dataType: 'json',
        success: function (data) {
            dialog.find(".project-title").html(data.project_title_persian + " (" + data.project_title_english + ")");
            dialog.find(".establish-time .time-body").html(data.submission_date);
            dialog.find(".time-left .time-body").html(data.deadline);
            const keys = data.key_words;
            for (let i = 0; i < keys.length; i++) {
                dialog.find(".keywords").append(
                    "<span class='border-span'>" +
                    keys[i]
                    + "</span>"
                );
            }
            setMajors(data);
            setValue(data);
            setComment(data.comments);

            $(".apply").remove();
            if (data.vote === "false") {
                $(".vote").remove();
            }
        },
        error: function (data) {
            console.log('You don\'t have any project.');
        },
    });

});

function deleteComment(comment) {
    $.ajax({
        method: 'POST',
        url: '/deleteComment/',
        dataType: 'json',
        data: {id: $(comment).attr("id")},
        success: function (data) {
            $(comment).remove()
            iziToast.success({
                rtl: true,
                message: "پیام با موفقیت پاک شد.",
                position: 'bottomLeft'
            });
        },
        error: function (data) {
            console.log('Error');
        },
    });
}

$("#new-projects").click(function (event) {
    $(".new-projects").attr("style", "display :block");
    $(".done-project").attr("style", "display :none");
    $(".your-project").attr("style", "display :none");
});