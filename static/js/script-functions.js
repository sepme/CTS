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
    $(".main").addClass("blur-div");
    var canvas = $("#loading-canvas");
    canvas.drawArc({
        strokeStyle: '#000',
        strokeWidth: 4,
        rounded: true,
        endArrow: true,
        arrowRadius: 15,
        arrowAngle: 90,
        x: 160, y: 120,
        start: 90,
        end: 360,
        radius: 50
    });
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
            var inputLabel = "label[for='" + $(this).attr("id") + "']";
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
        var inputLabel = "label[for='" + $(this).attr("id") + "']";
        if ($(this).val() !== '') {
            $(inputLabel).addClass("full-focus-out");
            $(inputLabel).css({
                "font-size": "12px",
                "top": "12px",
                "right": "30px",
                "color": "#6f7285",
                "padding": "0 10px"
            });
        }
        if ($(this).hasClass("error")) {
            $(inputLabel).css("color", "#ff4545");
        }
    }).on("focus", function () {
        var inputLabel = "label[for='" + $(this).attr("id") + "']";
        if ($(this).hasClass("solid-label")) {
            return false;
        } else if ($(this).hasClass("error")) {
            var errorDiv = $(this).next(".error");
            $(this).on("change", function () {
                if ($(this).hasClass("error")) {
                    $(this).removeClass("error");
                    $(errorDiv).remove();
                }
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
        var inputLabel = "label[for='" + $(this).attr("id") + "']";
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