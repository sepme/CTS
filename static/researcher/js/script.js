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
    const dialog = $("#showProject");
    if ($(this).attr('value') === "myproject")
        return;
    let id = $(this).attr("id");
    $(".project_id").attr('value', $(".preview-project").attr("id"));
    $("#apply_project_id").attr('value', id);
    /*
     * reset All data
     */
    dialog.find(".techniques").html("");
    /*
     * end of reset
     */
    $.ajax({
        method: 'GET',
        url: '/researcher/show_project/',
        dataType: 'json',
        data: {'id': id},
        success: function (data) {
            dialog.find(".modal-header .modal-title").html(data.persian_title + "<br>" + data.english_title);
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
            console.log(data.status);
            if (data.status === "waiting" || data.status === "involved") {
                $('.vote').remove();
                $('.apply').remove();
            }
            setMajors(data);
            setValue(data);
            setComment(data.comments);
            let status = "unseen";
            dialog.find(".modal-footer button").removeClass("confirm-project btn-primary").prop("disabled", true)
                .css("opacity", 1);
            switch (status) {
                case "unseen":
                    dialog.find(".modal-footer button").html(`درخواست شما ارسال شده است!`);
                    break;
                case "pending":
                    dialog.find(".modal-footer button").html(`
                        <div class="spinner-border text-warning" style="width: 1.5rem;height: 1.5rem" role="status">
                            <span class="sr-only">Loading...</span>
                        </div>
                        <span class="text-warning">درخواست شما درحال بررسی است!</span>
                    `);
                    break;
                case "accepted":
                    dialog.find(".modal-footer button").html(`
                        <i class="fas fa-check text-success"></i>
                        <span class="text-success">درخواست شما تایید شده است!</span>
                    `);
                    break;
                case "refused":
                    dialog.find(".modal-footer button").html(`
                        <i class="fas fa-times text-danger"></i>
                        <span class="text-danger">درخواست شما رد شده است!</span>
                    `);
                    break;
                default:
                    dialog.find(".modal-footer button").removeAttr("class").addClass("btn btn-primary confirm_project")
                        .prop("disabled", false).html(`ارسال درخواست انجام پروژه`);
            }
        },
        error: function (data) {
            console.log("error");
        },
    });
});

$("#accept-project").click(function () {
    $('#showProject').modal('toggle');
    $('#projectRequest').modal('toggle');
    $('#projectRequest .close__redirect').click(function () {
        $('#projectRequest').modal('toggle');
        $('#showProject').modal('toggle');
    });
});

function setRole(data) {
    let role = "<div>" +
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
    let resources = "<div>" +
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
        "</div>";
    $(".project-info-content").html(resources);
}

function setApproach(data) {
    let approach = "<div>" +
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
        "</div></div>";
    $(".project-info-content").html(approach);
}

function setMajors(data) {
    let majors = "<div>" +
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
    init_setup();
    init_dialog_btn(".message-body button, .message-body-sm button", ".message-show");
    // init_dialog_btn(".add-new-technique", ".add-technique");
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

    function auto_focus_code(element) {
        console.log("auto focus not working correctly\nNeEd To FiX!");
        // if (element.is(":first-child")) {
        //     console.log("Yes");
        //     element.focus();
        //     return true
        // } else {
        //     console.log("No");
        //     if (element.prev().val() === "") {
        //         auto_focus_code(element.prev());
        //         console.log("=>");
        //     } else {
        //         console.log("||");
        //         element.focus();
        //     }
        // }
    }

    // if ($(".c-digit-container").length !== 0) {
    //     $(".c-digit-container .code.c-digit").bind("paste", function (e) {
    //         let pastedData = e.originalEvent.clipboardData.getData('text');
    //         let idx = $(this).index();
    //         let newData = pastedData.substring(0, 5 - idx);
    //         console.log("idx ", idx);
    //         for (let i = idx; i <= 5; i++) {
    //             console.log("i ", i);
    //             if (i === 0) {
    //                 $(".c-digit-container .code.c-digit:first-child").attr("value", pastedData.charAt(i - idx));
    //             } else {
    //                 let child_num = i + 1;
    //                 $(".c-digit-container .code.c-digit:nth-child(" + child_num + ")").attr("value", pastedData.charAt(i - idx));
    //             }
    //
    //         }
    //         console.log(newData);
    //     }).on("focus", function () {
    //         auto_focus_code($(this));
    //
    //     }).on("keyup", function () {
    //         if ($(this).val() === "") {
    //             if(!$(this).is(":first-child")) {
    //                 $(this).prev().focus();
    //             }
    //         } else {
    //             let mainInput = $(this).closest(".form-group").find("input[name='skip_code']");
    //             let last_val = mainInput.val();
    //             let idx = $(this).index();
    //             mainInput.attr("value", last_val.substring(0, idx) + ($(this).val() === "" ? " " : $(this).val()) + last_val.substring(idx + 1));
    //             if (!$(this).is(":last-child")) {
    //                 $(this).next().focus();
    //             }
    //         }
    //     });
    // }
    $(".new-review-request").click(function () {
        $("#technique_id").attr('value', $(this).attr('id'));
    });
    $('input#upload-input').change(function (event) {
        $("img.profile").fadeIn("fast").attr('src', URL.createObjectURL(event.target.files[0]));
    });

    // Check user id
    if ($("#userID").length) {
        $("input#userID").on("keyup", function () {
            console.log("search: ", $(this).val());
            $('.userId-error').remove();
            let thisFormGroup = $(this).closest(".form-group");
            if ($(this).val()) {
                thisFormGroup.find(".form-group__status").removeClass("check").removeClass("success")
                    .removeClass("fail");
                thisFormGroup.find(".form-group__status").addClass("check");
                thisFormGroup.find("input").removeClass("error");
                $.ajax({
                    method: "POST",
                    url: "/researcher/checkUserId",
                    data: {"user_id": $(this).val()},
                    success: function (data) {
                        console.log(data);
                        thisFormGroup.find(".form-group__status").removeClass("check");
                        if (data.invalid_input){
                            thisFormGroup.find(".form-group__status").addClass("fail");
                            thisFormGroup.find("input").addClass("error");
                        } else if (data.is_unique) {
                        if (data.is_unique) {
                            thisFormGroup.find(".form-group__status").addClass("success");
                        } else {
                            thisFormGroup.find(".form-group__status").addClass("fail");
                            thisFormGroup.find("input").addClass("error");
                        }
                    },
                    error: function (data) {
                        console.log(data);
                        thisFormGroup.find(".form-group__status").removeClass("check");
                        iziToast.error({
                            rtl: true,
                            message: "ارتباط با سرور با مشکل مواجه شد!",
                            position: 'bottomLeft'
                        });
                    }
                });
            } else {
                thisFormGroup.find(".form-group__status").removeClass("check").removeClass("success")
                    .removeClass("fail");
                $(this).removeClass("error");
            }
        });
    }

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
        // init_dialog_btn(".preview-project", ".showProject");
        // init_dialog_btn(".my-project", ".showProject");
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
    //****************************************//
    //  User Info
    //****************************************//

    if (window.location.href.indexOf('/researcher/userInfo/') > -1) {
        function putAttachment(element) {
            element.on("change", function () {
                let fileName = $(this).val().split("\\").pop();
                let fileSize = this.files[0].size;
                if (fileSize < 1000000) {
                    fileSize = (fileSize / 1000) + " KB";
                } else {
                    fileSize = (fileSize / 1000000) + " MB";
                }
                let fileType = returnFileType($(this).val().split('.').pop().toLowerCase());
                let attachment = `
                <div class="attach-box m-auto">
                    <span class="attach-box__img ${fileType}"></span>
                    <span class="attach-box__info">
                        <span class="attach-box__info-name">
                            ${fileName}
                        </span>
                        <span class="attach-box__info-ext">
                            ${fileSize}
                        </span>
                    </span>
                    <span class="attach-box__option">
                        <a class="attach-box__option-download" href="#">
                            <i class="fas fa-download"></i>
                        </a>
                    </span>
                </div>
                <button class="btn btn-primary mt-4" type="button" id="deleteAttachment">حذف فایل</button>
            `;
                $(this).closest(".attach__container").html(attachment);
                $("#deleteAttachment").click(function () {
                    $(this).closest(".attach__container").html(`
                    <div class="form-group text-center font-weight-bold">
                        <label class="upload-dash-box" for="uploadResume">
                            <svg width="1em" height="1em" viewBox="0 0 16 16"
                                class="bi bi-cloud" fill="currentColor"
                                xmlns="http://www.w3.org/2000/svg"
                                style="font-size: 30px">
                                <path d="M4.406 3.342A5.53 5.53 0 0 1 8 2c2.69 0 4.923 2 5.166 4.579C14.758 6.804 16 8.137 16 9.773 16 11.569 14.502 13 12.687 13H3.781C1.708 13 0 11.366 0 9.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383zm.653.757c-.757.653-1.153 1.44-1.153 2.056v.448l-.445.049C2.064 6.805 1 7.952 1 9.318 1 10.785 2.23 12 3.781 12h8.906C13.98 12 15 10.988 15 9.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 4.825 10.328 3 8 3a4.53 4.53 0 0 0-2.941 1.1z"
                                    fill-rule="evenodd"></path>
                                    </svg>
                                        انتخاب فایل
                        </label>
                        <input type="file" class="form-control-file"
                            id="uploadResume" name="resume" hidden>
                    </div>
                `);
                    putAttachment($("input#uploadResume"));
                });
            });
        }

        if ($("input#uploadResume").length) {
            putAttachment($("input#uploadResume"));
        }

        if ($("#deleteAttachment").length) {
            $("#deleteAttachment").click(function () {
                $(this).closest(".attach__container").html(`
                    <div class="form-group text-center font-weight-bold">
                        <label class="upload-dash-box" for="uploadResume">
                            <svg width="1em" height="1em" viewBox="0 0 16 16"
                                class="bi bi-cloud" fill="currentColor"
                                xmlns="http://www.w3.org/2000/svg"
                                style="font-size: 30px">
                                <path d="M4.406 3.342A5.53 5.53 0 0 1 8 2c2.69 0 4.923 2 5.166 4.579C14.758 6.804 16 8.137 16 9.773 16 11.569 14.502 13 12.687 13H3.781C1.708 13 0 11.366 0 9.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383zm.653.757c-.757.653-1.153 1.44-1.153 2.056v.448l-.445.049C2.064 6.805 1 7.952 1 9.318 1 10.785 2.23 12 3.781 12h8.906C13.98 12 15 10.988 15 9.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 4.825 10.328 3 8 3a4.53 4.53 0 0 0-2.941 1.1z"
                                    fill-rule="evenodd"></path>
                                    </svg>
                                        انتخاب فایل
                        </label>
                        <input type="file" class="form-control-file"
                            id="uploadResume" name="resume" hidden>
                    </div>
                `);
                putAttachment($("input#uploadResume"));
            });
        }

        // $("#waitToGet").click(function (event) {
        //     $(this).modal("hide");
        //     $("#resumeValidation").modal("show");
        // });
    }

    //****************************************//
    //  End User Info
    //****************************************//

});


$(".submit-button").click(function (event) {
    event.preventDefault();
    let voteForm = $(this).closest("form");
    let data = voteForm.serialize();
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

let scientificForm = $('#ajax-sci-form');
scientificForm.submit(function (event) {
    event.preventDefault();
    scientificForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    scientificForm.find("button[type='reset']").attr("disabled", "true");
    scientificForm.find("label").addClass("progress-cursor");
    scientificForm.closest(".fixed-back").find(".card").addClass("wait");
    let $thisURL = scientificForm.attr('url');
    let data = $(this).serialize().toString();
    scientificForm.find("input").attr("disabled", "true").addClass("progress-cursor");
    $("input#edu-section").removeClass("error").css("color", "").prev().css("color", "");
    $(".edu-section").find("div.error").remove();

    $("input#edu-subject").removeClass("error").css("color", "").prev().css("color", "");
    $(".edu-subject").find("div.error").remove();

    $("input#university").removeClass("error").css("color", "").prev().css("color", "");
    $(".university").find("div.error").remove();

    $("input#edu-city").removeClass("error").css("color", "").prev().css("color", "");
    $(".edu-city").find("div.error").remove();

    $("input#year").removeClass("error").css("color", "").prev().css("color", "");
    $(".year").find("div.error").remove();

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
            let obj = JSON.parse(data.responseText);
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

let researchForm = $('.ajax-std-form');
researchForm.submit(function (event) {
    event.preventDefault();
    researchForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    researchForm.find("button[type='reset']").attr("disabled", "true");
    researchForm.find("label").addClass("progress-cursor");
    researchForm.closest(".fixed-back").find(".card").addClass("wait");
    let $thisURL = researchForm.attr('url');
    let data = $(this).serialize().toString();
    researchForm.find("input").attr("disabled", "true").addClass("progress-cursor");

    $("input#liable").removeClass("error").css("color", "").prev().css("color", "");
    $(".liable").find("div.error").remove();

    $("input#subject").removeClass("error").css("color", "").prev().css("color", "");
    $(".subject").find("div.error").remove();

    $("input#admin").removeClass("error").css("color", "").prev().css("color", "");
    $(".admin").find("div.error").remove();

    $("input#rank").removeClass("error").css("color", "").prev().css("color", "");
    $(".rank").find("div.error").remove();

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
            let obj = JSON.parse(data.responseText);
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
                $("#rank").closest("div").append("<div class='rank error'>" +
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

let executive_form = $('.ajax-exe-form');
executive_form.submit(function (event) {
    event.preventDefault();
    executive_form.find("button[type='submit']").addClass("loading-btn").attr("disabled", "true").css("color", "transparent");
    executive_form.find("button[type='reset']").attr("disabled", "true");
    executive_form.find("label").addClass("progress-cursor");
    executive_form.closest(".fixed-back").find(".card").addClass("wait");
    let $thisURL = executive_form.attr('url');
    let data = $(this).serialize().toString();
    executive_form.find("input").attr("disabled", "true").addClass("progress-cursor");
    $("input#duty").removeClass("error").css("color", "").prev().css("color", "");
    $(".duty").find("div.error").remove();

    $("input#from").removeClass("error").css("color", "").prev().css("color", "");
    $(".from").find("div.error").remove();

    $("input#until").removeClass("error").css("color", "").prev().css("color", "");
    $(".until").find("div.error").remove();

    $("input#workplace").removeClass("error").css("color", "").prev().css("color", "");
    $(".workplace").find("div.error").remove();

    $("input#exe-city").removeClass("error").css("color", "").prev().css("color", "");
    $(".exe-city").find("div.error").remove();

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
            let obj = JSON.parse(data.responseText);
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

let technique_review = $('#technique_review');
technique_review.submit(function (event) {
    event.preventDefault();
    technique_review.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    technique_review.find("button[type='reset']").attr("disabled", "true");
    technique_review.find("label").addClass("progress-cursor");
    technique_review.closest(".fixed-back").find(".card").addClass("wait");
    let $thisURL = technique_review.attr('url');
    // let data = $(this).serialize().toString();
    let data = new FormData(technique_review.get(0));
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
            technique_review.closest('.date').find(".value").html("امروز")
            if (data.success === "successful") {
                $('#reviewRequest').modal('toggle');
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                technique_review[0].reset();
            }
        },
        error: function (data) {
            let obj = JSON.parse(data.responseText);
            technique_review.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            technique_review.find("button[type='reset']").prop("disabled", false);
            technique_review.find("input").prop("disabled", false).removeClass("progress-cursor");
            technique_review.find("label").removeClass("progress-cursor");
            technique_review.closest(".fixed-back").find(".card").removeClass("wait");
            technique_review.find(".error:not(input)").remove();
            $("input#request-body").removeClass("error");
            $("input#upload-new-resume").removeClass("error");
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

function show_add_technique_record(data) {
    let newTechnique = "" +
        "<div class='card box flow-root-display w-100'>" +
        "    <div class='box-header text-right'>" +
        "        <h6>" + data.title + "</h6>" +
        "        <div class='box-object-left'>" +
        "           <a href='//" + data.link + "'>" +
        "            <i class='fas fa-film'/>" +
        "            <span class='info-text'>ویدیو آموزشی</span>" +
        "           </a>" +
        "       </div>" +
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
        "                        <div class='value'>";
    if (data.is_exam)
        newTechnique += "                            <span>" +
            "زمان آزمون از طریق تماس با شما هماهنگ خواهد شد" +
            "                            </span>";
    else
        newTechnique += "                            <span>" +
            "در حال بررسی...                               " +
            "                            </span>";
    newTechnique += "                        </div>" +
        "                    </div>" +
        "                </div>" +
        "            </div>" +
        "        </div>" +
        "    </div>" +
        "</div>";
    $(".techniques-list .empty-page").remove();
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
    // let data = $(this).serialize().toString();
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
            // Todo : Plz send link of techniques for me here Ali Agha! :D
            add_technique_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            add_technique_form.find("button[type='reset']").prop("disabled", false);
            add_technique_form.find("input").prop("disabled", false).removeClass("progress-cursor");
            add_technique_form.find("label").removeClass("progress-cursor");
            add_technique_form.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $('#addNewTechnique').modal('toggle');
                show_add_technique_record(data);
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                add_technique_form[0].reset();
            }
        },
        error: function (data) {
            let obj = JSON.parse(data.responseText);
            add_technique_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            add_technique_form.find("button[type='reset']").prop("disabled", false);
            add_technique_form.find("input").prop("disabled", false).removeClass("progress-cursor");
            add_technique_form.find("label").removeClass("progress-cursor");
            add_technique_form.closest(".modal").find(".card").removeClass("wait");
            add_technique_form.find(".error:not(input)").remove();
            $("input#resume").removeClass("error");
            $("input#technique-name").removeClass("error")
            if (obj.technique) {
                $("#technique-name").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.technique + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#technique-name").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                display_error(add_technique_form);
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

function setComment(data) {
    // let comments_code = "";
    // if (data.length === 0) {
    //     $(".no-comment").css("display", "block");
    // }
    // for (let i = 0; i < data.length; i++) {
    //     if (data[i].sender_type === "expert") { //expert
    //         let comment_body_classes = "comment-body";
    //         if (data[i].attachment !== "None") {
    //             comment_body_classes += " attached";
    //         }
    //         comments_code += "<div class='expert-comment' dir='ltr' id='" + data[i].pk + "' >" +
    //             "<div class='" + comment_body_classes + "'>" +
    //             "   <span class='comment-tools'>" +
    //             // "       <i class='fas fa-reply'>" +
    //             // "           <div class='reply'></div>" +
    //             // "       </i>" +
    //             "</span>";
    //         if (data[i].attachment !== "None") {
    //             comments_code += "<a href='/" + data[i].attachment + "' class='attached-file'>" +
    //                 "   <i class='fas fa-paperclip'></i>" +
    //                 "   <span>" + data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1) + "</span>" +
    //                 "</a>";
    //         }
    //         comments_code += "<pre>" + data[i].description + "</pre>" +
    //             "   </div>" +
    //             "</div>";
    //     } else if (data[i].sender_type === "researcher") { //researcher
    //         let comment_body_classes = "comment-body";
    //         if (data[i].attachment !== "None") {
    //             comment_body_classes += " attached";
    //         }
    //         comments_code += "<div class='my-comment' id='" + data[i].pk + "' >" +
    //             "<div class='" + comment_body_classes + "' dir='ltr'>" +
    //             "   <span class='comment-tools'>" +
    //             "       <div class='btn-group dropright'>" +
    //             "           <button type='button' class='dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
    //             "               <i class='fas fa-cog'></i>" +
    //             "           </button>" +
    //             "           <div class='dropdown-menu'>" +
    //             // "               <div class='dropdown-item'>" +
    //             // "                   <i class='fas fa-pen'></i>" +
    //             // "                   <span>ویرایش پیام</span>" +
    //             // "               </div>" +
    //             "               <div class='dropdown-item'>" +
    //             "                   <i class='fas fa-trash-alt'></i>" +
    //             "                   <span>حذف پیام</span>" +
    //             "               </div>" +
    //             "           </div>" +
    //             "       </div>" +
    //             // "       <i class='fas fa-reply'>" +
    //             // "           <div class='reply'></div>" +
    //             // "       </i>" +
    //             "   </span>";
    //         if (data[i].attachment !== "None") {
    //             comments_code += "<a href='/" + data[i].attachment + "' class='attached-file'>" +
    //                 "   <i class='fas fa-paperclip'></i>" +
    //                 "   <span>" + data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1) + "</span>" +
    //                 "</a>";
    //         }
    //         comments_code += "<pre>" + data[i].description + "</pre>" +
    //             "   </div>" +
    //             "</div>";
    //     } else { //system
    //         comments_code += "<div class='system-comment'>" +
    //             "<div class='comment-body' dir='ltr'>" +
    //             "<pre>" +
    //             data[i].description +
    //             "</pre>" +
    //             "</div>" +
    //             "</div>";
    //     }
    // }
    // $('.comments').html(comments_code);
    // dialog_comment_init();
    // $(".comments .fa-trash-alt").closest(".dropdown-item").click(function () {
    //     deleteComment($(this).closest('.my-comment'));
    // });
    let comments_code = "";
    console.log(data);
    for (let i = 0; i < data.length; i++) {
        if (data[i].sender_type === "researcher") { //researcher
            let comment_body_classes = "comment-body";
            let attachment = "";
            if (data[i].attachment !== "None") {
                comment_body_classes += " attached";
                attachment = `
                    <a href='/${data[i].attachment}' class='attached-file'>
                        <i class='fas fa-paperclip'></i>
                        <span>${data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1)}</span>
                    </a>
                `;
            }
            comments_code += `
                            <div class='my-comment' id='${data[i].pk}'>
                                <div class='comment-profile'></div>
                                <div class='${comment_body_classes}'>
                                    <span class='comment-tools'>
                                        <div class='btn-group dropright'>
                                            <button type='button' class='dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>
                                                <i class='fas fa-cog'></i>
                                            </button>
                                            <div class='dropdown-menu'>
                                                <div class='dropdown-item'>
                                                    <i class='fas fa-trash-alt'></i>
                                                    <span>حذف پیام</span>
                                                </div>
                                            </div>
                                        </div>
                                    </span>
                                    <pre>${data[i].description}</pre>
                                    ${
                data[i].attachment !== "None" ?
                    attachment
                    :
                    ""
                }
                                </div>
                            </div>
            `;
        } else if (data[i].sender_type === "expert") { //expert
            let comment_body_classes = "comment-body";
            if (data[i].attachment !== "None") {
                comment_body_classes += " attached";
            }
            comments_code += "<div class='your-comment'>" +
                "   <div class='" + comment_body_classes + "' dir='ltr'>" +
                "       <span class='comment-tools'>" +
                "       </span>" +
                "<pre>" + data[i].description + "</pre>";
            if (data[i].attachment !== "None") {
                comments_code += "<a href='/" + data[i].attachment + "' class='attached-file'>" +
                    "   <i class='fas fa-paperclip'></i>" +
                    "   <span>" + data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1) + "</span>" +
                    "</a>";
            }
            comments_code += "" +
                "   </div>" +
                "</div>";
        } else { //system
            comments_code += "<div class='system-comment'>" +
                "<div class='comment-body' dir='ltr'>" +
                "<pre>" +
                data[i].description +
                "</pre>" +
                "</div>" +
                "</div>";
        }
    }
    if (comments_code === "") {
        $(".no-comment").addClass("show");
    }
    $('.comments').html(comments_code).animate({scrollTop: $('.comments').prop("scrollHeight")}, 1000);
    dialog_comment_init();
    $(".comments .fa-trash-alt").closest(".dropdown-item").click(function () {
        deleteComment($(this).closest('.my-comment'));
    });
}

function addComment(data) {
    let comment_body_classes = "comment-body";
    let attachment = "";
    if (data.attachment !== "None") {
        comment_body_classes += " attached";
        attachment = `
                    <a href='/${data.attachment}' class='attached-file'>
                        <i class='fas fa-paperclip'></i>
                        <span>${data.attachment.substring(data.attachment.lastIndexOf("/") + 1)}</span>
                    </a>
                `;
    }
    let new_comment = `
                            <div class='my-comment' id='${data.pk}'>
                                <div class='comment-profile'></div>
                                <div class='${comment_body_classes}'>
                                    <span class='comment-tools'>
                                        <div class='btn-group dropright'>
                                            <button type='button' class='dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>
                                                <i class='fas fa-cog'></i>
                                            </button>
                                            <div class='dropdown-menu'>
                                                <div class='dropdown-item'>
                                                    <i class='fas fa-trash-alt'></i>
                                                    <span>حذف پیام</span>
                                                </div>
                                            </div>
                                        </div>
                                    </span>
                                    <pre>${data.description}</pre>
                                    ${
        data.attachment !== "None" ?
            attachment
            :
            ""
        }       
                                </div>
                            </div>
            `;
    $(".comments").append(new_comment);
}

let comment_form = $('#comment-form');
comment_form.submit(function (event) {
    event.preventDefault();
    comment_form.find("button[type='submit']").css("color", "transparent").addClass("loading-btn").attr("disabled", "true");
    comment_form.find("label").addClass("progress-cursor");
    let $thisURL = comment_form.attr('url');
    let data = new FormData(comment_form.get(0));
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
            if ($(".project-comment-innerDiv").find(".no-comment").length > 0) {
                $(".project-comment-innerDiv").find(".no-comment").remove();
            }
            addComment(data);
            iziToast.success({
                rtl: true,
                message: "پیام با موفقیت ارسال شد!",
                position: 'bottomLeft'
            });
            comment_form[0].reset();
            comment_form.find("#description").css("height", "fit-content");
            $(".comments .fa-trash-alt").closest(".dropdown-item").click(function () {
                deleteComment($(this).closest('.my-comment'));
            });
        },
        error: function (data) {
            let obj = JSON.parse(data.responseText);
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
// Custom project_request.html number type inputs arrows
$(".apply_Project .input-group-text").click(function () {
    let value = $(this).closest(".form-group").find(".form-control").val();
    if (isNaN(parseInt(value, 10))) {
        value = 0;
    }
    if ($(this).closest("div").hasClass("input-group-prepend")) {
        value -= 1;
        if (value < 0) {
            value = 0;
        }
        $(this).closest(".form-group").find(".form-control").val(value);
    } else if ($(this).closest("div").hasClass("input-group-append")) {
        value = parseInt(value) + 1;
        if (value > 168) {
            value = 168;
        }
        $(this).closest(".form-group").find(".form-control").val(value);
    }
});
// End
let apply_form = $(".apply_Project");
apply_form.submit(function (event) {
    event.preventDefault();
    let url = apply_form.attr('url');
    let data = $(this).serialize().toString();
    $("input#most_hours").removeClass("error");
    $("input#least_hours").removeClass("error");
    $("#least_hours").closest("div").find(".error").remove();
    $("#most_hours").closest("div").find(".error").remove();
    $.ajax({
        method: "POST",
        dataType: "json",
        data: data,
        url: url,
        success: function (data) {
            $("input#most_hours").removeClass("error");
            $("input#least_hours").removeClass("error");
            $(".apply").hide();
            $('#projectRequest').modal('toggle');
            iziToast.success({
                rtl: true,
                message: "درخواست شما برای استاد فرستاده شد.",
                position: 'bottomLeft'
            });
        },
        error: function (data) {
            let obj = JSON.parse(data.responseText);
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
            display_error(apply_form);
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
                rtl: true,
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

function ShowMyProject(project) {
    let show_project = "<div class='card project-item'>" +
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

$(".my-project").click(function () {
    const dialog = $(".showProject");
    let projectId = $(this).attr("id");
    $.ajax({
        method: 'GET',
        url: '/researcher/myProject/',
        data: {id: projectId},
        dataType: 'json',
        success: function (data) {
            dialog.find(".project-title").html(data.persian_title + "<br>" + " (" + data.english_title + ")");
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
            $(comment).remove();
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

function isOverflow(element) {
    return (element.offsetHeight < element.scrollHeight) || (element.offsetWidth < element.scrollWidth)
}

$("#active-project").click(function () {
    $(".new-project").attr("style", "display :none;");
    $(".done-project").attr("style", "display :none;");
    $(".missed-project").attr("style", "display :none;");
    $(".your-project").attr("style", "display :block;");
    $(".your-project .card.box").each(function () {
        if (isOverflow($(this).find(".project-techniques")[0])) {
            $(this).find(".project-techniques").addClass("do-not-touch");
            while (isOverflow($(this).find(".project-techniques")[0])) {
                $(this).find(".project-techniques span:nth-last-child(2)").remove();
            }
        } else {
            $(this).find(".project-techniques:not(.do-not-touch) span:last-child").css("display", "none");
        }

    });
});

$("#new-projects").click(function () {
    $(".new-project").attr("style", "display :block");
    $(".done-project").attr("style", "display :none");
    $(".your-project").attr("style", "display :none");
    $(".missed-project").attr("style", "display :none");
    $(".new-project .card.box").each(function () {
        if (isOverflow($(this).find(".project-techniques")[0])) {
            $(this).find(".project-techniques").addClass("do-not-touch");
            while (isOverflow($(this).find(".project-techniques")[0])) {
                $(this).find(".project-techniques span:nth-last-child(2)").remove();
            }
        } else {
            $(this).find(".project-techniques:not(.do-not-touch) span:last-child").css("display", "none");
        }

    })
});

$("#missed-project").click(function () {
    $(".missed-project").attr("style", "display :block");
    $(".done-project").attr("style", "display :none");
    $(".your-project").attr("style", "display :none");
    $(".new-project").attr("style", "display :none");
    $(".missed-project .card.box").each(function () {
        if (isOverflow($(this).find(".project-techniques")[0])) {
            $(this).find(".project-techniques").addClass("do-not-touch");
            while (isOverflow($(this).find(".project-techniques")[0])) {
                $(this).find(".project-techniques span:nth-last-child(2)").remove();
            }
        } else {
            $(this).find(".project-techniques:not(.do-not-touch) span:last-child").css("display", "none");
        }

    })
});

$("#done-project").click(function () {
    $(".new-project").attr("style", "display :none");
    $(".your-project").attr("style", "display :none");
    $(".missed-project").attr("style", "display :none");
    $(".done-project").attr("style", "display :block");
    $(".done-project .card.box").each(function () {
        if (isOverflow($(this).find(".project-techniques")[0])) {
            $(this).find(".project-techniques").addClass("do-not-touch");
            while (isOverflow($(this).find(".project-techniques")[0])) {
                $(this).find(".project-techniques span:nth-last-child(2)").remove();
            }
        } else {
            $(this).find(".project-techniques:not(.do-not-touch) span:last-child").css("display", "none");
        }

    })
});