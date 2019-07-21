function load_dialog(){
    $(".title-back").each(function () {
        var title_back_width = $(this).prev().outerWidth() + 30;
        $(this).css("width", title_back_width);
    });
    $(".row-header > .header").each(function () {
        var divWidth = $(this).outerWidth();
        divWidth = $(this).closest("div").innerWidth() - divWidth;
        $(this).prev().css("width",divWidth/2 - 10);
        $(this).next().css("width",divWidth/2 - 10);
        $(this).css("left", (divWidth)/2 );
    });
}
function init_windowSize() {
    if($(window).width() < 575.98){
    }else {
        var contentWidth = $(document).innerWidth() - 250;
        var contentMargin = 0.0862 * contentWidth - 63.9655;
        $(".info-card").css({
            "margin-right": contentMargin,
            "margin-left": contentMargin
        });
        $(".content").css({
            "width": contentWidth,
            "height": "90%"
        });
        $(".side-bar").css("height", "100%");
    }
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
    if($(content).hasClass("blur-div")) {
        $(content).removeClass("blur-div");
    }else {
        $(content).addClass("blur-div");
    }
}
function init_dialog_btn(element, dialogClass) {
    $(element).click(function (){
        blur_div_toggle(".main");
        $(dialogClass).css("display","block");
        close_dialog(dialogClass);
        dialog_comment_init();
        load_dialog();
        // $(".project-info-innerDiv").height($(".project-info-content").outerHeight());
        if( dialogClass === ".showProject"){
            accept_project();
        }
    });
}
function input_focus(){
    if( $("input,textarea").prop("disabled") ) {
        $(this).each(function () {
            var inputLabel = "label[for='"+$(this).attr("id")+"']";
            $(inputLabel).css({
                "font-size":"13px",
                "top":"0px",
                "right":"15px",
                "color":"#8d8d8d"
            });
        });
    }
    $("input,textarea").on("focus", function () {
        if($(this).hasClass("solid-label"))
            return false;
        var inputLabel = "label[for='"+$(this).attr("id")+"']";
        $(inputLabel).css({
            "font-size":"13px",
            "top":"0px",
            "right":"15px",
            "color":"#3CCD1C"
        });
        $(this).css("color","#3ccd1c");
    }).on("focusout", function () {
        if($(this).hasClass("solid-label"))
            return false;
        var inputLabel = "label[for='"+$(this).attr("id")+"']";
        $(inputLabel).css("color","#6f7285");
        if($(this).val() === ''){
            $(inputLabel).css({
                "font-size":"14px",
                "top":"28px",
                "right":"25px",
                "color":"#6f7285"
            });
        }else {
            $(this).css("color","#8d8d8d");
            $(inputLabel).css("color","#8d8d8d");
        }
    });
}
function delete_item(className){
    div = "<span class='initial-value' style='border: 1px dashed #bdbdbd;width: fit-content;border-radius: 0.25em;padding: 5px 10px;font-size: 13px;font-weight: 300;'>برای افزودن سابقه جدید روی <i class='fas fa-plus'></i>  کلیک کنید!  </span>";
    $(".refuse-btn").click(function () {
        $(className+ " div#" + $(this).attr("id")).remove();
        if($(className).val() === '') {
            $(className).append(div);
        }
    });
}
function accept_project(){
    $(".accept-btn").click(function () {
        $(".showProject").slideUp('slow').delay('slow');
        $(".project-details").delay('slow').slideDown('slow');
        close_dialog(".project-details");
        load_dialog();
    });
}
function close_dialog(className){
    $(".close").click(function (){
        $(className).css("display","none");
        $(".main").removeClass("blur-div");
    });
}
function dialog_comment_init() {
    // add emoji to comment
    $(".new-comment-tools > .fa-smile").click(function() {
        alert("Not working");
        // $('#comment').emojiPicker('toggle');
        // alert("a");
    });
    // delete user comment
    $(".comment-tools > .fa-trash-alt").click(function () {
        $(this).parents("div.my-comment").remove();
    });
    // attach file to comment
    $(".new-comment-tools > label[for='comment-attach']").click(function () {
        rows = $("textarea#comment").attr("rows");
        $("textarea#comment").attr("rows", ++rows);
        padding_bottom = parseInt($("textarea#comment").css("padding-bottom")) + 30;
        $("textarea#comment").css("padding-bottom", padding_bottom);

        if($("div.attachment > div").last().hasClass("attach")){
            bottom_position = parseInt($("div.attachment > div").last().css("bottom"));
        }else {
            bottom_position = 10;
        }

        $("div.attachment").append("<div class='attach'>" +
            "<span>" + "نام فایل" + "</span>" +
            "<div class='progress'>" +
                "<div class='progress-bar progress-bar-striped progress-bar-animated' role='progressbar' aria-valuenow='75' aria-valuemin='0' aria-valuemax='100' style='width: 75%'></div>" +
            "</div>" +
        "</div>");
        $("div.attachment > div").last().css("bottom", bottom_position + 30);
    });
    // replay to a comment
    $(".comment-tools > .fa-reply").click(function () {
        var text = $.trim($(this).closest("div").children(2).text());
        $("textarea#comment").closest("div").append("<div class='replay-div'></div>");
        $(".replay-div").html("<i class='fa fa-reply fa-lg'></i>" + text + "<i class='fa fa-times'></i>");
        $(".replay-div > .fa-times").click(function () {
           $(".replay-div").remove();
           $("textarea#comment").css("padding-top","2px").focus().on("focusout", function () {
                var inputLabel = "label[for='"+$(this).attr("id")+"']";
                $(inputLabel).css("color","#6f7285");
                if($(this).val() === ''){
                    $(inputLabel).css({
                        "font-size":"14px",
                        "top":"28px",
                        "right":"25px",
                        "color":"#6f7285"
                    });
                }else {
                    $(this).css("color","#8d8d8d");
                    $(inputLabel).css("color","#8d8d8d");
                }
            });
        });
        $("textarea#comment").css("padding-top","35px").focus().on("focusout", function () {
            var inputLabel = "label[for='"+$(this).attr("id")+"']";
            $(inputLabel).css("color","#6f7285");
            if($(this).val() === ''){
                $(inputLabel).css({
                    "font-size":"14px",
                    "top":"58px",
                    "right":"25px",
                    "color":"#6f7285"
                });
            }else {
                $(this).css("color","#8d8d8d");
                $(inputLabel).css("color","#8d8d8d");
            }
        });
    });
    // edit user comment
    $(".comment-tools > .fa-pen").click(function () {
        text = $.trim($(this).closest("div").children(2).text());
        $("textarea#comment").html(text);
        $("textarea#comment").focus();
    });
}
