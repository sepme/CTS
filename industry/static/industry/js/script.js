$(window).on("load", function () {
    init_windowSize();
    load_dialog();
    $('*').persiaNumber();
}).on("resize", function () {
    init_windowSize();
    load_dialog();
});

function numbersComma(num) {
    let newNum = num.toString();
    return newNum.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
}

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
        "</div>";
    // if (data.required_technique.length != 0) {
    resources += "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "جهت انجام پروژه خود به چه تخصص ها و چه تکنیک ها آزمایشگاهی ای احتیاج دارید؟" +
        "</div>" +
        "<div class='answer'>" +
        data.required_method +
        "</div>" +
        "</div>";
    // }
    resources += "<div>" +
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
        numbersComma(data.required_budget) +
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
        "لطفا راه حل خود را برای حل این مشکل به طور خلاصه توضیح دهید." +
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
        numbersComma(data.predict_profit) +
        "</div></div>";
    $(".project-info-content").html(majors);
}

function setValue(data) {
    $("#v-pills-settings-tab").click(function () {
        setRole(data);
        $('*').persiaNumber();
    });
    $("#v-pills-messages-tab").click(function () {
        setResources(data);
        $('*').persiaNumber();
    });
    $("#v-pills-profile-tab").click(function () {
        setApproach(data);
        $('*').persiaNumber();
    });
    $("#v-pills-home-tab").click(function () {
        setMajors(data);
        $('*').persiaNumber();
    });
}

function setTab(data) {
    if (data.expert_messaged.length === 0) {
        $(".project-comment-innerDiv .add-comment").css("display", "none");
        let no_comment = "<div class='no-comment'>متاسفانه، هنوز پروژه شما توسط استادی  بررسی نشده است.</div>";
        $(".project-comment-innerDiv").append(no_comment);
    } else {
        for (let i = 0; i < data.expert_messaged.length; i++) {
            let tab = "<a class='nav-link' data-toggle='pill'" +
                "role='tab' aria-controls='v-pills-home' aria-selected='true'>" +
                "" +
                data.expert_messaged[i].name +
                "</a>";
            $(".comment-tabs div").append(tab);
            $(".comment-tabs .nav-link:last-child").attr("id", "v-pills-expert-" + data.expert_messaged[i].id);
            if (i === 0) {
                $(".comment-tabs div .nav-link").addClass("active");
            }
        }
        getComments($(".comment-tabs .active").attr("id").replace("v-pills-expert-", ""), data.id);
        $(".comment-tabs .nav-link").click(function () {
            getComments($(this).attr("id").replace("v-pills-expert-", ""), data.id);
        });
    }
}

function expertResume() {
    $(".show-resume").click(function () {
        $(".showProject").slideUp('slow').delay('slow');
        $(".expert-resume").delay('slow').slideDown('slow');
        close_dialog(".expert-resume");
        load_dialog();
        id = $(".comment-tabs .active").attr("id").replace("v-pills-expert-", "")
        $.ajax({
                method: 'GET',
                url: '/expert/get_resume',
                dataType: 'json',
                data: {id :id},
                success: function (data) {
                    var sci_record = JSON.parse(data.sci_record);
                    if (sci_record.length !== 0) {
                        var table_row = "";
                        for (i = 0; i < sci_record.length; i++) {
                            table_row += "<tr>" +
                                "<td>" + sci_record[i].fields.degree + "</td>" +
                                "<td>" + sci_record[i].fields.major + "</td>" +
                                "<td>" + sci_record[i].fields.university + "</td>" +
                                "<td>" + sci_record[i].fields.city + "</td>" +
                                "<td>" + sci_record[i].fields.date_of_graduation + "</td>" +
                                "</tr>";
                            $('.sci_record').html(table_row);
                        }
                    }
                    var executive_record = JSON.parse(data.exe_record);
                    if (executive_record.length !== 0) {
                        var table_row = "";
                        for (i = 0; i < executive_record.length; i++) {
                            table_row += "<tr>" +
                                "<td>" + executive_record[i].fields.executive_post + "</td>" +
                                "<td>" + executive_record[i].fields.date_start_post + "</td>" +
                                "<td>" + executive_record[i].fields.date_end_post + "</td>" +
                                "<td>" + executive_record[i].fields.organization + "</td>" +
                                "<td>" + executive_record[i].fields.city + "</td>" +
                                "</tr>";
                            $('.executive_record').html(table_row);
                        }
                    }
                    var research_record = JSON.parse(data.research_record);
                    console.log(research_record);
                    if (research_record.length !== 0) {
                        var table_row = "";
                        for (i = 0; i < research_record.length; i++) {
                            table_row += "<tr>" +
                                "<td>" + research_record[i].fields.research_title + "</td>" +
                                "<td>" + research_record[i].fields.researcher + "</td>" +
                                "<td>" + research_record[i].fields.co_researcher + "</td>" +
                                "</tr>";
                            $('.research_record').html(table_row);
                        }
                    }
                    var paper_record = JSON.parse(data.paper_record);
                    if (paper_record.length !== 0) {
                        var table_row = "";
                        for (i = 0; i < paper_record.length; i++) {
                            table_row += "<tr>" +
                                "<td>" + paper_record[i].fields.research_title + "</td>" +
                                "<td>" + paper_record[i].fields.date_published + "</td>" +
                                "<td>" + paper_record[i].fields.published_at + "</td>" +
                                "<td>" + paper_record[i].fields.impact_factor + "</td>" +
                                "<td>" + paper_record[i].fields.citation + "</td>" +
                                "</tr>";
                            $('.paper_record').html(table_row);
                        }
                    }
                    $('.researcher_count').html(data.researcher_count);
                    $('.has_industrial_research').html(data.has_industrial_research);
                    $('.awards').html(data.awards);
                    $('.languages').html(data.languages);
                },
        });
    });
}

function setIndustryComment(data) {
    let comments_code = "";
    for (let i = 0; i < data.length; i++) {
        comments_code += "<div class='my-comment'>" +
            "<div class='comment-profile'>" +
            "</div>" +
            "<div class='comment-body'>" +
            "<span class='comment-tools'>" +
            "<i class='fas fa-pen'>" +
            "</i>" +
            "<i class='fas fa-reply'><div class='reply'></div>" +
            "</i>";
        if (data[i].attachment !== "None") {
            comments_code += "<a href='/" +
                data[i].attachment +
                "'><i class='fas fa-paperclip'></i></a>";
        }
        comments_code += "</span>" +
            "<span>" +
            data[i].description +
            "</span>" +
            "</div>" +
            "</div>";
    }
    $('.comments').html(comments_code);
}

function setComment(data) {
    let id = $(".comment-tabs .active").attr("id").replace("v-pills-expert-", "");
    data = data.comment;
    let comments_code = "";
    let profile = $("#profile").attr('src');
    for (let i = 0; i < data.length; i++) {
        if (data[i].sender_type === "industry") { //industry
            comments_code += "<div class='my-comment'>" +
                "<div class='comment-profile'>" +
                "</div>" +
                "<div class='comment-body'>" +
                "<span class='comment-tools'>" +
                "<i class='fas fa-pen'>" +
                "</i>" +
                "<i class='fas fa-reply'><div class='reply'></div>" +
                "</i>";
            if (data[i].attachment !== "None") {
                comments_code += "<a href='/" +
                    data[i].attachment +
                    "'><i class='fas fa-paperclip'></i></a>";
            }
            comments_code += "</span>" +
                "<span>" +
                data[i].text +
                "</span>" +
                "</div>" +
                "</div>";
        } else if (data[i].sender_type === "expert") { //expert
            comments_code += "<div class='your-comment'>" +
                "<div class='comment-body' dir='ltr'>" +
                "<span class='comment-tools'>" +
                "<i class='fas fa-trash-alt'></i>" +
                "<i class='fas fa-reply' value=" +
                data[i].pk +
                "></i>" +
                "<i class='fas fa-pen'>" +
                "</i>";
            if (data[i].attachment !== "None") {
                comments_code += "<a href='/" +
                    data[i].attachment +
                    "'><i class='fas fa-paperclip'></i></a>";
            }
            comments_code += "</span>" +
                "<span>" +
                data[i].text +
                "</span>" +
                "</div>" +
                "</div>";
        } else { //system
            comments_code += "<div class='my-comment'>" +
                "<div class='comment-body' dir='ltr'>" +
                "<span>" +
                data[i].text +
                "</span>" +
                "</div>" +
                "</div>";
        }
    }
    $('.comments').html(comments_code).animate({scrollTop: $('.comments').prop("scrollHeight")}, 1000);
}

function tag_input_label(tag_input) {
    $("#" + tag_input + "_tagsinput .tags_clear").css("display", "none");
    $("#" + tag_input + "_tagsinput span.tag a").html("<i class='fas fa-times'></i>");

    if (!$(".tagsinput").find(".tag").length) {
        $("label[for='" + tag_input + "']").removeClass("full-focus-out").css({
            "font-size": "13px",
            "top": "28px",
            "right": "25px",
            "color": "#6f7285",
            "padding": "0"
        });
        $("#" + tag_input + "_tag").attr("placeholder", "");
    }

    $("#" + tag_input + "_tag").on("focus", function () {
        $("label[for='" + tag_input + "']").addClass("full-focus-out").css({
            "font-size": "12px",
            "top": "12px",
            "right": "30px",
            "padding": "0 10px",
            "color": "#3ccd1c"
        });
        $(".tagsinput").css("border-color", "#3ccd1c");
    }).on("focusout", function () {

        $(".tagsinput").css("border-color", "#bdbdbd85");

        if ($(".tagsinput").find(".tag").length) {
            $("label[for='" + tag_input + "']").addClass("full-focus-out").css({
                "font-size": "12px",
                "top": "12px",
                "right": "30px",
                "padding": "0 10px",
                "color": "#6f7285"
            });
        } else {
            $("label[for='" + tag_input + "']").removeClass("full-focus-out").css({
                "font-size": "13px",
                "top": "28px",
                "right": "25px",
                "color": "#6f7285",
                "padding": "0"
            });
            $("#" + tag_input + "_tag").attr("placeholder", "");
        }
    });
}

function newItem_label() {
    $("#id_key_words_tagsinput").find("#id_key_words_tag").attr("placeholder", "افزودن");
    tag_input_label("id_key_words");
}

function getComments(expert_id, project_id) {
    $.ajax({
        method: 'GET',
        url: 'get_comment/',
        dataType: 'json',
        data: {
            expert_id: expert_id,
            project_id: project_id
        },
        success: function (data) {
            setComment(data);
        },
        error: function (data) {

        },
    });
}

function addComment(data) {
    let new_comment = "<div class='my-comment'>" +
        "<div class='comment-profile'>" +
        "</div>" +
        "<div class='comment-body'>" +
        "<span class='comment-tools'>" +
        "<i class='fas fa-pen'>" +
        "</i>" +
        "<i class='fas fa-reply'><div class='reply'></div>" +
        "</i>";
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
    // let new_comment = "<div class='my-comment'>" +
    //             "<div class='comment-body' dir='ltr'>" +
    //             "<span class='comment-tools'>";
    //             if (data.attachment !== "None") {
    //                 new_comment += "<a href='/" +
    //                                 data.attachment +
    //                                 "'><i class='fas fa-paperclip'></i></a>" ;   
    //             }
    //         new_comment += "</span>" +
    //             "<span>" +
    //             data.description +
    //             "</span>" +
    //             "</div>" +
    //             "</div>";
    console.log(new_comment);
    return new_comment;
}

$(document).ready(function () {
        $(".chamran-btn-info").click(function () {
            const dialog = $(".showProject");
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
                url: '/industry/show_project/',
                dataType: 'json',
                data: {id: id},
                success: function (data) {
                    console.log(data);
                    localStorage.setItem("project_id", "" + id);
                    localStorage.setItem("replied_text", null);
                    dialog.find(".project-title").html(data.project_title_persian + " (" + data.project_title_english + ")");
                    dialog.find(".establish-time .time-body").html(data.submission_date);
                    dialog.find(".time-left .time-body").html(data.deadline);
                    for (let i = 0; i < data.key_words.length; i++) {
                        dialog.find(".techniques").append(
                            "<span class='border-span'>" +
                            data.key_words[i]
                            + "</span>"
                        );
                    }
                    dialog.find('.card-head').html(data.project_title_persian);
                    setMajors(data);
                    setValue(data);
                    console.log(data.expert_messaged);
                    if (data.status !== 0) {
                        if (data.vote === "false") {
                            $(".vote").remove();
                        }
                        setTab(data);
                    } else {
                        $('.vote').remove();
                        $('.add-comment').remove();
                    }
                },
                error: function (data) {

                },
            });
        });

        $("#id_key_words_tagsinput").find("#id_key_words_tag").on("focus", function () {
            $(this).css("width", "fit-content");
        });

        $('#id_key_words').tagsInput({
            'height': 'FIT-CONTENT',
            'width': '100%',
            'defaultText': '',
            'onAddTag': newItem_label,
            'onRemoveTag': newItem_label
        });
        tag_input_label("id_key_words");
// variable
        edu_count = 0;
        exe_count = 0;
        stu_count = 0;
        art_count = 0;
        search_input(".search_message");
        input_focus();
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
            init_dialog_btn(".message-body button, .message-body-sm button", ".message-show");
            expertResume();
            // if($(".mainInfo-body").css("display") === "block"){
            //     blur_div_toggle(".top-bar");
            //     blur_div_toggle(".side-bar");
            // }
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
            $(".chamran_btn.education-btn").click(function () {
                div = document.createElement("div");
                $(div).addClass('card').addClass('ch-card-item');
                $(div).attr("id", edu_count);
                $(div).html("<div class='row'>" +
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
                    "<div class='col-lg-2' style='display:flex'>" +
                    "<div class='wait-item' id='" + edu_count + "'>" +
                    "<span>منتظر تایید....</span>" +
                    "<i class='fas fa-clock'></i>" +
                    "</div>" +
                    "<div class='delete-item' id='" + edu_count + "'>" +
                    "<span>حذف</span>" +
                    "<i class='fas fa-trash'></i>" +
                    "</div>" +
                    "</div>" +
                    "</div>");
                $('.education').append(div);
                delete_item(".education");
                input_focus();
                edu_count++;
            });
            $(".chamran_btn.executive-btn").click(function () {
                div = document.createElement("div");
                $(div).addClass('card').addClass('ch-card-item');
                $(div).attr("id", exe_count);
                $(div).html("<div class='row'>" +
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
                    "<label for='workplace" + exe_count + "'>محل خدمت</label>" +
                    "<input type='text' id='workplace" + exe_count + "' class='w-100'>" +
                    "</div>" +
                    "<div class='col-lg-4'>" +
                    "<label for='exe-city" + exe_count + "'>شهر</label>" +
                    "<input type='text' id='exe-city" + exe_count + "' class='w-100'>" +
                    "</div>" +
                    "<div class='col-lg-3' style='display:flex'>" +
                    "<div class='wait-item' id='" + exe_count + "'>" +
                    "<span>منتظر تایید....</span>" +
                    "<i class='fas fa-clock'></i>" +
                    "</div>" +
                    "<div class='delete-item' id='" + exe_count + "'>" +
                    "<span>حذف</span>" +
                    "<i class='fas fa-trash'></i>" +
                    "</div>" +
                    "</div>" +
                    "</div>");
                $('.executive').append(div);
                delete_item(".executive");
                input_focus();
                $("#from" + exe_count).persianDatepicker({});
                $("#until" + exe_count).persianDatepicker({});
                exe_count++;
            });
            $(".chamran_btn.studious-btn").click(function () {
                div = document.createElement("div");
                $(div).addClass('card').addClass('ch-card-item');
                $(div).attr("id", stu_count);
                $(div).html("<div class='row'>" +
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
                    "<div class='col-lg-5' style='display:flex'>" +
                    "<div class='wait-item' id='" + stu_count + "'>" +
                    "<span>منتظر تایید....</span>" +
                    "<i class='fas fa-clock'></i>" +
                    "</div>" +
                    "<div class='delete-item' id='" + stu_count + "'>" +
                    "<span>حذف</span>" +
                    "<i class='fas fa-trash'></i>" +
                    "</div>" +
                    "</div>" +
                    "</div>");
                $('.studious').append(div);
                delete_item(".studious");
                input_focus();
                stu_count++;
            });
            $(".chamran_btn.article-btn").click(function () {
                div = document.createElement("div");
                $(div).addClass('card').addClass('ch-card-item');
                $(div).attr("id", art_count);
                $(div).html("<div class='row'>" +
                    "<div class='col-lg-4'>" +
                    "<label for='article-name" + art_count + "'>عنوان مقاله</label>" +
                    "<input type='text' id='article-name" + art_count + "' class='w-100'>" +
                    "</div>" +
                    "<div class='col-lg-4'>" +
                    "<label for='publish-date" + art_count + "'>تاریخ انتشار</label>" +
                    "<input type='text' id='publish-date" + art_count + "' class='w-100'>" +
                    "</div>" +
                    "<div class='col-lg-4'>" +
                    "<label for='published-at" + art_count + "'>محل دقیق انتشار</label>" +
                    "<input type='text' id='published-at" + art_count + "' class='w-100'>" +
                    "</div>" +
                    "</div>" +
                    "<div class='row'>" +
                    "<div class='col-lg-5'>" +
                    "<label for='impact-factor" + art_count + "'>Impact Factor</label>" +
                    "<input type='text' id='impact-factor" + art_count + "' class='w-100'>" +
                    "</div>" +
                    "<div class='col-lg-4'>" +
                    "<label for='referring-num" + art_count + "'>تعداد ارجاع به مقاله شما</label>" +
                    "<input type='text' id='referring-num" + art_count + "' class='w-100'>" +
                    "</div>" +
                    "<div class='col-lg-3' style='display:flex'>" +
                    "<div class='wait-item' id='" + art_count + "'>" +
                    "<span>منتظر تایید....</span>" +
                    "<i class='fas fa-clock'></i>" +
                    "</div>" +
                    "<div class='delete-item' id='" + art_count + "'>" +
                    "<span>حذف</span>" +
                    "<i class='fas fa-trash'></i>" +
                    "</div>" +
                    "</div>" +
                    "</div>");
                $('.article').append(div);
                delete_item(".article");
                input_focus();
                art_count++;
            });
            $(".chamran_btn.technique").click(function () {
                $(".main").addClass("blur-div");
                $(".dialog-main").css("display", "block");
                close_dialog();
            });
            let comment_form = $('#comment-form');
            comment_form.submit(function (event) {
                event.preventDefault();
                comment_form.find("button[type='submit']").css("color", "transparent").addClass("loading-btn").attr("disabled", "true");
                comment_form.find("label").addClass("progress-cursor");
                $("#project_id").attr('value', $(".show-project").attr("id"));
                $("#expert_id").attr('value', $(".comment-tabs .active").attr("id").replace("v-pills-expert-", ""));
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
                        comment_code = addComment(data);
                        $(".project-comment-innerDiv").find(".comments").append(comment_code);
                        iziToast.success({
                            rtl: true,
                            message: "پیام با موفقیت ارسال شد!",
                            position: 'bottomLeft'
                        });
                        comment_form[0].reset();
                        $('.comments').animate({scrollTop: $('.comments').prop("scrollHeight")}, 1000);
                    },
                    error: function (data) {
                        console.log(data);
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
            // $(".chamran_btn").click(function () {
            //     var comment_obj = $("#comment");
            //     var comment_description = comment_obj.val();
            //     addComment(comment_description);
            //     console.log(comment_description);
            //     $.ajax({
            //         method: 'GET',
            //         url: '/industry/submit_comment/',
            //         dataType: 'json',
            //         data: {
            //             description: comment_description,
            //             project_id: localStorage.getItem("project_id"),
            //         },
            //         success: function (data) {
            //             localStorage.setItem("replied_text", null);
            //             // display the comment
            //
            //         },
            //     });
            //     comment_obj.val("");
            // });
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
    }
);