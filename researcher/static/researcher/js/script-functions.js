function load_dialog() {
    $(".title-back").each(function () {
        let title_back_width = $(this).prev().outerWidth() + 30;
        $(this).css("width", title_back_width);
    });
    $(".row-header > .header").each(function () {
        let divWidth = $(this).outerWidth();
        divWidth = $(this).closest("div").innerWidth() - divWidth;
        $(this).prev().css("width", divWidth / 2 - 10);
        $(this).next().css("width", divWidth / 2 - 10);
        $(this).css("left", (divWidth) / 2);
    });
}

function init_windowSize() {
    // if ($(window).width() < 575.98) {
    // } else {
    //     let contentWidth = $(document).innerWidth() - 250;
    //     let contentMargin = 0.0862 * contentWidth - 54.9655;
    //     $(".info-card").css({
    //         "margin-right": contentMargin,
    //         "margin-left": contentMargin
    //     });
    //     $(".content").css({
    //         "width": contentWidth,
    //         "height": "90%"
    //     });
    //     $(".side-bar").css("height", "100%");
    // }
}

function init_dialog_btn(element, dialogClass) {
    $(element).click(function () {
        $(".fixed-back").removeClass("show");
        $(".main").removeClass("blur-div");
        blur_div_toggle(".main");
        $(dialogClass).addClass("show");
        close_dialog(dialogClass);
        dialog_comment_init();
        load_dialog();
    });
}

function cancel_add(className) {
    div = "<span class='initial-value' style='border: 1px dashed #bdbdbd;width: fit-content;border-radius: 0.25em;padding: 5px 10px;font-size: 13px;font-weight: 300;'>برای افزودن سابقه جدید روی <i class='fas fa-plus'></i>  کلیک کنید!  </span>";
    $(".refuse-btn").click(function () {
        $(className + " div#" + $(this).attr("id")).remove();
        if ($(className).html() === '') {
            $(className).append(div);
        }
    });
}

function search_input(className) {
    $(className).focusin(function () {
        $(this).css("width", "50%");
    }).focusout(function () {
        if ($(this).val() === '') {
            $(this).css("width", "initial");
        }
    });
}

function close_dialog(className) {
    $(".close").click(function () {
        $(className).removeClass("show");
        $(".main").removeClass("blur-div");
        if (className === ".add-technique") {
            express();
            $(className).find("input").val("");
            $(className).find("input:checked").prop("checked", false);
            reset($(className).find(".upload-resume + label"));
            let upload_resume = ".fixed-back input.upload-resume";
            reset($(upload_resume).closest("div").find("img.upload-img"));
            reset($(upload_resume).closest("div").find("img.file-img"));
            $(upload_resume).next().find(".upload-file-text").css("padding-top", "0").html("آپلود فایل");
        } else if (className === ".review-request") {
            $(className).find("textarea").val("");
            $(className).find("input:checked").prop("checked", false);
            reset($(className).find(".upload-resume + label"));
            let upload_resume = ".fixed-back input.upload-resume";
            reset($(upload_resume).closest("div").find("img.upload-img"));
            reset($(upload_resume).closest("div").find("img.file-img"));
            $(upload_resume).next().find(".upload-file-text").css("padding-top", "0").html("آپلود فایل");
        } else {
            $(className).find("input").val("");
            $(className).find("input:checked").prop("checked", false);
            $(className).find(".keywords").html("");
        }
        input_focus();
    });
}

function record_edit(className) {
    $(className + " .fa-pen").click(function () {
        if ($(className + " .ch-card-item").length === 0) {
            if (className === '.education') {
                let count = parseInt($(this).attr('id').replace('edit_edu_', ''));
                $(className).append(education_data_form(count));
                cancel_add(".education");
                $("#edu-section" + count).val($(this).closest('tr').children("td:nth-child(1)").text());
                $("#edu-subject" + count).val($(this).closest('tr').children("td:nth-child(2)").text());
                $("#university" + count).val($(this).closest('tr').children("td:nth-child(3)").text());
                $("#edu-city" + count).val($(this).closest('tr').children("td:nth-child(4)").text());
                $("#edu-year" + count).val($(this).closest('tr').children("td:nth-child(5)").text());
            } else if (className === '.executive') {
                let count = parseInt($(this).attr('id').replace('edit_exe_', ''));
                $(className).append(executive_data_form(count));
                cancel_add(".executive");
                $("#duty" + count).val($(this).closest('tr').children("td:nth-child(1)").text());
                $("#from" + count).val($(this).closest('tr').children("td:nth-child(2)").text());
                $("#until" + count).val($(this).closest('tr').children("td:nth-child(3)").text());
                $("#workplace" + count).val($(this).closest('tr').children("td:nth-child(4)").text());
                $("#exe-city" + count).vaal($(this).closest('tr').children("td:nth-child(5)").text());
            } else if (className === '.studious') {
                let count = parseInt($(this).attr('id').replace('edit_stu_', ''));
                $(className).append(studious_data_form(count));
                cancel_add(".studious");
                $("#subject" + count).val($(this).closest('tr').children("td:nth-child(1)").text());
                $("#admin" + count).val($(this).closest('tr').children("td:nth-child(2)").text());
                $("#liable" + count).val($(this).closest('tr').children("td:nth-child(3)").text());
                $("#rank" + count).val($(this).closest('tr').children("td:nth-child(4)").text());
            }
            input_focus();
        }
    });
    // $(className + " .fa-trash-alt").click(function () {
    //     div = "<span class='initial-value' style='border: 1px dashed #bdbdbd;width: fit-content;border-radius: 0.25em;padding: 5px 10px;font-size: 13px;font-weight: 300;'>برای افزودن سابقه جدید روی <i class='fas fa-plus'></i>  کلیک کنید!  </span>";
    //     if (className === '.education') {
    //         let count = parseInt($(this).attr('id').replace('edit_edu_', ''));
    //         $(this).closest("tr").remove();
    //     } else if (className === '.executive') {
    //         let count = parseInt($(this).attr('id').replace('edit_exe_', ''));
    //         $(this).closest("tr").remove();
    //     } else if (className === '.studious') {
    //         let count = parseInt($(this).attr('id').replace('edit_stu_', ''));
    //         $(this).closest("tr").remove();
    //     }
    //     if ($(className + " > table > tbody > tr").length === 0) {
    //         $(className).html(div);
    //     }
    // });
}

function education_data_form(edu_count) {
    let div = document.createElement("div");
    $(div).addClass('card').addClass('ch-card-item');
    $(div).attr("id", edu_count);
    $(div).html("<form action='' method='post'><div class='row'>" +
        "<div class='col-lg-6'>" +
        "<label for=\"edu-section" + edu_count + "\">مقطع تحصیلی</label>\n" +
        "<input type=\"text\" id=\"edu-section" + edu_count + "\" class=\"w-100\">" +
        "</div>" +
        "<div class='col-lg-6'>" +
        "<label for=\"edu-subject" + edu_count + "\">رشته تحصیلی</label>\n" +
        "<input type=\"text\" id=\"edu-subject" + edu_count + "\" class=\"w-100\">" +
        "</div>" +
        "</div>" +
        "</div>" +
        "<div class='row'>" +
        "<div class='col-lg-4'>" +
        "<label for=\"university" + edu_count + "\">دانشگاه</label>\n" +
        "<input type=\"text\" id=\"university" + edu_count + "\" class=\"w-100\">" +
        "</div>" +
        "<div class='col-lg-3'>" +
        "<label for=\"edu-city" + edu_count + "\">شهر محل تحصیل</label>\n" +
        "<input type=\"text\" id=\"edu-city" + edu_count + "\" class=\"w-100\">" +
        "</div>" +
        "<div class='col-lg-3'>" +
        "<label for=\"year" + edu_count + "\">سال اخذ مدرک</label>\n" +
        "<input type=\"text\" id=\"year" + edu_count + "\" class=\"w-100\">" +
        "</div>" +
        "<div class='col-lg-2'></div>" +
        "</div>" +
        "<div class='row mtop-lg-25'>" +
        "<div class='col-lg-9'>" +
        "<button type='button' id='" + edu_count + "' class='w-100 accept-btn btn'>افزودن</button>" +
        "</div>" +
        "<div class='col-lg-3'>" +
        "<button type='button' id='" + edu_count + "' class='w-100 refuse-btn btn'>لغو</button>" +
        "</div>" +
        "</div></form>");
    return div;
}

function education_record() {
    $(".education-btn > i.fa-plus").click(function () {
        if ($(".education .ch-card-item").length === 0) {
            if ($(".education > .initial-value").hasClass("initial-value")) {
                $(".education").html(education_data_form(edu_count));
            } else {
                $('.education').append(education_data_form(edu_count));
            }
            cancel_add(".education");
            // add_education_record(edu_count);
            input_focus();
            edu_count++;
        }
    });
}

function show_scientific_record(pk) {
    let row = "<tbody class='row-sci-" + pk + "'><tr>" +
        "<td>" + $("#edu-section").val() + "</td>" +
        "<td>" + $("#edu-subject").val() + "</td>" +
        "<td>" + $("#university").val() + "</td>" +
        "<td>" + $("#edu-city").val() + "</td>" +
        "<td>" + $("#year").val() + "</td>" +
        "<td>" +
        // "<i class='fas fa-pen' id='edit_edu'></i>" +
        "<i class='fas fa-trash-alt delete_edu' value=" + pk + "></i>" +
        "</td>" +
        "</tr></tbody>";
    if (!$(".education > table").hasClass("table")) {
        let table = "<table class='table mtop-lg-25'>" +
            "<thead>" +
            "<tr>" +
            "<td>مقطع تحصیلی</td>" +
            "<td>رشته تحصیلی</td>" +
            "<td>دانشگاه</td>" +
            "<td>شهر محل تحصیل</td>" +
            "<td>سال اخذ مدرک</td>" +
            "<td></td>" +
            "</tr>" +
            "</thead>" +
            "<tbody>" +
            "</tbody>" +
            "</table>";
        $(".education").html(table);
    }
    $(".education > table").append(row);
    $(".education div#" + $(this).attr("id")).remove();
    record_edit(".education");
}

function executive_data_form(exe_count) {
    let div = document.createElement("div");
    $(div).addClass('card').addClass('ch-card-item');
    $(div).attr("id", exe_count);
    $(div).html("<form action='' method='post'><div class='row'>" +
        "<div class='col-lg-5'>" +
        "<label for='duty" + exe_count + "'>سمت</label>" +
        "<input type='text' id='duty" + exe_count + "' class='w-100'>" +
        "</div>" +
        "<div class='col-lg-1'>" +
        "<span class='center-vr'>زمان :</span>" +
        "</div>" +
        "<div class='col-lg-3'>" +
        "<label for='from" + exe_count + "'>از تاریخ</label>" +
        "<input type='text' id='from" + exe_count + "' class='w-100'>" +
        "</div>" +
        "<div class='col-lg-3'>" +
        "<label for='until" + exe_count + "'>تا تاریخ</label>" +
        "<input type='text' id='until" + exe_count + "' class='w-100'>" +
        "</div>" +
        "</div>" +
        "<div class='row'>" +
        "<div class='col-lg-5'>" +
        "<label for='workplace" + exe_count + "'>نام مجموعه</label>" +
        "<input type='text' id='workplace" + exe_count + "' class='w-100'>" +
        "</div>" +
        "<div class='col-lg-4'>" +
        "<label for='exe-city" + exe_count + "'>شهر</label>" +
        "<input type='text' id='exe-city" + exe_count + "' class='w-100'>" +
        "</div>" +
        "<div class='col-lg-3'></div>" +
        "</div>" +
        "<div class='row mtop-lg-25'>" +
        "<div class='col-lg-9'>" +
        "<button type='button' id='" + exe_count + "' class='w-100 accept-btn btn'>افزودن</button>" +
        "</div>" +
        "<div class='col-lg-3'>" +
        "<button type='button' id='" + exe_count + "' class='w-100 refuse-btn btn'>لغو</button>" +
        "</div>" +
        "</div></form>");
    return div;
}

// function executive_record() {
//     $(".executive-btn > i.fa-plus").click(function () {
//         if( $(".executive .ch-card-item").length === 0 ) {
//             if ($(".executive > .initial-value").hasClass("initial-value")) {
//                 $(".executive").html(executive_data_form(exe_count));
//             } else {
//                 $('.executive').append(executive_data_form(exe_count));
//             }
//             cancel_add(".executive");
//             add_executive_record(exe_count);
//             input_focus();
//             $("#from" + exe_count).persianDatepicker({});
//             $("#until" + exe_count).persianDatepicker({});
//             exe_count++;
//         }
//     });
// }
function show_executive_record(pk) {
    let row = "<tbody class='row-exe-" + pk + "'><tr>" +
        "<td>" + $("#duty").val() + "</td>" +
        "<td>" + $("#workplace").val() + "</td>" +
        "<td>" + $("#exe-city").val() + "</td>" +
        "<td>" + $("#from").val() + "</td>" +
        "<td>" + $("#until").val() + "</td>" +
        "<td>" +
        // "<i class='fas fa-pen' id='edit_exe'></i>" +
        "<i class='fas fa-trash-alt delete_exe' value=" + pk + "></i>" +
        "</td>" +
        "</tr></tbody>";
    if (!$(".executive > table").hasClass("table")) {
        let table = "<table class='table mtop-lg-25'>" +
            "<thead>" +
            "<tr>" +
            "<td>سمت</td>" +
            "<td>نام مجموعه</td>" +
            "<td>شهر</td>" +
            "<td>از تاریخ</td>" +
            "<td>تا تاریخ</td>" +
            "<td></td>" +
            "</tr>" +
            "</thead>" +
            "<tbody>" +
            "</tbody>" +
            "</table>";
        $(".executive").html(table);
    }
    $(".executive > table").append(row);
    $(".executive div#" + $(this).attr("id")).remove();
    record_edit(".executive");
}

function studious_data_form(stu_count) {
    let div = document.createElement("div");
    $(div).addClass('card').addClass('ch-card-item');
    $(div).attr("id", stu_count);
    $(div).html("<form action='' method='post'><div class='row'>" +
        "<div class='col-lg-5'>" +
        "<label for='subject" + stu_count + "'>عنوان طرح پژوهشی</label>" +
        "<input type='text' id='subject" + stu_count + "' class='w-100'>" +
        "</div>" +
        "<div class='col-lg-3'>" +
        "<label for='admin" + stu_count + "'>نام مجری</label>" +
        "<input type='text' id='admin" + stu_count + "' class='w-100'>" +
        "</div>" +
        "<div class='col-lg-4'>" +
        "<label for='liable" + stu_count + "'>مسئول اجرا/همکار</label>" +
        "<input type='text' id='liable" + stu_count + "' class='w-100'>" +
        "</div>" +
        "</div>" +
        "<div class='row'>" +
        "<div class='col-lg-7 rankDiv'>" +
        "<label class='rankLabel' for='rank' style='width:245px'>وضعیت طرح پژوهشی</label>" +
        "<select id='rank'>" +
        "<option selected dir='rtl'>انتخاب کنید ...</option>" +
        "<option value='1'>در دست  اجرا</option>" +
        "<option value='2'>خاتمه یافته</option>" +
        "<option value='3'>متوقف</option>" +
        "</select>" +
        "</div>" +
        "<div class='col-lg-5'></div>" +
        "</div>" +
        "<div class='row mtop-lg-25'>" +
        "<div class='col-lg-9'>" +
        "<button type='button' id='" + stu_count + "' class='w-100 accept-btn btn'>افزودن</button>" +
        "</div>" +
        "<div class='col-lg-3'>" +
        "<button type='button' id='" + stu_count + "' class='w-100 refuse-btn btn'>لغو</button>" +
        "</div>" +
        "</div></form>");
    return div;
}

// function studious_record() {
//     $(".studious-btn > i.fa-plus").click(function () {
//         if ($(".studious .ch-card-item").length === 0) {
//             if ($(".studious > .initial-value").hasClass("initial-value")) {
//                 $(".studious").html(studious_data_form(stu_count));
//             } else {
//                 $('.studious').append(studious_data_form(stu_count));
//             }
//             cancel_add(".studious");
//             add_studious_record(stu_count);
//             input_focus();
//             stu_count++;
//         }
//     });
// }

function show_research_record(pk) {
    console.log($("#rank").val());
    if ($("#rank").val() === 1) {
        let row = "<tbody class='row-stu-" + pk + "'><tr>" +
            "<td>" + $("#subject").val() + "</td>" +
            "<td>" + $("#admin").val() + "</td>" +
            "<td>" + $("#liable").val() + "</td>" +
            "<td>در دست اجرا</td>" +
            "<td>" +
            // "<i class='fas fa-pen' id='edit_stu'></i>" +
            "<i class='fas fa-trash-alt delete_stu' value=" + pk + "></i>" +
            "</td>" +
            "</tr></tbody>";
    } else if ($("#rank").val() === 2) {
        let row = "<tbody class='row-stu-" + pk + "'><tr>" +
            "<td>" + $("#subject").val() + "</td>" +
            "<td>" + $("#admin").val() + "</td>" +
            "<td>" + $("#liable").val() + "</td>" +
            "<td>خاتمه یافته</td>" +
            "<td>" +
            // "<i class='fas fa-pen' id='edit_stu'></i>" +
            "<i class='fas fa-trash-alt' id='edit_stu'></i>" +
            "</td>" +
            "</tr></tbody>";
    } else if ($("#rank").val() === 3) {
        let row = "<tbody class='row-stu-" + pk + "'><tr>" +
            "<td>" + $("#subject").val() + "</td>" +
            "<td>" + $("#admin").val() + "</td>" +
            "<td>" + $("#liable").val() + "</td>" +
            "<td>متوقف</td>" +
            "<td>" +
            "<i class='fas
            ' id='edit_stu'></i>" +
            "<i class='fas fa-trash-alt' id='edit_stu'></i>" +
            "</td>" +
            "</tr></tbody>";
    }
    if (!$(".studious > table").hasClass("table")) {
        let table = "<table class='table mtop-lg-25'>" +
            "<thead>" +
            "<tr>" +
            "<td>عنوان طرح پژوهشی</td>" +
            "<td>مجری</td>" +
            "<td>مسئول اجرا/ همکار</td>" +
            "<td>وضعیت طرح پژوهشی</td>" +
            "<td></td>" +
            "</tr>" +
            "</thead>" +
            "<tbody>" +
            "</tbody>" +
            "</table>";
        $(".studious").html(table);
    }
    $(".studious > table ").append(row);
    $(".studious div#" + $(this).attr("id")).remove();
    record_edit(".studious");
}

function dialog_comment_init() {
    $(".send-comment-container .comment-input input#comment-attach").on("change", function () {
        let fileName = $(this).val().split("\\").pop();
        $(".send-comment-container .comment-input .attachment span").html(fileName);
        $(".send-comment-container .comment-input").addClass("attached");

        $(".send-comment-container .comment-input.attached i.fa-trash-alt").click(function () {
            $(".send-comment-container .comment-input input#comment-attach").val("");
            $(".send-comment-container .comment-input .attachment span").html("");
            $(".send-comment-container .comment-input").removeClass("attached");
        });
    });
    // add emoji to comment
    // $(".new-comment-tools > .fa-smile").click(function () {
    //     alert("Not working");
    //     // $('#comment').emojiPicker('toggle');
    //     // alert("a");
    // });
    // // delete user comment
    // $(".comment-tools > .fa-trash-alt").click(function () {
    //     $(this).parents("div.my-comment").remove();
    // });
    // // attach file to comment
    // $(".new-comment-tools > label[for='comment-attach']").click(function () {
    //     rows = $("textarea#comment").attr("rows");
    //     $("textarea#comment").attr("rows", ++rows);
    //     padding_bottom = parseInt($("textarea#comment").css("padding-bottom")) + 30;
    //     $("textarea#comment").css("padding-bottom", padding_bottom);
    //
    //     if ($("div.attachment > div").last().hasClass("attach")) {
    //         bottom_position = parseInt($("div.attachment > div").last().css("bottom"));
    //     } else {
    //         bottom_position = 20;
    //     }
    //
    //     // $("div.attachment").append("<div class='attach'>" +
    //     //     "<span>" + "نام فایل" + "</span>" +
    //     //     "<div class='progress'>" +
    //     //     "<div class='progress-bar progress-bar-striped progress-bar-animated' role='progressbar' aria-valuenow='75' aria-valuemin='0' aria-valuemax='100' style='width: 75%'></div>" +
    //     //     "</div>" +
    //     //     "</div>");
    //     $("div.attachment > div").last().css("bottom", bottom_position + 15);
    // });
    // // replay to a comment
    // $(".comment-tools > .fa-reply").click(function () {
    //     let text = $.trim($(this).closest("div").children(2).text());
    //     $("textarea#comment").closest("div").append("<div class='replay-div'></div>");
    //     $(".replay-div").html("<i class='fa fa-reply fa-lg'></i>" + text + "<i class='fa fa-times'></i>");
    //     $(".replay-div > .fa-times").click(function () {
    //         $(".replay-div").remove();
    //         $("textarea#comment").css("padding-top", "2px").focus().on("focusout", function () {
    //             let inputLabel = "label[for='" + $(this).attr("id") + "']";
    //             $(inputLabel).css("color", "#6f7285");
    //             if ($(this).val() === '') {
    //                 $(inputLabel).css({
    //                     "font-size": "14px",
    //                     "top": "28px",
    //                     "right": "25px",
    //                     "color": "#6f7285"
    //                 });
    //             } else {
    //                 $(this).css("color", "#8d8d8d");
    //                 $(inputLabel).css("color", "#8d8d8d");
    //             }
    //         });
    //     });
    //     $("textarea#comment").css("padding-top", "35px").focus().on("focusout", function () {
    //         let inputLabel = "label[for='" + $(this).attr("id") + "']";
    //         $(inputLabel).css("color", "#6f7285");
    //         if ($(this).val() === '') {
    //             $(inputLabel).css({
    //                 "font-size": "14px",
    //                 "top": "58px",
    //                 "right": "25px",
    //                 "color": "#6f7285"
    //             });
    //         } else {
    //             $(this).css("color", "#8d8d8d");
    //             $(inputLabel).css("color", "#8d8d8d");
    //         }
    //     });
    // });
    // // edit user comment
    // $(".comment-tools > .fa-pen").click(function () {
    //     text = $.trim($(this).closest("div").children(2).text());
    //     $("textarea#comment").html(text);
    //     $("textarea#comment").focus();
    // });
}

function vote_dialog_init() {
    let flag = 0;
    let slide_count = 9;
    $(".vote-question").hover(function () {
        $(this).parent('.col-lg-12').children('.vote-question-text').slideDown().css({
            "color": "#3ccd1c",
            "border-color": "#3ccd1c"
        });
    }, function () {
        if (!$(this).parent('.col-lg-12').children('.vote-question-text').hasClass('fix')) {
            $(this).parent('.col-lg-12').children('.vote-question-text').slideUp();
        } else {
            $(this).parent('.col-lg-12').children('.vote-question-text').css({
                "color": "#707070",
                "border-color": "#707070"
            })
        }
    }).click(function () {
        $(this).parent('.col-lg-12').children('.vote-question-text').toggleClass('fix');
    });
    $(".vote").click(function () {
        if ($('.vote-dialog').css('display') === 'none') {
            $('.vote-dialog').slideDown();
            $('.vote > .dots').addClass('expand');
        } else {
            $('.vote-dialog').slideUp();
            $('.vote > .dots').removeClass('expand');
        }
    });
    $(".vote-dialog > .expert-back").hover(function () {
        $(this).addClass('hover');
    }, function () {
        $(this).removeClass('hover');
    }).click(function () {
        $(".showProject").slideUp('slow').delay('slow');
        $(".voting").delay('delay').slideDown('slow');
        close_dialog('.voting');
        vote_slider(14);
        $(".progress-line").css("width", "calc(100% / 14)");
    });
}

function vote_slider(slide_count) {
    let counter = 0;

    function next_button_init() {
        $(".next-button").click(function () {
            if (counter < slide_count - 1) {
                counter++;
                let progressWidth = parseInt($(".vote-list > .vote-item").css('width'));
                let width = parseFloat($(".progress-line").css('width'));
                $(".progress-line").css('width', width + progressWidth);

                $(".swiper-wrapper").css({
                    "transform": "translate3d(-" + 100 * counter + "%, 0, 0)",
                    "transition-duration": "0.3s"
                });
            }
            if (counter === slide_count - 1) {
                $(this).closest("div").prepend("<span class='submit-button'>" +
                    "<i class='fas fa-check'></i>" +
                    "ثبت" +
                    "</span>");
                $(this).remove();
            }
            if (counter > 0) {
                $(".prev-button").removeClass("disabled");
            }
        });
    }

    next_button_init();
    $(".prev-button").click(function () {
        if (counter > 0) {
            counter--;
            let progressWidth = parseInt($(".vote-list > .vote-item").css('width'));
            let width = parseFloat($(".progress-line").css('width'));
            $(".progress-line").css('width', width - progressWidth);

            $(".swiper-wrapper").css({
                "transform": "translate3d(-" + 100 * counter + "%, 0, 0)",
                "transition-duration": "0.3s"
            });
        }
        if (counter === slide_count - 2) {
            $(this).closest("div").prepend("<span class='next-button'>" +
                "<i class='fas fa-arrow-right'></i>" +
                "بعدی" +
                "</span>");
            $(this).closest("div").find(".submit-button").remove();
            next_button_init();
        }
        if (counter === 0) {
            $(this).addClass('disabled');
        }
    });
}

if (window.location.href.indexOf("researcher/technique/") > -1) {
    function slide_up() {
        $(".modal .all-techniques").slideUp('slow');
        return $.Deferred().resolve(false);
    }

    function remove_class() {
        $(".modal input#technique-name").removeClass("expand");
    }

    function expand() {
        $(".modal .all-techniques").slideDown('slow');
        $(".modal input#technique-name").addClass("expand");
        $(".modal .select-technique i").removeClass("fa-plus").addClass("fa-search");
        $(".modal label[for='technique-name']").html("جستجو تکنیک");

    }

    function express() {
        slide_up().done(remove_class());
        $(".modal .select-technique i").removeClass("fa-search").addClass("fa-plus");
        $(".modal label[for='technique-name']").html("نام تکنیک");
    }

    $(".modal .select-technique").click(function () {
        if ($(".modal input#technique-name").hasClass("expand")) {
            express();
        } else {
            expand();
        }

    });
    $(".modal input.upload-resume").next().hover(function () {
        $(this).find("svg").find("path").attr("fill", "#3ccd1c");
    }, function () {
        $(this).find("svg").find("path").attr("fill", "#bdbdbd");
    });

    $(".modal .confirmation .upload-file").click(function () {
        $(this).closest("form").find("input.upload-resume").next().slideDown("slow").closest("div.col-12").css("padding-bottom", "15px");
    });

    $(".modal .confirmation .close-upload").click(function () {
        $(this).closest("form").find("input.upload-resume").next().slideUp("slow").closest("div.col-12").css("padding-bottom", "0px");
    });

    $(".modal input.upload-resume").on("change", function () {
        $(this).closest("div").find("img.upload-img").css("display", "none");
        $(this).closest("div").find("img.file-img").css("display", "block");
        let fileName = $(this).val().split("\\").pop();
        $(this).next().find(".upload-file-text").css("padding-top", "5px")
            .html(fileName);
    });
}


function question() {
    $(".show-researching-question").click(function () {
        $(".question-initial-info").css("display", "none");
        $(".preview-question").css("display", "block");
        $(".confirmation").css("display", "none");
        $(".main").removeClass("blur-div");
    });
    $(".close-thanks-response").click(function () {
        $(".thanks_response").css("display", "none");
        $(".main").removeClass("blur-div");
    });
    $("input.upload-answer").next().hover(function () {
        $(this).find("svg").find("path").attr("fill", "#3ccd1c");
    }, function () {
        $(this).find("svg").find("path").attr("fill", "#bdbdbd");
    });
    $(".confirmation .upload-file").click(function () {
        $(this).closest("form").find("input.upload-answer").next().slideDown("slow").closest("div.col-12").css("padding-bottom", "15px");
    });
    $(".confirmation .close-upload").click(function () {
        $(this).closest("form").find("input.upload-answer").next().slideUp("slow").closest("div.col-12").css("padding-bottom", "0px");
    });
    $("input.upload-answer").on("change", function () {
        $(this).closest("div").find("img.upload-img").css("display", "none");
        $(this).next("img.file-img").css("display", "block");
        let fileName = $(this).val().split("\\").pop();
        $(this).next().find(".upload-file-text").css("padding-top", "5px")
            .html(fileName);
    });

}

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

$(".delete_edu").click(function () {
    let pk = $(this).attr("value");
    $.ajax({
        method: 'POST',
        url: "/researcher/delete_scientific/",
        dataType: 'json',
        data: {pk: pk},
        success: function (data) {
            $(".row-sci-" + pk).remove();
        },
        error: function (data) {
            console.log(data);
        },
    });
});

$(".delete_stu").click(function () {
    let pk = $(this).attr("value");
    console.log("delete_stu");
    console.log(pk);
    $.ajax({
        method: 'POST',
        url: "/researcher/delete_studious/",
        dataType: 'json',
        data: {pk: pk},
        success: function (data) {
            console.log(pk);
            $(".row-stu-" + pk).remove();
        },
        error: function (data) {
            console.log(data);
        },
    });
});

$(".delete_exe").click(function () {
    let pk = $(this).attr("value");
    console.log("delete_exe");
    console.log(pk);
    $.ajax({
        method: 'POST',
        url: "/researcher/delete_executive/",
        dataType: 'json',
        data: {pk: pk},
        success: function (data) {
            $(".row-exe-" + pk).remove();
            if (!$(".executive > table").hasClass("tbody"))
                console.log("doesnt have tbody");
        },
        error: function (data) {
            console.log(data);
        },
    });
});
    