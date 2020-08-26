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

function init_dialog_btn(element, dialogClass) {
    vote_dialog_init(dialogClass);
    $(element).click(function () {
        $(".fixed-back").removeClass("show");
        $(".main").removeClass("blur-div");
        blur_div_toggle(".main");
        $(dialogClass).addClass("show");
        close_dialog(dialogClass);
        dialog_comment_init();
        load_dialog();
        if (dialogClass === ".showProject") {
            $(dialogClass).removeAttr("id");
            $(dialogClass).attr("id", $(this).attr("id"));
        }
    });
}

function modalPreview(modalClass) {
    vote_dialog_init(modalClass);
    $(".fixed-back").removeClass("show");
    $(".main").removeClass("blur-div");
    blur_div_toggle(".main");
    $(modalClass).addClass("show");
    close_dialog(modalClass);
    dialog_comment_init();
    load_dialog();
    if (modalClass === ".showProject") {
        $(modalClass).removeAttr("id");
        $(modalClass).attr("id", $(this).attr("id"));
    }
}

// function cancel_add(className) {
//     let div = "<span class='initial-value' style='border: 1px dashed #bdbdbd;width: fit-content;border-radius: 0.25em;padding: 5px 10px;font-size: 13px;font-weight: 300;'>برای افزودن سابقه جدید روی <i class='fas fa-plus'></i>  کلیک کنید!  </span>";
//     $(".refuse-btn").click(function () {
//         $(className + " div#" + $(this).attr("id")).remove();
//         alert($(className).val());
//         if ($(className).val() === '') {
//             $(className).append(div);
//         }
//     });
// }

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
        if (className === ".showProject") {
            $(className).find(".techniques").html("");
            $(className).find(".card-head").html("");
            $(className).find(".time-body").html("");
            $(className).find(".project-info-content").html("");
            $(className).find(".comments").html("");
            $(className).find(".message").remove();
            $(className).find(".message.info").remove();
        }
        // if (className === ".expert-resume") {
        //     $(".expert-resume").slideUp('slow').delay('slow');
        //     $(".showProject").delay('slow').slideDown('slow');
        // }
        $(className).find(".no-comment").remove();
        $(className).find(".comment-tabs .nav").html("");
    });
}

//
// function addComment(comment) {
//     let newPost = "<div class=\"my-comment\" style='display: none'><div class=\"comment-profile\"></div><div class=\"comment-body\" dir=\"ltr\"><span class=\"comment-tools\"><i class=\"fas fa-trash-alt\"></i><i class=\"fas fa-reply\"></i><i class=\"fas fa-pen\"></i></span><span>" + comment + "</span></div></div>";
//     let $comments = $(".comments");
//     $comments.html(newPost + $comments.html());
//
// }
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

function dialog_comment_init() {
    $(".send-comment-container .comment-input input#comment-attach").on("change", function () {
        let fileName = $(this).val().split("\\").pop();
        $(".send-comment-container .comment-input .attachment span").html(fileName);
        $(".send-comment-container .comment-input").addClass("attached");

        $(".send-comment-container .comment-input.attached i.fa-trash-alt").click(function () {
            $(".send-comment-container .comment_formcomment-input input#comment-attach").val("");
            $(".send-comment-container .comment-input .attachment span").html("");
            $(".send-comment-container .comment-input").removeClass("attached");
        });
    });
    let comment_form = $('#comment-form');
    $(comment_form).off("submit");
    comment_form.submit(function (event) {
        event.preventDefault();
        comment_form.find("button[type='submit']").css("color", "transparent").addClass("loading-btn").attr("disabled", "true");
        comment_form.find("label").addClass("progress-cursor");
        comment_form.find("input#project_id").attr('value', comment_form.closest(".add-comment").attr("id"));
        if ($(this).find("#expert_id").val() === "") {
            $("#expert_id").attr('value', $(this).closest(".row").find(".comment-tabs .active").attr("id")
                .replace("v-pills-expert-", ""));
        }
        console.log($("#project_id").val());
        console.log($("#expert_id").val());
        let thisUrl = "/industry/submit_comment/";
        let data = new FormData(comment_form.get(0));
        $.ajax({
            method: 'POST',
            url: thisUrl,
            data: data,
            type: "ajax",
            processData: false,
            contentType: false,
            success: function (data) {
                comment_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                    .prop("disabled", false);
                comment_form.find("label").removeClass("progress-cursor");
                comment_form.closest(".fixed-back").find(".card").removeClass("wait");
                let PCID = $(".project-comment-innerDiv");
                if (PCID.find(".no-comment").length > 0) {
                    PCID.find(".no-comment").remove();
                }
                let comment_code = addComment(data);
                PCID.find(".comments").append(comment_code);
                iziToast.success({
                    rtl: true,
                    message: "پیام با موفقیت ارسال شد!",
                    position: 'bottomLeft'
                });

                comment_form[0].reset();
                comment_form.find("#description").css("height", "fit-content");
                comment_form.closest(".section").find("textarea#description").removeClass("error");
                comment_form.closest(".section").find('.error').remove();
                comment_form.closest(".section").find('.file-name').html("");
                comment_form.closest(".section").find(".send-comment-container .comment-input").removeClass("attached");
                comment_form.closest(".section").find('.comments').animate({scrollTop: comment_form.closest(".section").find('.comments').prop("scrollHeight")}, 1000);
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
    // add emoji to comment
    // $(".new-comment-tools > .fa-smile").click(function () {
    //     alert("Not working");
    //     // $('#comment').emojiPicker('toggle');
    //     // alert("a");
    // });
    // delete user comment
    // $(".comment-tools > .fa-trash-alt").click(function () {
    //     $(this).parents("div.my-comment").remove();
    // });
    // attach file to comment
    // $(".new-comment-tools > label[for='comment-attach']").click(function () {
    //     rows = $("textarea#comment").attr("rows");
    //     $("textarea#comment").attr("rows", ++rows);
    //     padding_bottom = parseInt($("textarea#comment").css("padding-bottom")) + 30;
    //     $("textarea#comment").css("padding-bottom", padding_bottom);
    //
    //     if ($("div.attachment > div").last().hasClass("attach")) {
    //         bottom_position = parseInt($("div.attachment > div").last().css("bottom"));
    //     } else {
    //         bottom_position = 10;
    //     }
    //
    //     $("div.attachment").append("<div class='attach'>" +
    //         "<span>" + "نام فایل" + "</span>" +
    //         "</div>");
    //         // "<div class='progress'>" +
    //         // "<div class='progress-bar progress-bar-striped progress-bar-animated' role='progressbar' aria-valuenow='75' aria-valuemin='0' aria-valuemax='100' style='width: 75%'></div>" +
    //         // "</div>" +
    //     $("div.attachment > div").last().css("bottom", bottom_position + 30);
    // });
    // // replay to a comment
    // $(".comment-tools > .fa-reply").click(function () {
    //     var text = $.trim($(this).closest("div").children(2).text());
    //     $("textarea#comment").closest("div").append("<div class='replay-div'></div>");
    //     $(".replay-div").html("<i class='fa fa-reply fa-lg'></i>" + text + "<i class='fa fa-times'></i>");
    //     $(".replay-div > .fa-times").click(function () {
    //         $(".replay-div").remove();
    //         $("textarea#comment").css("padding-top", "2px").focus().on("focusout", function () {
    //             var inputLabel = "label[for='" + $(this).attr("id") + "']";
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
    //         var inputLabel = "label[for='" + $(this).attr("id") + "']";
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

function vote_dialog_init(className) {
    let flag = 0;
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
    $(className + " .vote").click(function () {
        if ($('.vote-dialog').css('display') === 'none') {
            $('.vote-dialog').slideDown();
            $('.vote').addClass('expand');
        } else {
            $('.vote-dialog').slideUp();
            $('.vote').removeClass('expand');
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
        vote_slider(12);
        $(".progress-line").css("width", "calc(100% / 12)");
    });
}

function vote_slider(slide_count) {
    counter = 0;
    $(".next-button").click(function () {
        if (counter < slide_count - 1) {
            counter++;
            progressWidth = parseInt($(".vote-list > .vote-item").css('width'));
            width = parseFloat($(".progress-line").css('width'));
            $(".progress-line").css('width', width + progressWidth);

            $(".swiper-wrapper").css({
                "transform": "translate3d(-" + 100 * counter + "%, 0, 0)",
                "transition-duration": "0.3s"
            });
        }
        if (counter === slide_count - 1) {
            $(this).html("<i class='fas fa-check'></i>" +
                "ثبت");
        }
        if (counter > 0) {
            $(".prev-button").removeClass("disabled");
        }
    });
    $(".prev-button").click(function () {
        if (counter > 0) {
            counter--;
            progressWidth = parseInt($(".vote-list > .vote-item").css('width'));
            width = parseFloat($(".progress-line").css('width'));
            $(".progress-line").css('width', width - progressWidth);

            $(".swiper-wrapper").css({
                "transform": "translate3d(-" + 100 * counter + "%, 0, 0)",
                "transition-duration": "0.3s"
            });
        }
        if (counter === slide_count - 2) {
            $(".next-button").html("<i class='fas fa-arrow-right'></i>" +
                "بعدی");
        }
        if (counter === 0) {
            $(this).addClass('disabled');
        }
    });
}