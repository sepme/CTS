function reset(element) {
    element.removeAttr("style");
}

function init_setup() {
    autosize($("textarea"));

}

function init_windowSize() {
    // if ($(window).width() < 575.98) {
    // } else {
    //     var contentWidth = $(document).innerWidth() - 250;
    //     var contentMargin = 0.0862 * contentWidth - 54.9655;
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

function loading() {
    // $(".main").addClass("blur-div");
    // let canvas = $("#loading-canvas");
    // canvas.drawArc({
    //     strokeStyle: '#000',
    //     strokeWidth: 4,
    //     rounded: true,
    //     endArrow: true,
    //     arrowRadius: 15,
    //     arrowAngle: 90,
    //     x: 160, y: 120,
    //     start: 90,
    //     end: 360,
    //     radius: 50
    // });
}

function blur_div_toggle(content) {
    if ($(content).hasClass("blur-div")) {
        $(content).removeClass("blur-div");
    } else {
        $(content).addClass("blur-div");
    }
}

function input_focus() {
    if ($("input[type='text'],input[type='email'],textarea, input[type='number']").prop("disabled")) {
        $(this).each(function () {
            let inputLabel = "label[for='" + $(this).attr("id") + "']";
            $(inputLabel).addClass("full-focus-out");
            $(inputLabel).css({
                "font-size": "13px",
                "top": "12px",
                "right": "30px",
                "color": "#8d8d8d"
            });

        });
    }
    $("input[type='text'],input[type='email'],textarea, input[type='number']").each(function () {
        let inputLabel = "label[for='" + $(this).attr("id") + "']";
        if ($(this).val() !== '') {
            $(inputLabel).addClass("full-focus-out");
            $(inputLabel).css({
                "font-size": "12px",
                "top": "12px",
                "right": "30px",
                "color": "#6f7285",
                "padding": "0 10px"
            });
        } else {
            $(inputLabel).removeClass("full-focus-out");
            $(inputLabel).css({
                "font-size": "13px",
                "top": "28px",
                "right": "25px",
                "color": "#6f7285",
                "padding": "0"
            });
        }
        if ($(this).hasClass("error")) {
            $(inputLabel).css("color", "#ff4545");
        }
    }).on("focus", function () {
        let inputLabel = "label[for='" + $(this).attr("id") + "']";
        if ($(this).hasClass("solid-label")) {
            return false;
        } else if ($(this).hasClass("error")) {
            let errorDiv = $(this).next(".error");
            $(this).on("change", function () {
                console.log($(this).attr("id"));
                $(this).removeClass("error");
                errorDiv.remove();
            });
        } else {
            $(inputLabel).addClass("full-focus-out");
            $(inputLabel).css({
                "font-size": "12px",
                "top": "12px",
                "right": "30px",
                "color": "#3CCD1C",
                "padding": "0 10px"
            });
            $(this).css("color", "#3ccd1c");
        }
    }).on("focusout", function () {
        let inputLabel = "label[for='" + $(this).attr("id") + "']";
        if ($(this).hasClass("solid-label")) {
            return false;
        } else if ($(this).hasClass("error")) {

        } else {
            $(inputLabel).css("color", "#6f7285");
            if ($(this).val() === '') {
                $(inputLabel).css({
                    "font-size": "13px",
                    "top": "28px",
                    "right": "25px",
                    "color": "#6f7285",
                    "padding": "0"
                });
                $(inputLabel).removeClass("full-focus-out");
            } else {
                $(this).css("color", "#8d8d8d");
                $(inputLabel).css("color", "#8d8d8d");
            }
        }
    });
}

if (window.location.href.indexOf('messages') > -1) {
    function returnFileType(type) {
        type = type.toLowerCase();
        if (type === "pdf" || type === "doc" || type === "gif" || type === "jpg" || type === "png" || type === "ppt"
            || type === "txt" || type === "wmv" || type === "zip") {
            return type;
        } else {
            return "unknown";
        }
    }

    function initMessagePreview() {

        $(".box.preview-message .box-header span.back-arrow").click(function () {
            $(".message-expand").removeClass("show");
            $(".box.hover-enable").removeClass("focus");
        });

        $(".box.hover-enable").click(function () {
            $(".box.hover-enable").removeClass("focus");
            $(this).addClass("focus");

            const id = $(this).attr('id');
            $.ajax({
                url: '/message_detail/' + id,
                data: {},
                dataType: 'json',
                success: function (data) {
                    console.log(data);
                    $(".message-expand").addClass("show");
                    $(".preview-message .box-header h6").html(data.title);
                    $(".preview-message .box-body pre").html(data.text);
                    // let fileName = data.attachment.substring(data.attachment.lastIndexOf("/") + 1).toUpperCase();
                    let file_type = data.attachment.substring(data.attachment.lastIndexOf(".") + 1).toUpperCase()
                    let attachment = "<a  href='/" + data.attachment + "'><div>" +
                        "   <span class='file-type image " + returnFileType(file_type) + "'></span>" +
                        "   <div class='file-name'>" + data.attachment.substring(data.attachment.lastIndexOf('/') + 1, data.attachment.lastIndexOf('.')) + "</div>" +
                        "   <span class='file-type text'>" + file_type + " File</span>" +
                        "</div></a>";
                    $(".preview-message .box-body .attachment").html(attachment);
                    $(".preview-message .box-header .data-modified span").html(data.date);
                },
                error: function (data) {
                    console.log(data);
                }
            });
        });
        // $(".preview-message").click(function () {
        //     $(".fixed-back").removeClass("show");
        //     $(".main").removeClass("blur-div");
        //     blur_div_toggle(".main");
        //     $(".message-show").addClass("show");
        //     close_dialog(".message-show");
        // });

        // $("button.preview-message").click(function () {
        //     const id = $(this).attr('id');
        //     $.ajax({
        //         url: '/message_detail/' + id,
        //         data: {},
        //         dataType: 'json',
        //         success: function (data) {
        //             console.log(data);
        //
        //             $(".message-show .card-head").html(data.title);
        //             $(".message-show .message-text").html(data.text);
        //             let attachment = "<a  href='/" + data.attachment +
        //                 "'><span class='fas fa-paperclip fa-lg'></span></a>";
        //             $(".message-show-head .title").append(attachment);
        //             $(".message-show .establish-time .time-body").html(data.date);
        //         },
        //         error: function (data) {
        //             console.log(data);
        //         }
        //     });
        // });

    }

    function getAllMessages() {
        return $(".tab-content div.card").toArray();
    }

    function messageNav(messages, element) {
        if ($(element).attr("id") === "news-message") {
            $(".tab-content").html("");
            $.each(messages, function (i, val) {
                if ($(val).closest("div").hasClass("news-message")) {
                    $(".tab-content").append(val);
                }
            });
            if ($(".tab-content").is(":empty")) {
                console.log("not message");
            }
        } else if ($(element).attr("id") === "notice-message") {
            $(".tab-content").html("");
            $.each(messages, function (i, val) {
                if ($(val).closest("div").hasClass("notice-message")) {
                    $(".tab-content").append(val);
                }
            });
            if ($(".tab-content").is(":empty")) {
                console.log("not check question");
            }
        } else if ($(element).attr("id") === "alert-message") {
            $(".tab-content").html("");
            $.each(messages, function (i, val) {
                if ($(val).closest("div").hasClass("alert-message")) {
                    $(".tab-content").append(val);
                }
            });
            if ($(".tab-content").is(":empty")) {
                console.log("not answered question");
            }
        }
        initMessagePreview();
        // showQuestion();
    }

    initMessagePreview();
    let messages = getAllMessages();
    $(".nav-pills .nav-link").click(function () {
        messageNav(messages, this);
    });

    let activeTab = 3;
    let messageType = [0, 0, 0];
    $.each(messages, function (i, val) {
        if ($(val).closest("div").hasClass("news-message")) {
            messageType[0]++;
        } else if ($(val).closest("div").hasClass("notice-message")) {
            messageType[1]++;
        } else if ($(val).closest("div").hasClass("alert-message")) {
            messageType[2]++;
        }
    });
    if (messageType[0]) {
        messageNav(messages, ".nav-pills .nav-link#news-message");
    } else if (messageType[1]) {
        $(".nav-pills .nav-link.active").removeClass("active");
        $(".nav-pills .nav-link#notice-message").addClass("active");
        messageNav(messages, ".nav-pills .nav-link#notice-message");
    } else if (messageType[1]) {
        $(".nav-pills .nav-link.active").removeClass("active");
        $(".nav-pills .nav-link#alert-message").addClass("active");
        messageNav(messages, ".nav-pills .nav-link#alert-message");
    } else {
        messageNav(messages, ".nav-pills .nav-link#news-message");
    }
}