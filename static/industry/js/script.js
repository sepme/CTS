function numbersComma(num) {
    let newNum = num.toString();
    return newNum.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
}

function setEthicalConsider(data, status) {
    let role = "";
    if (data.policy)
        role += `<div>
                    <div class="question">
                        <span class="question-mark"><i class='far fa-question-circle'></i></span> 
                        <span>
                            ملاحظات اخلاقی
                        </span>
                        <div class='answer'>${data.policy}</div>
                    </div>
                </div>`;
    if (data.executive_restrictions)
        role += `<div>
                    <div class="question">
                        <span class="question-mark"><i class='far fa-question-circle'></i></span> 
                        <span>
                            محدودیت های اجرایی طرح و روش کاهش آن ها
                        </span>
                        <div class='answer'>${data.executive_restrictions}</div>
                    </div>
                </div>`;
    $(".project-info-content" + status).html(role);
}

function setGoal(data, status) {
    let goal = "";
    if (data.main_goal)
        goal += `<div>
                    <div class='question'>
                        <span class='question-mark'>
                            <i class='far fa-question-circle'></i>
                        </span>                                    
اهداف اصلی                       
                    </div>
                    <div class='answer'>${data.main_goal}</div>
                </div>`;
    if (data.secondary_goal)
        goal += `<div>
                    <div class='question'>
                        <span class='question-mark'>
                            <i class='far fa-question-circle'></i>
                        </span>                                    
اهداف فرعی                       
                    </div>
                    <div class='answer'>${data.secondary_goal}</div>
                </div>`;
    if (data.practical_goal)
        goal += `<div>
                    <div class='question'>
                        <span class='question-mark'>
                            <i class='far fa-question-circle'></i>
                        </span>                                    
اهداف کاربردی                       
                    </div>
                    <div class='answer'>${data.practical_goal}</div>
                </div>`;
    if (data.research_question)
        goal += `<div>
                    <div class='question'>
                        <span class='question-mark'>
                            <i class='far fa-question-circle'></i>
                        </span>                                    
سوالات پژوهش                       
                    </div>
                    <div class='answer'>${data.research_question}</div>
                </div>`;
    if (data.reseach_assumptions)
        goal += `<div>
                    <div class='question'>
                        <span class='question-mark'>
                            <i class='far fa-question-circle'></i>
                        </span>                                    
فرضیات پژوهش                       
                    </div>
                    <div class='answer'>${data.reseach_assumptions}</div>
                </div>
                `;
    $(".project-info-content" + status).html(goal);
}

function setProcedure(data, status) {
    let procedure = `<div>
                        <div class='question'>
                            <span class='question-mark'>
                                <i class='far fa-question-circle'></i>
                            </span>                                    
خلاصه ضرورت اجرا                            
                        </div>
                        <div class='answer'>${data.summary_method}</div>
                     </div>`;
    if (data.required_equipment)
        procedure += `<div>
                        <div class='question'>
                            <span class='question-mark'>
                                <i class='far fa-question-circle'></i>
                            </span>                                    
مشخصات ابزار جمع آوری اطلاعات و نحوه جمع آوری آن                            
                        </div>
                        <div class='answer'>${data.required_equipment}</div>
                     </div>`;
    if (data.sample_count_method)
        procedure += `<div>
                        <div class='question'>
                            <span class='question-mark'>
                                <i class='far fa-question-circle'></i>
                            </span>                                    
روش محاسبه حجم نمونه و تعداد آن                            
                        </div>
                        <div class='answer'>${data.sample_count_method}</div>
                     </div>`;
    if (data.analyse_method)
        procedure += `<div>
                        <div class='question'>
                            <span class='question-mark'>
                                <i class='far fa-question-circle'></i>
                            </span>                                    
روش تجزیه و تحلیل داده ها                            
                        </div>
                        <div class='answer'>${data.analyse_method}</div>
                     </div>`;
    $(".project-info-content" + status).html(procedure);
}

function setProblemStatement(data, status) {
    let problemStatement = `<div>
                                <div class='question'>
                                    <span class='question-mark'>
                                        <i class='far fa-question-circle'></i>
                                    </span>                                    
خلاصه ضرورت اجرا                                    
                                </div>
                                <div class='answer'>${data.summary_of_necessity}</div>
                            </div>`;
    if (data.necessity_expression)
        problemStatement += `<div>
                                <div class='question'>
                                    <span class='question-mark'>
                                        <i class='far fa-question-circle'></i>
                                    </span>                                    
مشروح بیان مسئله و ضرورت اجرا                                    
                                </div>
                                <div class='answer'>${data.necessity_expression}</div>
                            </div>`;
    if (data.research_history)
        problemStatement += `<div>
                                <div class='question'>
                                    <span class='question-mark'>
                                        <i class='far fa-question-circle'></i>
                                    </span>                                    
سابقه طرح و بررسی متون                                    
                                </div>
                                <div class='answer'>${data.research_history}</div>
                            </div>`;
    $(".project-info-content" + status).html(problemStatement);
}

// "<div>" +
// "<div class='question'>" +
// "<span class='question-mark'>" +
// "<i class='far fa-question-circle'></i>" +
// "</span>" +
// "برآورد شما از سود مالی این پروژه چگونه است؟" +
// "</div>" +
// "<div class='answer'>" +
// numbersComma(data.predict_profit) +
// " ریال" +
// "</div></div>";

function setValue(data, status) {
    $("#v-pills-roles-tab" + status).click(function () {
        setEthicalConsider(data, status);
        $('*').persiaNumber();
    });
    $("#v-pills-resources-tab" + status).click(function () {
        setGoal(data, status);
        $('*').persiaNumber();
    });
    $("#v-pills-approaches-tab" + status).click(function () {
        setProcedure(data, status);
        $('*').persiaNumber();
    });
    $("#v-pills-majors-tab" + status).click(function () {
        setProblemStatement(data, status);
        $('*').persiaNumber();
    });
}

function setTab(data) {
    if (data.expert_messaged.length === 0) {
        $(".project-comment-innerDiv .add-comment").css("display", "none");
        let no_comment = `<div class='no-comment not-requested'>
            <img src='../../../../static/img/hourglass.svg' alt=''>
            <h6>لطفا شکیبا باشید!</h6>
            <pre>متاسفانه، هنوز پروژه شما توسط استادی بررسی نشده است.</pre>
            </div>`;
        $(".project-comment-innerDiv").append(no_comment);
        $(".project-comment-innerDiv .no-comment.not-requested").addClass("show");
        $(".confirm-request").attr("style", "display : none");
        $(".comment").attr("style", "display : none");
        $(".comments").attr("style", "display : none");
    } else {
        $(".confirm-request").attr("style", "display : block");
        $(".comment").attr("style", "display : block");
        $(".comments").attr("style", "display : block");
        for (let i = 0; i < data.expert_messaged.length; i++) {
            let tab = "<a class='nav-link' data-toggle='pill'" +
                " role='tab' aria-controls='v-pills-home' aria-selected='true'>" +
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
    $("[data-target='#expertResume']").click(function () {
        let modal = $('#expertResume');
        if ($('.modal#showProject').length) {
            $('#showProject').modal('hide');
            modal.modal('show');
            $('#expertResume .close__redirect').click(function () {
                modal.modal('hide');
                $('#showProject').modal('show');
            });
        } else {
            modal.modal('show');
            $('#expertResume .close__redirect').click(function () {
                modal.modal('hide');
            });
        }
        if ($(this).hasClass("rounded-name-profile")) {
            let tab = `<a class='nav-link active d-none' data-toggle='pill' role='tab' aria-controls='v-pills-home'
                aria-selected='true' id="v-pills-expert-${$(this).attr("id")}" ></a>`;
            modal.find(".comment-tabs div").html(tab);
        }
        let id = modal.find(".comment-tabs .nav-link.active").attr("id").replace("v-pills-expert-", "");
        $.ajax({
            method: 'GET',
            url: '/expert/get_resume',
            dataType: 'json',
            data: {id: id},
            success: function (data) {
                console.log(data);
                if (data.photo)
                    $("#expertResume #expert_photo").attr("src", data.photo);
                else
                    $("#expertResume #expert_photo").attr("src", "/static/expert/img/profile.jpg");
                $("#expert_name").html(data.name);
                $("#expert_uni").html(data.university);
                $("#expert_field").html(data.scientific_rank + " " + data.special_field);
                let sci_record = JSON.parse(data.sci_record);
                if (sci_record.length !== 0) {
                    let table_row = "";
                    for (let i = 0; i < sci_record.length; i++) {
                        table_row += "<tr>" +
                            "<td>" + sci_record[i].fields.degree + "</td>" +
                            "<td>" + sci_record[i].fields.major + "</td>" +
                            "<td>" + sci_record[i].fields.university + "</td>" +
                            "<td>" + sci_record[i].fields.city + "</td>" +
                            "<td>" + sci_record[i].fields.date_of_graduation + "</td>" +
                            "</tr>";
                        $('#expert_scientific_record').html(table_row);
                    }
                } else {
                    $('#expert_scientific_record').html(`<tr><td colspan="5">هیچ اطلاعاتی توسط کاربر ثبت نشده</td></tr>`);
                }
                let executive_record = JSON.parse(data.exe_record);
                if (executive_record.length !== 0) {
                    let table_row = "";
                    for (let i = 0; i < executive_record.length; i++) {
                        table_row += "<tr>" +
                            "<td>" + executive_record[i].fields.executive_post + "</td>" +
                            "<td>" + executive_record[i].fields.date_start_post + "</td>" +
                            "<td>" + executive_record[i].fields.date_end_post + "</td>" +
                            "<td>" + executive_record[i].fields.organization + "</td>" +
                            "<td>" + executive_record[i].fields.city + "</td>" +
                            "</tr>";
                        $('#expert-executive-info').html(table_row);
                    }
                } else {
                    $('#expert-executive-info').html(`<tr><td colspan="5">هیچ اطلاعاتی توسط کاربر ثبت نشده</td></tr>`);
                }
                let research_record = JSON.parse(data.research_record);
                console.log(research_record);
                if (research_record.length !== 0) {
                    let table_row = "";
                    for (let i = 0; i < research_record.length; i++) {
                        table_row += "<tr>" +
                            "<td>" + research_record[i].fields.research_title + "</td>" +
                            "<td>" + research_record[i].fields.researcher + "</td>" +
                            "<td>" + research_record[i].fields.co_researcher + "</td>" +
                            "</tr>";
                        $('#expert_research_record').html(table_row);
                    }
                } else {
                    $('#expert_research_record').html(`<tr><td colspan="5">هیچ اطلاعاتی توسط کاربر ثبت نشده</td></tr>`);
                }
                let paper_record = JSON.parse(data.paper_record);
                if (paper_record.length !== 0) {
                    let table_row = "";
                    for (let i = 0; i < paper_record.length; i++) {
                        table_row += "<tr>" +
                            "<td>" + paper_record[i].fields.research_title + "</td>" +
                            "<td>" + paper_record[i].fields.date_published + "</td>" +
                            "<td>" + paper_record[i].fields.published_at + "</td>" +
                            "<td>" + paper_record[i].fields.impact_factor + "</td>" +
                            "<td>" + paper_record[i].fields.citation + "</td>" +
                            "</tr>";
                        $('#expert_paper_record').html(table_row);
                    }
                } else {
                    $('#expert_paper_record').html(`<tr><td colspan="5">هیچ اطلاعاتی توسط کاربر ثبت نشده</td></tr>`);
                }
                if (data.researcher_count) {
                    $('.researcher_count').html(data.researcher_count);
                    modal.find('.researcher_count').closest("li").removeClass("d-none");
                }
                if (data.has_industrial_research) {
                    $('.has_industrial_research').html(data.has_industrial_research);
                    modal.find('.has_industrial_research').closest("li").removeClass("d-none");
                }
                if (data.awards) {
                    $('.awards').html(data.awards);
                    modal.find('.awards').closest("li").removeClass("d-none");
                }

                // if (data.languages === '') {
                //     $(".foreign-lang").closest("li").css("display", "none");
                // } else {
                //     $('.languages').html(data.languages);
                // }
                if (data.awards !== '' || data.researcher_count || data.has_industrial_research || data.languages) {
                    modal.find(".optional-part").removeClass("d-none");
                    modal.on("hidden.bs.modal", function () {
                        modal.find(".optional-part").addClass("d-none");
                        modal.find('.researcher_count').closest("li").addClass("d-none");
                        modal.find('.has_industrial_research').closest("li").addClass("d-none");
                        modal.find('.awards').closest("li").addClass("d-none");
                    });
                }

                getComments(id, modal.find("#project_id").val());
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
            "<span class='comment-tools'>"
        // "<i class='fas fa-pen'>" +
        // "</i>" +
        // "<i class='fas fa-reply'><div class='reply'></div>" +
        // "</i>"
        ;
        if (data[i].attachment !== "None") {
            comments_code += "<a href='" +
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
    console.log("comment ", data);
    // data = data.comment;
    let comments_code = "";
    for (let i = 0; i < data.length; i++) {
        if (data[i].sender_type === "industry") { //industry
            let comment_body_classes = "comment-body";
            if (data[i].attachment !== "None") {
                comment_body_classes += " attached";
            }
            comments_code += `
                <div class='my-comment'>
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
                        <pre>${data[i].text}</pre>
                        ${data[i].attachment !== "None" ?
                `<a href='${data[i].attachment}' class='attached-file'>
                                <i class='fas fa-paperclip'></i>
                                <span>${data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1)}</span>
                            </a>`
                :
                ""
            }
                    </div>
                </div>                                
            `;
        } else if (data[i].sender_type === "expert" || data[i].sender_type === "researcher") { //expert or researcher
            let comment_body_classes = "comment-body";
            if (data[i].attachment !== "None") {
                comment_body_classes += " attached";
            }
            comments_code += `
                <div class='your-comment'>
                    <div class='${comment_body_classes}' dir='ltr'>
                        <span class='comment-tools'></span>
                        <pre>${data[i].text}</pre>
                        ${data[i].attachment !== "None" ?
                `<a href='${data[i].attachment}' class='attached-file'>
                                <i class='fas fa-paperclip'></i>
                                <span>${data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1)}</span>
                            </a>`
                :
                ""
            }
                    </div>
                </div>
            `;
        } else { //system
            comments_code += `
                <div class='system-comment'>
                    <div class='comment-body' dir='ltr'>
                        <pre>${data[i].text}</pre>
                    </div>
                </div>
            `;
        }
    }
    $('.comments').html(comments_code).animate({scrollTop: $('.comments').prop("scrollHeight")}, 1000);
    $(".comments .fa-trash-alt").closest(".dropdown-item").click(function () {
        deleteComment($(this).closest('.my-comment'));
    });
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
            "top": "11px",
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
                "top": "11px",
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
        url: '/industry/get_comment/',
        dataType: 'json',
        data: {
            expert_id: expert_id,
            project_id: project_id
        },
        success: function (data) {
            if (data.accepted) {
                $(".accept-request").hide();
                $(".accept-request").prop('disabled', true);
                $(".reject-request").hide();
                $(".reject-request").prop('disabled', true);
                if (data.enforcer) {
                    $('.request').html("این پروژه به این استاد واگذار شده است.");
                    $('.add-comment').attr('style', "display : block");
                    $(".comment_submit").prop('disabled', false);
                } else {
                    $('.request').html("درخواست این استاد برای پروژه رد شده است.");
                    $('.add-comment').attr('style', "display : none");
                    $(".comment_submit").prop('disabled', true);
                }
            } else if (data.applied === false) {
                $('.request').html("برای مشاهده رزومه استاد بر روی دکمه روبه رو کلیک کنید.");
                $(".accept-request").hide();
                $(".accept-request").prop('disabled', true);
                $(".reject-request").hide();
                $(".reject-request").prop('disabled', true);
            } else {
                $('.request').html("درخواستی برای انجام پروژه شما از طرف این استاد دریافت شده است.");
                $('.request').show();
                $(".accept-request").show();
                $(".accept-request").prop('disabled', false);
                $(".reject-request").show();
                $(".reject-request").prop('disabled', false);
            }
            setComment(data.comment);
        },
        error: function (data) {

        },
    });
}

function addComment(data) {
    let comment_body_classes = "comment-body";
    if (data.attachment !== "None") {
        comment_body_classes += " attached";
    }
    let new_comment = "<div class='my-comment'>" +
        "<div class='comment-profile'></div>" +
        "<div class='" + comment_body_classes + "'>" +
        "       <span class='comment-tools'>" +
        "               <div class='btn-group dropright'>" +
        "                   <button type='button' class='dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
        "                       <i class='fas fa-cog'></i>" +
        "                   </button>" +
        "                   <div class='dropdown-menu'>" +
        // "                       <div class='dropdown-item'>" +
        // "                           <i class='fas fa-pen'></i>" +
        // "                           <span>ویرایش پیام</span>" +
        // "                       </div>" +
        "                       <div class='dropdown-item'>" +
        "                           <i class='fas fa-trash-alt'></i>" +
        "                           <span>حذف پیام</span>" +
        "                       </div>" +
        "                   </div>" +
        "               </div>" +
        // "               <i class='fas fa-reply'>" +
        // "                   <div class='reply'></div>" +
        // "               </i>" +
        "           </span>" +
        "<pre>" + data.description + "</pre>";
    if (data.attachment !== "None") {
        new_comment += "<a href='" + data.attachment + "' class='attached-file'>" +
            "   <i class='fas fa-paperclip'></i>" +
            "   <span>" + data.attachment.substring(data.attachment.lastIndexOf("/") + 1) + "</span>" +
            "</a>";
    }
    new_comment += "" +
        "   </div>" +
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
    return new_comment;
}

let requestForm = $("#researcher-request-ajax");
requestForm.submit(function (event) {
    console.log("------");
    event.preventDefault();
    let thisUrl = "/industry/request_researcher/";
    let form = new FormData(requestForm.get(0));
    $("#id_least_hour").removeClass("error").css("color", "").prev().css("color", "");
    $("#id_researcher_count").removeClass("error").css("color", "").prev().css("color", "");
    $('.error').remove();
    $.ajax({
        method: 'POST',
        url: thisUrl,
        data: form,
        processData: false,
        contentType: false,
        success: function (data) {
            iziToast.success({
                rtl: true,
                message: "درخواست شما با موفقیت ثبت شد!",
                position: 'bottomLeft'
            });
            // requestForm[0].reset();
            requestForm.closest(".modal").modal("hide");
        },
        error: function (data) {
            let obj = JSON.parse(data.responseText);
            if (obj.least_hour) {
                $("#id_least_hour").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.least_hour + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("#id_least_hour").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.researcher_count) {
                $("#id_researcher_count").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.researcher_count + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("#id_researcher_count").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            display_error(requestForm);
        },
    });
});

$(window).on("load", function () {
    init_windowSize();
    load_dialog();
    $('*').persiaNumber();
}).on("resize", function () {
    init_windowSize();
    load_dialog();
});

$(document).ready(function () {
    $('.content').scroll(function () {
        if ($(".content").scrollTop() > 300) {
            $("a.top-button").addClass('show');
        } else {
            $("a.top-button").removeClass('show');
        }
    });
    //****************************************//
    //  Task Bar
    //****************************************//
    let taskList = $(".ct-checklist");
    if (taskList.length) {
        taskList.find(".ct-checklist-item__checkbox input[type='checkbox']").click(function () {
            if ($(this).is(":checked")) {
                let text = $(this).closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text").html();
                $(this).closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text").html(`<del>${text}</del>`);
            } else {
                let text = $(this).closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text del").html();
                $(this).closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text").html(`${text}`);
            }
        });

        taskList.find(".ct-checklist-item__detail .ct-checklist__text").click(function () {
            if ($(this).find('pre[contenteditable="true"]').length === 0) {
                let text = $(this).html();
                let checklistItem = $(this).closest(".ct-checklist__item");
                checklistItem.addClass("onEdit");
                $(this).html(`<pre contenteditable="true">${text}</pre>`);
                let dropdown_list = $(".modal#addTask .ct-task-assignee .dropdown-menu").html();
                checklistItem.append(`
                    <div class="ct-checklist-item__footer">
                        <div class="float-left mt-1">
                            <div class="ct-task-option d-flex">
                                        <div class="ct-task-due ct-option-btn">
                                            <button id="edit_task_due" type="button" class=""
                                                    data-toggle="datetimepicker" style="padding: 6px 10px;" dir="ltr">
                                                <svg width="1em" height="1em"
                                                     viewBox="0 0 16 16" class="bi bi-clock"
                                                     fill="currentColor"
                                                     xmlns="http://www.w3.org/2000/svg">
                                                    <path fill-rule="evenodd"
                                                          d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm8-7A8 8 0 1 1 0 8a8 8 0 0 1 16 0z"></path>
                                                    <path fill-rule="evenodd"
                                                          d="M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z"></path>
                                                </svg>
                                            </button>
                                        </div>
                                        <div class="ct-task-assignee ct-option-btn">
                                            <div class="dropdown">
                                                <button class="btn btn-secondary dropdown-toggle ct-option-btn"
                                                        type="button" id="dropdownAssignment"
                                                        data-toggle="dropdown" aria-haspopup="true"
                                                        aria-expanded="false"  style="padding: 4px 9px;">
                                                    <svg width="1em" height="1em"
                                                         viewBox="0 0 16 16"
                                                         class="bi bi-person-plus"
                                                         fill="currentColor"
                                                         xmlns="http://www.w3.org/2000/svg">
                                                        <path fill-rule="evenodd"
                                                              d="M8 5a2 2 0 1 1-4 0 2 2 0 0 1 4 0zM6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm6 5c0 1-1 1-1 1H1s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C9.516 10.68 8.289 10 6 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10zM13.5 5a.5.5 0 0 1 .5.5V7h1.5a.5.5 0 0 1 0 1H14v1.5a.5.5 0 0 1-1 0V8h-1.5a.5.5 0 0 1 0-1H13V5.5a.5.5 0 0 1 .5-.5z"></path>
                                                    </svg>
                                                </button>
                                                <div class="dropdown-menu text-right"
                                                     aria-labelledby="dropdownAssignment">
                                                    ${dropdown_list}
                                                </div>
                                            </div>
                                        </div>
                                        <div class="ct-task-delete ct-option-btn d-none">
                                            <button>
                                                <svg width="1em" height="1em"
                                                     viewBox="0 0 16 16" class="bi bi-trash"
                                                     fill="currentColor"
                                                     xmlns="http://www.w3.org/2000/svg">
                                                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"></path>
                                                    <path fill-rule="evenodd"
                                                          d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"></path>
                                                </svg>
                                            </button>
                                        </div>
                                    </div>
                        </div>
                        <div class="">
                            <button class="save-change btn btn-primary btn-sm">ذخیره</button>
                            <button class="cancel-change btn btn-link text-dark btn-sm">
                                <svg width="2em" height="2em" viewBox="0 0 16 16" class="bi bi-x" fill="currentColor"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path fill-rule="evenodd" 
                                        d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z">
                                    </path>
                                </svg> 
                            </button>
                        </div>
                    </div>`);

                checklistItem.find(".ct-checklist-item__footer .ct-task-assignee.ct-option-btn .dropdown-item").click(function () {
                    let mentionVal = $(this).attr("data-value");
                    checklistItem.find(".ct-checklist-item__detail .ct-checklist__text pre").html(`<span class="atMention me" title="">@${mentionVal}</span>` + text);
                });

                $('#edit_task_due').pDatepicker({
                    format: 'YYYY/MM/DD',
                    onShow: function (unix) {
                        let datePicker = $(".datepicker-container");
                        if (datePicker.find(".datepicker-plot-area").height() + datePicker.offset().top > $(window).height()) {
                            if (datePicker.offset().top > 310) {
                                datePicker.css("top", datePicker.offset().top - 310);
                            } else {
                                datePicker.css("top", 0);
                            }
                        }
                    },
                    dayPicker: {
                        onSelect: function (unix) {
                            let pdate = new persianDate(unix);
                            $('#edit_task_due').append(pdate.format("YYYY/MM/DD"));
                        },
                    },
                });

                checklistItem.find(".ct-checklist-item__footer button.cancel-change").click(function () {
                    checklistItem.removeClass("onEdit");
                    checklistItem.find(".ct-checklist-item__detail .ct-checklist__text").html(text);
                    checklistItem.find(".ct-checklist-item__footer").remove();
                });

                checklistItem.find(".ct-checklist-item__footer button.save-change").click(function () {
                    checklistItem.removeClass("onEdit");
                    text = checklistItem.find(".ct-checklist-item__detail .ct-checklist__text pre").html();
                    checklistItem.find(".ct-checklist-item__detail .ct-checklist__text").html(text);
                    checklistItem.find(".ct-checklist-item__footer").remove();
                });
            }
        });

        taskList.find(".ct-checklist-item-delete").click(function () {
            $(this).closest(".ct-checklist__item").remove();
        });

        $('#id_task_due').pDatepicker({
            format: 'YYYY/MM/DD',
            onShow: function (unix) {
                let datePicker = $(".datepicker-container");
                if (datePicker.find(".datepicker-plot-area").height() + datePicker.offset().top > $(window).height()) {
                    if (datePicker.offset().top > 310) {
                        datePicker.css("top", datePicker.offset().top - 310);
                    } else {
                        datePicker.css("top", 0);
                    }
                }
            },
            dayPicker: {
                onSelect: function (unix) {
                    let pdate = new persianDate(unix);
                    $('#id_task_due').append(pdate.format("YYYY/MM/DD"));
                },
            },
        });

        let addTaskForm = $("form#add-task-ajax");
        addTaskForm.find(".ct-task-assignee.ct-option-btn .dropdown-item:not(.selected)").click(function () {
            let mentionVal = $(this).attr("data-value");
            $(this).addClass("selected");
            addTaskForm.find(".tagId-list").append(`<li class="tagId-item">
                                            <span>@${mentionVal}</span>
                                            <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-x"
                                                 fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                <path fill-rule="evenodd"
                                                      d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"></path>
                                            </svg>
                                        </li>`);
            let thisDropItem = $(this);
            addTaskForm.find(".tagId-list .tagId-item:last-child").click(function () {
                $(this).closest(".tagId-item").remove();
                thisDropItem.removeClass("selected");
            });
            // let title = addTaskForm.find("#id_task_title").html();
            // addTaskForm.find("#id_task_title").html(`<span class="atMention me" title="">@${mentionVal}</span>` + title);
        });
        addTaskForm.submit(function (event) {
            event.preventDefault();
            let title = addTaskForm.find("#id_task_title").html();
            let mentions = [];
            addTaskForm.find(".tagId-list .tagId-item").each(function () {
                mentions.push($(this).find("span").text());
                title = `<span class="atMention">${$(this).find("span").text()}</span> ` + title;
            });
            let pk = taskList.find(".ct-checklist__item").length + 1;

            let task = `<div class="ct-checklist__item d-flex">
                                                            <div class="ct-checklist-item__checkbox">
                                                                <div class="form-group form-check">
                                                                    <input type="checkbox"
                                                                           class="form-check-input inp-cbx"
                                                                           id="checkList#${pk}"
                                                                           name="requestResearcher" value=1 hidden>
                                                                    <label class="form-check-label cbx mb-0"
                                                                           for="checkList#${pk}">
                                                                        <span>
                                                                            <svg class="inline-svg bi bi-check2"
                                                                                 viewBox="0 0 16 16"
                                                                                 xmlns="http://www.w3.org/2000/svg">
                                                                                <path fill-rule="evenodd"
                                                                                      d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"></path>
                                                                            </svg>
                                                                        </span>
                                                                    </label>
                                                                </div>
                                                            </div>
                                                            <div class="ct-checklist-item__detail">
                                                                <div class="ct-checklist__text">${title}</div>
                                                                <div class="ct-checklist-item__control d-flex">
                                                                    <div class="ct-checklist-item-due">
                                                                        <button>
                                                                            <svg width="1em" height="1em"
                                                                                 viewBox="0 0 16 16" class="bi bi-clock"
                                                                                 fill="currentColor"
                                                                                 xmlns="http://www.w3.org/2000/svg">
                                                                                <path fill-rule="evenodd"
                                                                                      d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm8-7A8 8 0 1 1 0 8a8 8 0 0 1 16 0z"></path>
                                                                                <path fill-rule="evenodd"
                                                                                      d="M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z"></path>
                                                                            </svg>
                                                                        </button>
                                                                    </div>
                                                                    <div class="ct-checklist-item-assignee">
                                                                        <button>
                                                                            <svg width="1em" height="1em"
                                                                                 viewBox="0 0 16 16"
                                                                                 class="bi bi-person-plus"
                                                                                 fill="currentColor"
                                                                                 xmlns="http://www.w3.org/2000/svg">
                                                                                <path fill-rule="evenodd"
                                                                                      d="M8 5a2 2 0 1 1-4 0 2 2 0 0 1 4 0zM6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm6 5c0 1-1 1-1 1H1s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C9.516 10.68 8.289 10 6 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10zM13.5 5a.5.5 0 0 1 .5.5V7h1.5a.5.5 0 0 1 0 1H14v1.5a.5.5 0 0 1-1 0V8h-1.5a.5.5 0 0 1 0-1H13V5.5a.5.5 0 0 1 .5-.5z"></path>
                                                                            </svg>
                                                                        </button>
                                                                    </div>
                                                                    <div class="ct-checklist-item-delete">
                                                                        <button>
                                                                            <svg width="1em" height="1em"
                                                                                 viewBox="0 0 16 16" class="bi bi-trash"
                                                                                 fill="currentColor"
                                                                                 xmlns="http://www.w3.org/2000/svg">
                                                                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"></path>
                                                                                <path fill-rule="evenodd"
                                                                                      d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"></path>
                                                                            </svg>
                                                                        </button>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>`;
            taskList.append(task);

            taskList.find(".ct-checklist__item:last-child .ct-checklist-item__checkbox input[type='checkbox']").click(function () {
                if ($(this).is(":checked")) {
                    let text = $(this).closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text").html();
                    $(this).closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text").html(`<del>${text}</del>`);
                } else {
                    let text = $(this).closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text del").html();
                    $(this).closest(".ct-checklist__item").find(".ct-checklist-item__detail .ct-checklist__text").html(`${text}`);
                }
            });

            taskList.find(".ct-checklist__item:last-child .ct-checklist-item-delete").click(function () {
                $(this).closest(".ct-checklist__item").remove();
            });
            addTaskForm.find("#id_task_title").html("");
            addTaskForm.find(".tagId-list").html("");
            addTaskForm.find(".ct-task-assignee.ct-option-btn .dropdown-item.selected").removeClass("selected");

            $("#addTask").modal("hide");
        });
    }
    //****************************************//
    //  End Task Bar
    //****************************************//

    //****************************************//
    //  New Project
    //****************************************//
    if (window.location.href.indexOf("/industry/newProject/") !== -1) {
        $("input#id_required_budget").on("keyup", function () {
            $(this).attr();
        });

        $(".container form").submit(function () {
            $(this).find("[type='submit']").prop("disabled", true);
        });
    }
    //****************************************//
    //  End New Project
    //****************************************//

    //****************************************//
    //  Deadline Progress
    //****************************************//
    let addDeadlineForm = $("form#add-card-ajax");
    if (addDeadlineForm.length) {
        addDeadlineForm.submit(function (event) {
            event.preventDefault();
            let title = addDeadlineForm.find("#id_card_title").val();
            let due = addDeadlineForm.find("#id_card_deadline").val();
            $.ajax({
                method: "POST",
                url: "/addCard/",
                data: addDeadlineForm.serialize(),
                success: function (data) {
                    console.log(data);
                    let progressItem = `<div class="step-container">
                                    <span class="step-date">
                                        <div>${due}</div>
                                    </span>
                                    <span class="step-name">${title}</span>
                                </div>`;
                    $(progressItem).insertBefore('.project-progress .line-100');
                    $("#addDeadline").modal("hide");
                    iziToast.success({
                        rtl: true,
                        message: "آیتم با موفقیت اضافه شد!",
                        position: 'bottomLeft'
                    });
                },
                error: function (data) {
                    console.log(data);
                    iziToast.error({
                        rtl: true,
                        message: "درخواست شما با مشکل مواجه شد!\nلطفا دوباره تکرار کنید.",
                        position: 'bottomLeft'
                    });
                }
            });
        });
    }

    let deadLineProgress = $(".project-progress.project-progress-sm");
    if (deadLineProgress.length) {
        if ($(window).width() < 992) {
            let deadLineProgressOverFlow = deadLineProgress.closest(".overflow-auto");
            if (deadLineProgressOverFlow.find(".project-progress").offset().left <= deadLineProgressOverFlow.offset().left - 50) {
                deadLineProgressOverFlow.prev(".scroll-left").removeClass("d-none");
            }
            deadLineProgressOverFlow.scroll(function () {
                if ($(this).find(".project-progress").offset().left > $(this).offset().left - 50) {
                    $(this).prev(".scroll-left").addClass("d-none");
                } else {
                    $(this).prev(".scroll-left").removeClass("d-none");
                }

                let rightPos = $(this).find(".project-progress").offset().left + $(this).find(".project-progress").outerWidth();
                let fixRightPos = $(this).offset().left + $(this).outerWidth();
                if (rightPos - fixRightPos < 50) {
                    $(this).next(".scroll-right").addClass("d-none");
                } else {
                    $(this).next(".scroll-right").removeClass("d-none");
                }
            });
            // TODO: left and right animation not working properly
            let w_diff = deadLineProgress.outerWidth() - deadLineProgressOverFlow.outerWidth();
            deadLineProgressOverFlow.prev(".scroll-left").click(function () {
                console.log("pre left ", $(this).next(".overflow-auto").find(".project-progress").offset().left);
                $(this).next(".overflow-auto").animate({scrollLeft: $(this).next(".overflow-auto").find(".project-progress").offset().left - 50}, 300);
                console.log("left ", $(this).next(".overflow-auto").find(".project-progress").offset().left);
            });
            deadLineProgressOverFlow.next(".scroll-right").click(function () {
                let leftLoc = $(this).prev(".overflow-auto").find(".project-progress").offset().left + 50 - w_diff;
                console.log("pre right * ", $(this).prev(".overflow-auto").find(".project-progress").offset().left);
                console.log("pre right ", leftLoc);
                $(this).prev(".overflow-auto").animate({scrollLeft: leftLoc}, 300);
                console.log("right ", $(this).prev(".overflow-auto").find(".project-progress").offset().left);
            });
        }
    }
    //****************************************//
    //  End Deadline Progress
    //****************************************//

    function selecting_expert(element) {
        element.on("keyup", function () {
            const thisElement = $(this);
            $.ajax({
                method: "POST",
                url: "/industry/search_user_id",
                data: {"searchKey": thisElement.val()},
                success: function (data) {
                    console.log(data);
                    let availableTags = [];
                    for (let i = 0; i < data.experts.length; i++) {
                        // console.log("fullname: ", data.experts[i].fullname)
                        let fullname = data.experts[i].fullname;
                        availableTags.push(
                            {
                                "value": fullname,
                                "userId": data.experts[i].userId,
                                "photo": data.experts[i].photo,
                                "id": data.experts[i].id,
                                "autoAdd": data.experts[i].autoAdd,
                                "label": `
                                    <span><div>${data.experts[i].fullname}</div><div>${data.experts[i].userId}</div></span>
                                    <img src='${data.experts[i].photo}' alt='expert photo' width='70px' height="55px">
                                `
                            }
                        );
                    }
                    thisElement.autocomplete({
                        source: availableTags,
                        minWidth: 1,
                        open: function (event, ui) {
                            thisElement.addClass("remove-border-bottom");
                            console.log("open");
                        },
                        close: function (event, ui) {
                            thisElement.removeClass("remove-border-bottom");
                            console.log("close");
                        },
                        select: function (event, ui) {
                            let itemStatus = `<div class="selected-expert__status text-warning">
                                                    در انتظار تایید
                                                </div>`;
                            if (ui.item.autoAdd) {
                                itemStatus = `<div class="selected-expert__status text-success">
                                                    تایید شده
                                                </div>`
                            }
                            let expert = `<div class="selected-expert mb-2" id="${ui.item.id}">
                                                <img src="${ui.item.photo}" alt="${ui.item.value}" width="60px" height="60px">
                                                <div class="selected-expert__details text-right">
                                                    <div>${ui.item.value}</div>
                                                    <div dir="ltr">${ui.item.userId}</div>
                                                </div>
                                                ${itemStatus}
                                                <button type="button" class="selected-expert__delete-item">
                                                    <i class="fas fa-times"></i>
                                                </button>
                                            </div>`;
                            thisElement.closest(".form-group").closest("div.col-md-10").append(expert);
                            thisElement.val("");
                            $(".selected-expert:last-child .selected-expert__delete-item").click(function () {
                                $(this).closest(".selected-expert").remove();
                            });
                        }
                    }).data("ui-autocomplete")._renderItem = function (ul, item) {
                        return $("<li class='ui-autocomplete-row'></li>")
                            .data("item.autocomplete", item)
                            .append(item.label)
                            .appendTo(ul);
                    };
                    $(".ui-menu.ui-widget.ui-widget-content.ui-autocomplete.ui-front").addClass("item-has-img");
                },
                error: function (data) {
                    console.log(data);
                }
            });
        });
    }

    selecting_expert($("#searchExpert"));


    $('.accept-request').click(function (data) {
        let expert_id = $(".comment-tabs .active").attr("id").replace("v-pills-expert-", "");
        let project_id = $(this).closest(".confirm-request").attr("id");
        let thisElement = $(this);
        data = {
            "expert_id": expert_id,
            "project_id": project_id
        };
        $.ajax({
            method: 'post',
            url: 'accept_request/',
            dataType: 'json',
            data: data,
            success: function (data) {
                iziToast.success({
                    rtl: true,
                    message: "درخواست شما با موفقیت ارسال شد!",
                    position: 'bottomLeft'
                });
                thisElement.hide();
                thisElement.prop('disabled', true);
                thisElement.closest(".button-group").find(".accept-request").hide();
                thisElement.closest(".button-group").find(".accept-request").prop('disabled', true);
                thisElement.closest(".confirm-request").find('.request').html("این پروژه به این استاد واگذار شده است.");
            },
            error: function (data) {
                iziToast.error({
                    rtl: true,
                    message: "درخواست شما با خطا روبه رو شد!",
                    position: 'bottomLeft'
                });
            },
        });
    });

    $('.reject-request').click(function (data) {
        let expert_id = $(".comment-tabs .active").attr("id").replace("v-pills-expert-", "");
        let project_id = $(this).closest(".confirm-request").attr("id");
        let thisElement = $(this);
        data = {
            "expert_id": expert_id,
            "project_id": project_id
        };
        $.ajax({
            method: 'POST',
            url: 'refuse_request/',
            dataType: 'json',
            data: data,
            success: function (data) {
                iziToast.success({
                    rtl: true,
                    message: "درخواست شما با موفقیت ارسال شد!",
                    position: 'bottomLeft'
                });
                thisElement.hide();
                thisElement.prop('disabled', true);
                thisElement.closest(".button-group").find(".accept-request").hide();
                thisElement.closest(".button-group").find(".accept-request").prop('disabled', true);
                thisElement.closest(".confirm-request").find('.request').html("درخواست این استاد برای پروژه رد شده است.");
            },
            error: function (data) {
                iziToast.error({
                    rtl: true,
                    message: "درخواست شما با خطا روبه رو شد!",
                    position: 'bottomLeft'
                });
            },
        });
    });

    // Check user id
    if ($("#userID").length) {
        $("input#userID").on("keyup", function () {
            console.log("search: ", $(this).val());
            let thisFormGroup = $(this).closest(".form-group");
            if ($(this).val()) {
                thisFormGroup.find(".form-group__status").removeClass("check").removeClass("success")
                    .removeClass("fail");
                thisFormGroup.find(".form-group__status").addClass("check");
                thisFormGroup.find("input").removeClass("error").css("color", "").prev().css("color", "");
                $("#userID").closest("div").find(".error").remove();
                $.ajax({
                    method: "POST",
                    url: "/checkUserId",
                    data: {"user_id": $(this).val()},
                    success: function (data) {
                        console.log(data);
                        thisFormGroup.find(".form-group__status").removeClass("check");
                        if (data.invalid_input) {
                            $("#userID").closest("div").append("<div class='error userId'>" +
                                "<span class='error-body'>" +
                                "<ul class='errorlist'>" +
                                "<li>" + data.message + "</li>" +
                                "</ul>" +
                                "</span>" +
                                "</div>");
                            thisFormGroup.find(".form-group__status").addClass("fail");
                            thisFormGroup.find("input").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                        } else if (data.is_unique) {
                            thisFormGroup.find(".form-group__status").addClass("success");
                        } else {
                            $("#userID").closest("div").append("<div class='error userId'>" +
                                "<span class='error-body'>" +
                                "<ul class='errorlist'>" +
                                "<li>" + data.message + "</li>" +
                                "</ul>" +
                                "</span>" +
                                "</div>");
                            thisFormGroup.find(".form-group__status").addClass("fail");
                            thisFormGroup.find("input").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
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

    function setDates(date) {
        $(".project-details .project-progress .start").html(date[0]);
        $(".project-details .project-progress .first_phase").html(date[1]);
        $(".project-details .project-progress .second_phase").html(date[2]);
        $(".project-details .project-progress .third_phase").html(date[3]);
        $(".project-details .project-progress .date_finished").html(date[4]);
    }

    function projectDetail(data) {
        if (data.vote)
            $(".vote").attr('style', "display: block;");
        else
            $(".vote").attr('style', "display: none;");
        let projectDetails = $(".project-details");
        projectDetails.find(".card-head").html(data.persian_title + "<br>" + ' ( ' + data.english_title + ' )');
        projectDetails.find(".establish-time .time-body").html(data.date);
        projectDetails.find(".time-left .time-body").html(data.deadline);

        let techniques = "";
        for (let tech_index = 0; tech_index < data.techniques.length; tech_index++) {
            let element = data.techniques[tech_index];
            techniques += "<span class='border-span'>" +
                element +
                "</span>";
        }
        $(".techniques").html(techniques);

        $("#industry-name").html(data.industry_name);
        $("#enforcer-name").html(data.enforcer_name).attr("value", data.enforcer_id);
        $("#executive-info").html(data.executive_info);
        $("#industry_logo").attr("src", data.industry_logo);
        $(".budget-amount").html(data.budget_amount);
        setDates(data.timeScheduling);
        setProblemStatement(data, "-detail");
        setValue(data, "-detail");
        setTab(data);
        // modalPreview(".project-details");
    }

    $(".preview-project").click(function () {
        const dialog = $("#showProject");
        $(this).closest(".card").find('.unseen-comments').html("");
        let id = $(this).attr("id");
        $.ajax({
            method: 'GET',
            url: '/industry/show_project/',
            dataType: 'json',
            data: {id: id},
            success: function (data) {
                if (data.accepted) {
                    projectDetail(data);
                } else {
                    $('.confirm-request').attr('id', id);
                    $('.add-comment').attr('id', id);
                    localStorage.setItem("project_id", "" + id);
                    localStorage.setItem("replied_text", null);
                    dialog.find(".modal-header .modal-title").html(data.persian_title + "<br>" + data.english_title);
                    dialog.find(".establish-time .time-body").html(data.submission_date);
                    dialog.find(".time-left .time-body").html(data.deadline);
                    for (let i = 0; i < data.key_words.length; i++) {
                        dialog.find(".techniques").append(
                            "<span class='border-span'>" +
                            data.key_words[i]
                            + "</span>"
                        );
                    }
                    setProblemStatement(data, "-preview");
                    setValue(data, "-preview");
                    if (data.status !== 1 && data.status !== 2) {
                        dialog.find('.add-comment').attr('style', 'display : none');
                        $('.image-btn-circle').prop('disabled', true);
                        $(".row.add-comment").css("display", "none");
                        dialog.find(".card").addClass("b-x0");
                        if (dialog.find(".container .message.info.image-right").length === 0) {
                            let info_msg = "<div class='message info image-right'>" +
                                "<img src='../../../../static/img/blue_warning.svg' alt=''>" +
                                "<h5>توجه</h5>" +
                                "<p>پروژه شما در حال بررسی توسط کارشناسان ما می‌باشد تا در صورت نیاز به اصلاح، با شما تماس گرفته شود.</p>" +
                                "<p>این فرایند،‌تا دقایقی دیگر  زمان خواهد برد.<p>" +
                                "<p>با تشکر از صبر و بردباری شما</p>" +
                                "</div>";
                            dialog.find(".container").append(info_msg);
                        }
                    } else {
                        if (data.vote)
                            $('.vote').attr('style', "display : block;");
                        else
                            $('.vote').attr('style', "display : none;");

                        $('.add-comment').attr('style', "display : block");
                        $('.image-btn-circle').prop('disabled', false);
                        setTab(data);
                        console.log(data);
                        dialog_comment_init();
                        // if (data.status === 1) {
                        //     $(".row.add-comment").css("display", "none");
                        // }
                    }
                    // modalPreview(".showProject");
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
    init_setup();
    search_input(".search_message");
    input_focus();
    if ($(window).width() < 767) {
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
        // init_dialog_btn(".preview-project", ".project-details");
        init_dialog_btn(".message-body button, .message-body-sm button", ".message-show");
        // init_dialog_btn(".show-resume", ".expert-resume");
        expertResume();
        // if($(".mainInfo-body").css("display") === "block"){
        //     blur_div_toggle(".top-bar");
        //     blur_div_toggle(".side-bar");
        // }
        // $(".form-submit").click(function () {
        //     blur_div_toggle(".top-bar");
        //     blur_div_toggle(".side-bar");
        //     $(".mainInfo-body").css("display", "none");
        // });
        $("i.fa-plus").click(function () {
            if ($("input#Uni").val() !== '') {
                let div = document.createElement("div");
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
            let div = document.createElement("div");
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
            let div = document.createElement("div");
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
            let div = document.createElement("div");
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
            let div = document.createElement("div");
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

    //# Project Setting Technique Selection

    // initial utils for Project Setting Modal
    if ($('#projectSetting').length) {

        let fileInput = $(".file-upload-min").closest(".form-group").find("input");
        fileInput.on("change", function () {
            let fileName = $(this).val().split("\\").pop();
            let label = $(this).closest(".form-group").find(".file-upload-min");
            if ($(this).val() !== "") {
                label.find(".file-upload-min-value").text(fileName);
            } else {
                label.find(".file-upload-min-value").text("برای بارگذاری فایل کلیک کنید!");
            }
        })

        // initial selected techniques tagInput
        $('#projectSetting #tags').tagsInput({
            'height': '100%',
            'width': '100%',
            'defaultText': '',
            'onAddTag': newItem_label,
            'onRemoveTag': newItem_label
        });
        $("#projectSetting #tags_tagsinput #tags_addTag").css("display", "none");
        $('#projectSetting #tags_tagsinput').addClass("border-0 mt-0");
        // add technique that write in input on Enter press
        $("#add-new-technique").keyup(function (e) {
            if (e.keyCode === 13) {
                if ($(this).val() !== "") {
                    $('#tags').addTag($(this).val());
                    $(this).val("");
                }
            }
        });

        let projectSettingForm = $('#ajax-project-setting');
        //## get techniques list via ajax request
        $("[data-target='#projectSetting']").click(function () {
            let pk = $(this).closest(".card").find("button.default-btn").attr("id");
            $(".modal#projectSetting").find("form#ajax-project-setting").attr("id", pk);
            let projectSetting = $("#projectSetting");
            projectSetting.find(".selected-expert").remove();
            projectSetting.find("#tags_tagsinput .tag").remove();
            $.ajax({
                method: 'GET',
                url: projectSettingForm.attr("action"),
                dataType: 'json',
                data: {'id': pk},
                success: function (data) {
                    console.log(data);
                    console.log(data.requestResearcher);
                    if (data.requestResearcher) {
                        $("#researcherAccess").attr("value", 1);
                        projectSettingForm.find("#ApplicationDeadline").closest(".form-group").removeClass("d-none");
                        $("#ApplicationDeadline").attr('value', data.researcherRequestDeadline);
                    } else {
                        // $("#researcherAccess").click();
                        $("#researcherAccess").attr("value", "");
                        projectSettingForm.find("#ApplicationDeadline").closest(".form-group").addClass("d-none");
                    }
                    if (data.end_note_fileName)
                        $(".end-note-file-name").text(data.end_note_fileName);
                    if (data.proposal_filaName)
                        $(".proposal-file-name").text(data.proposal_filaName);

                    let source = [];
                    for (let i = 0; i <= Object.keys(data.techniques).length - 1; i++) {
                        let item = {};
                        item["title"] = Object.keys(data.techniques)[i];
                        item["key"] = i + 1;
                        if (Object.values(data.techniques)[i].length) {
                            item["folder"] = true;
                            let children = [];
                            for (let j = 0; j < Object.values(data.techniques)[i].length; j++) {
                                let child_item = {};
                                child_item["title"] = Object.values(data.techniques)[i][j];
                                child_item["key"] = i + "." + j;
                                children.push(child_item);
                            }
                            item["children"] = children;
                        }
                        source.push(item);
                    }

                    // initialize fancy tree
                    function _svg(className, addClass) {
                        let html = '';
                        switch (className) {
                            case "folder":
                                html = '<svg class="bi bi-folder" width="20px" height="20px" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\n' +
                                    '  <path d="M9.828 4a3 3 0 01-2.12-.879l-.83-.828A1 1 0 006.173 2H2.5a1 1 0 00-1 .981L1.546 4h-1L.5 3a2 2 0 012-2h3.672a2 2 0 011.414.586l.828.828A2 2 0 009.828 3v1z"/>\n' +
                                    '  <path fill-rule="evenodd" d="M13.81 4H2.19a1 1 0 00-.996 1.09l.637 7a1 1 0 00.995.91h10.348a1 1 0 00.995-.91l.637-7A1 1 0 0013.81 4zM2.19 3A2 2 0 00.198 5.181l.637 7A2 2 0 002.826 14h10.348a2 2 0 001.991-1.819l.637-7A2 2 0 0013.81 3H2.19z" clip-rule="evenodd"/>\n' +
                                    '</svg>';
                                break;
                            case "folderOpen":
                                html = '<svg class="bi bi-folder-minus" width="20px" height="20px" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\n' +
                                    '  <path fill-rule="evenodd" d="M9.828 4H2.19a1 1 0 00-.996 1.09l.637 7a1 1 0 00.995.91H9v1H2.826a2 2 0 01-1.991-1.819l-.637-7a1.99 1.99 0 01.342-1.31L.5 3a2 2 0 012-2h3.672a2 2 0 011.414.586l.828.828A2 2 0 009.828 3h3.982a2 2 0 011.992 2.181L15.546 8H14.54l.265-2.91A1 1 0 0013.81 4H9.828zm-2.95-1.707L7.587 3H2.19c-.24 0-.47.042-.684.12L1.5 2.98a1 1 0 011-.98h3.672a1 1 0 01.707.293z" clip-rule="evenodd"/>\n' +
                                    '  <path fill-rule="evenodd" d="M11 11.5a.5.5 0 01.5-.5h4a.5.5 0 010 1h-4a.5.5 0 01-.5-.5z" clip-rule="evenodd"/>\n' +
                                    '</svg>';
                                break;
                            case "checkbox":
                                html = '<svg class="bi bi-square" width="16px" height="16px" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\n' +
                                    '  <path fill-rule="evenodd" d="M14 1H2a1 1 0 00-1 1v12a1 1 0 001 1h12a1 1 0 001-1V2a1 1 0 00-1-1zM2 0a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V2a2 2 0 00-2-2H2z" clip-rule="evenodd"/>\n' +
                                    '</svg>';
                                break;
                            case "checkboxSelected":
                                html = '<svg class="bi bi-check-square" width="16px" height="16px" viewBox="0 0 16 16" fill="#3ccd1c" xmlns="http://www.w3.org/2000/svg">\n' +
                                    '  <path fill-rule="evenodd" d="M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>\n' +
                                    '  <path fill-rule="evenodd" d="M10.97 4.97a.75.75 0 0 1 1.071 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.236.236 0 0 1 .02-.022z"/>\n' +
                                    '</svg>';
                                break;
                            case "checkboxUnknown":
                                html = '<svg class="bi bi-dash-square" width="20px" height="20px" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\n' +
                                    '  <path fill-rule="evenodd" d="M14 1H2a1 1 0 00-1 1v12a1 1 0 001 1h12a1 1 0 001-1V2a1 1 0 00-1-1zM2 0a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V2a2 2 0 00-2-2H2z" clip-rule="evenodd"/>\n' +
                                    '  <path fill-rule="evenodd" d="M3.5 8a.5.5 0 01.5-.5h8a.5.5 0 010 1H4a.5.5 0 01-.5-.5z" clip-rule="evenodd"/>\n' +
                                    '</svg>';
                                break;
                            case "expanderClosed":
                                html = '<svg class="bi bi-chevron-left" width="16px" height="16px" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\n' +
                                    '  <path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 010 .708L5.707 8l5.647 5.646a.5.5 0 01-.708.708l-6-6a.5.5 0 010-.708l6-6a.5.5 0 01.708 0z" clip-rule="evenodd"/>\n' +
                                    '</svg>';
                                break;
                            case "expanderOpen":
                                html = '<svg class="bi bi-chevron-down" width="16px" height="16px" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\n' +
                                    '  <path fill-rule="evenodd" d="M1.646 4.646a.5.5 0 01.708 0L8 10.293l5.646-5.647a.5.5 0 01.708.708l-6 6a.5.5 0 01-.708 0l-6-6a.5.5 0 010-.708z" clip-rule="evenodd"/>\n' +
                                    '</svg>';
                                break;
                            case "empty":
                                break

                        }
                        return {html: html};
                    }

                    projectSetting.find("#fancy-tree").off();
                    projectSetting.find("#fancy-tree").fancytree({
                        extensions: ["glyph"],
                        checkbox: true,
                        selectMode: 2,
                        checkboxAutoHide: true,
                        clickFolderMode: 2,
                        icon: false,
                        lazyLoad: function (event, data) {
                            // data.result = {url: "https://cdn.rawgit.com/mar10/fancytree/72e03685/demo/ajax-sub2.json"};
                        },
                        activate: function (event, data) {

                        },
                        select: function (event, data) {
                            if (data.node.isSelected()) {
                                if (!data.node.isFolder()) {
                                    if ($('#tags_tagsinput').find(".tag span:contains(" + data.node.title + ")").length === 0) {
                                        $('#tags').addTag(data.node.title);
                                    }
                                }
                            } else {
                                $('#tags').removeTag(data.node.title);
                            }
                        },
                        source: source,
                        glyph: {
                            preset: "awesome5",
                            map: {
                                checkbox: _svg("checkbox"),
                                checkboxSelected: _svg("checkboxSelected"),
                                checkboxUnknown: _svg("checkboxUnknown"),
                                expanderClosed: "fas fa-chevron-left",
                                expanderLazy: "fas fa-angle-right",
                                expanderOpen: "fas fa-chevron-down",
                                doc: _svg("empty"),
                                folder: _svg("folder"),
                                folderOpen: _svg("folderOpen")
                            }
                        },
                    });
                    // select_technique("#projectSetting");

                    // show experts
                    for (let i = 0; i < data.acceptedExpert.length; i++) {
                        let expert = `<div class="selected-expert mb-2" id="${data.acceptedExpert[i].id}">
                                                <img src="${data.acceptedExpert[i].photo}" 
                                                    alt="${data.acceptedExpert[i].fullname}" width="60px" height="60px">
                                                <div class="selected-expert__details text-right">
                                                    <div>${data.acceptedExpert[i].fullname}</div>
                                                    <div dir="ltr">${data.acceptedExpert[i].userId}</div>
                                                </div>
                                                <div class="selected-expert__status text-success ml-3">
                                                    تایید شده
                                                </div>
                                            </div>`;
                        projectSettingForm.find("#searchExpert").closest(".form-group").closest("div.col-md-10").append(expert);
                    }
                    for (let i = 0; i < data.suggestedExpert.length; i++) {
                        let expert = `<div class="selected-expert mb-2" id="${data.suggestedExpert[i].id}">
                                                <img src="${data.suggestedExpert[i].photo}" 
                                                    alt="${data.suggestedExpert[i].fullname}" width="60px" height="60px">
                                                <div class="selected-expert__details text-right">
                                                    <div>${data.suggestedExpert[i].fullname}</div>
                                                    <div dir="ltr">${data.suggestedExpert[i].userId}</div>
                                                </div>
                                                <div class="selected-expert__status text-warning ml-3">
                                                    در انتظار تایید
                                                </div>
                                            </div>`;
                        projectSettingForm.find("#searchExpert").closest(".form-group").closest("div.col-md-10").append(expert);
                    }
                    // preview projectTechniques
                    for (let i = 0; i < data.projectTechniques.length; i++) {
                        $('#tags').addTag(data.projectTechniques[i]);
                        let tree = $("#fancy-tree").fancytree("getTree");
                        let node = tree.findFirst(data.projectTechniques[i]);
                        if (node) {
                            node.setSelected();
                            node.getParent().setExpanded();
                        }
                    }
                },
            });
            // change default border and focus event of this tagInput
            projectSetting.find("#tags #tags_tagsinput").css("border", "none")
                .find("#tags_tag").on("focus", function () {
                $(this).css("width", "fit-content");
            });
            tag_input_label("tags");

        });

        //## show date picker on check
        projectSettingForm.find("#researcherAccess").on("change", function () {
            if ($(this).is(":checked")) {
                projectSettingForm.find("#ApplicationDeadline").closest(".form-group").removeClass("d-none");
                $("#researcherAccess").attr("value", 1);
            } else {
                projectSettingForm.find("#ApplicationDeadline").closest(".form-group").addClass("d-none");
                $("#researcherAccess").attr("value", 0);
            }
        });

        //## ignore submit form on press Enter key
        projectSettingForm.on('keyup keypress', function (e) {
            let keyCode = e.keyCode || e.which;
            if (keyCode === 13) {
                e.preventDefault();
                return false;
            }
        });

        //## submitting project setting form
        projectSettingForm.submit(function (event) {
            event.preventDefault();
            let data = new FormData(projectSettingForm.get(0));
            // let techs = [];
            let id = $(this).attr("id");
            // let expertIds = [];
            let applicationDeadline = $("#ApplicationDeadline").val();
            $.each(projectSettingForm.find(".selected-expert"), function () {
                data.append("expert_ids", $(this).attr("id"));
            });
            $.each($("#tags_tagsinput").find(".tag"), function (index, value) {
                data.append("technique", $(this).find("span").text());
                // techs[index] = $(this).find("span").text();
            });

            let telegram_group = projectSettingForm.find("#telegramGroupLink").val();
            data.set('id', id);
            data.set('telegram_group', telegram_group);
            data.set('researcherRequestDeadline', applicationDeadline);
            if ($("#researcherAccess").val() == 1)
                data.set('requestResearcher', true);
            $("#ApplicationDeadline").removeClass("error").css("color", "").prev().css("color", "");
            $("#ApplicationDeadline").closest("div").find(".error").remove();
            $.ajax({
                traditional: true,
                method: 'POST',
                url: $(this).attr('action'),
                data: data,
                processData: false,
                contentType: false,
                success: function (data) {
                    iziToast.success({
                        rtl: true,
                        message: data.message,
                        position: 'bottomLeft',
                    });
                    $('#projectSetting').modal('hide');
                    setTimeout(location.reload.bind(location), 1500);
                },
                error: function (data) {
                    let obj = JSON.parse(data.responseText);
                    let message = "";
                    if (obj.message !== undefined)
                        message = obj.message;
                    else
                        message = "اجرای این عملیات با خطا مواجه شد!";
                    iziToast.error({
                        rtl: true,
                        message: message,
                        position: 'bottomLeft'
                    });
                    if (obj.researcherRequestDeadline) {
                        $("#ApplicationDeadline").closest("div").append("<div class='error'>" +
                            "<span class='error-body'>" +
                            "<ul class='errorlist'>" +
                            "<li>" + obj.researcherRequestDeadline + "</li>" +
                            "</ul>" +
                            "</span>" +
                            "</div>");
                        $("#ApplicationDeadline").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                    }
                }
            });
        });
    }

    //End Project Setting Technique Selection
    function returnFileType(type) {
        type = type.toLowerCase();
        if (type === "pdf" || type === "doc" || type === "gif" || type === "jpg" || type === "png"
            || type === "ppt" || type === "txt" || type === "wmv" || type === "zip") {
            return type;
        } else if (type === "jpeg")
            return "jpg";
        return "unknown";
    }

    $("button[data-target='#researcherInfo']").click(function () {
        let modal = $("#researcherInfo");
        let id = $(this).attr("id");
        let url = $(this).attr("data-url");
        let project_id = $(this).attr("value");
        $.ajax({
            method: 'GET',
            url: url,
            dataType: 'json',
            data: {id: id, project_id: project_id},
            success: function (data) {
                // if (data.status === "justComment") {
                //     $(".confirm-researcher").prop('disabled', true);
                //     $(".refuse-researcher").prop('disabled', true);
                //     $(".delete-researcher").prop('disabled', true);
                if (data.status === "pending") {
                    $('.request-response').removeClass("d-none");
                    $(".confirm-researcher").attr('value', id);
                    $(".refuse-researcher").attr('value', id);
                } else if (data.status === "accepted") {
                    $('.remove-researcher').removeClass("d-none");
                    $(".delete-researcher").attr('value', id);
                }
                $("#researcherInfo").find(".add-comment").attr("id", project_id);
                modal.find(".researcher_id").attr("value", id);
                $(".project_id").attr("value", project_id);
                if (data.photo)
                    $('#researcher_photo').attr("src", data.photo);
                else
                    $('#researcher_photo').attr("src", "/static/expert/img/profile.jpg");
                $('#researcher_name').html(data.name);
                $('#researcher_major').html(data.major);
                switch (data.grade) {
                    case 1:
                        $('#researcher_grade').html('کارشناسی');
                        break;
                    case 2:
                        $('#researcher_grade').html('کارشناسی ارشد');
                        break;
                    case 3:
                        $('#researcher_grade').html('دکتری');
                        break;
                    case 4:
                        $('#researcher_grade').html('دکتری عمومی');
                        break;
                }
                let tech = "";
                for (let index = 0; index < data.techniques.length; index++)
                    tech += `<div class="technique-item">
                                <span class="technique-name">${data.techniques[index].name}</span>
                                <span class="grade grade__${data.techniques[index].level}"></span>
                             </div>`;
                // tech += "<span class='border-span'>" + data.techniques[index] + "</span>";
                $("#technique-list").html(tech);
                $('#researcher_university').html(data.university);
                $('#researcher_entry_year').html(data.entry_year);

                let scientific_record = JSON.parse(data.scientific_record);
                if (scientific_record.length !== 0) {
                    let table_row = "";
                    for (let i = 0; i < scientific_record.length; i++) {
                        table_row = table_row + "<tr>" +
                            "<td>" + scientific_record[i].fields.major + "</td>" +
                            "<td>" + scientific_record[i].fields.grade + "</td>" +
                            "<td>" + scientific_record[i].fields.university + "</td>" +
                            "<td>" + scientific_record[i].fields.place + "</td>" +
                            "<td>" + scientific_record[i].fields.graduated_year + "</td>" +
                            "</tr>";
                        $('#researcher_scientific_record').html(table_row)
                    }
                } else {
                    $('#researcher_scientific_record').html(`<tr><td colspan="5">هیچ اطلاعاتی توسط کاربر ثبت نشده</td></tr>`);
                }

                let executive_record = JSON.parse(data.executive_record);
                if (executive_record.length !== 0) {
                    let table_row = "";
                    for (let i = 0; i < executive_record.length; i++) {
                        table_row = table_row + "<tr>" +
                            "<td>" + executive_record[i].fields.post + "</td>" +
                            "<td>" + executive_record[i].fields.place + "</td>" +
                            "<td>" + executive_record[i].fields.city + "</td>" +
                            "<td>" + executive_record[i].fields.start + "</td>" +
                            "<td>" + executive_record[i].fields.end + "</td>" +
                            "</tr>";
                        $('#researcher_executive_record').html(table_row)
                    }
                } else {
                    $('#researcher_executive_record').html(`<tr><td colspan="5">هیچ اطلاعاتی توسط کاربر ثبت نشده</td></tr>`);
                }

                let research_record = JSON.parse(data.research_record);
                if (research_record.length !== 0) {
                    let table_row = "";
                    let status = "";
                    for (let i = 0; i < research_record.length; i++) {
                        switch (research_record[i].fields.status) {
                            case 1:
                                status = "در دست اجرا";
                                break;
                            case 2:
                                status = "خاتمه یافته";
                                break;
                            case 3:
                                status = "متوقف";
                                break;
                        }
                        table_row = table_row + "<tr>" +
                            "<td>" + research_record[i].fields.title + "</td>" +
                            "<td>" + research_record[i].fields.presenter + "</td>" +
                            "<td>" + research_record[i].fields.responsible + "</td>" +
                            "<td>" + status + "</td>" +
                            "</tr>";
                        $('#researcher_research_record').html(table_row);
                    }
                } else {
                    $('#researcher_research_record').html(`<tr><td colspan="4">هیچ اطلاعاتی توسط کاربر ثبت نشده</td></tr>`);
                }
                if (data.resume) {
                    // console.log(data.resume_name.substring(data.resume_name.lastIndexOf("/") + 1));
                    let fileType = returnFileType(data.resume.substring(data.resume.lastIndexOf(".") + 1).toUpperCase());
                    let resume = `
                    <div class="attach-box m-auto">
                        <span class="attach-box__img ${fileType}"></span>
                        <span class="attach-box__info">
                            <span class="attach-box__info-name">${data.resume_name.substring(data.resume_name.lastIndexOf("/") + 1)}</span>
                            <span class="attach-box__info-ext">${fileType.toUpperCase()}</span>
                        </span>
                        <span class="attach-box__option">
                            <a class="attach-box__option-download" href="${data.resume}">
                                <i class="fas fa-download"></i>
                            </a>
                        </span>
                    </div>
                    `;
                    $("#researcherInfoResume").html(resume);
                } else
                    $("#researcherInfoResume").html("");
                if (data.comments.length)
                    $(".modal#researcherInfo").find(".no-comment").attr("style", "display : none;");
                else
                    $(".modal#researcherInfo").find(".no-comment").attr("style", "display : block;");
                setComment(data.comments);
                //TODO(@sepehrmetanat): Add Researcher Techniques using a method on related Model
            },
            error: function (data) {

            },
        });
    });

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
        // these HTTP methods do not requiref CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

function researcher_remove_func() {
    $("#researcher-remove-").click(function (event) {
        let researcher_id = $(this).val();
        let project_id = $("#project_id").val();
        let parent = $(this).closest(".remove-researcher");
        $(".delete-researcher").prop("disabled", true);
        $.ajax({
            method: 'POST',
            url: '/industry/delete_researcher/',
            dataType: 'json',
            data: {researcher_id: researcher_id, project_id: project_id},
            success: function (data) {
                parent.addClass("d-none");
                iziToast.success({
                    rtl: true,
                    message: "پژوهشگر با موفقیت حذف شد.",
                    position: 'bottomLeft'
                });
            },
            error: function (data) {
                $(".delete-researcher").prop("disabled", false);
                iziToast.error({
                    rtl: true,
                    message: "اتصال با سرور با مشکل رو به رو شده است.",
                    position: 'bottomLeft'
                });
            }
        });
    });
}

researcher_remove_func();


$("#researcher-confirm-").click(function (event) {
    let researcher_id = $(this).val();
    let project_id = $("#project_id").val();
    let parent = $(this).closest(".request-response");
    $(".confirm-researcher").prop('disabled', true);
    $(".refuse-researcher").prop('disabled', true);
    $.ajax({
        method: 'POST',
        url: '/industry/confirm_researcher/',
        dataType: 'json',
        data: {researcher_id: researcher_id, project_id: project_id},
        success: function (data) {
            parent.addClass("d-none");
            parent.next(".remove-researcher").removeClass("d-none");
            researcher_remove_func();
            iziToast.success({
                rtl: true,
                message: "درخواست شما با موفقیت ثبت شد!",
                position: 'bottomLeft'
            });
        },
        error: function (data) {
            $(".confirm-researcher").prop('disabled', false);
            $(".refuse-researcher").prop('disabled', false);
            iziToast.error({
                rtl: true,
                message: "اتصال با سرور با مشکل رو به رو شده است.",
                position: 'bottomLeft'
            });
        }
    });
});

$("#researcher-reject-").click(function (event) {
    let researcher_id = $(this).val();
    let project_id = $("#project_id").val();
    let parent = $(this).closest(".request-response");
    $(".confirm-researcher").prop('disabled', true);
    $(".refuse-researcher").prop('disabled', true);
    $.ajax({
        method: 'POST',
        url: '/industry/reject_researcher/',
        dataType: 'json',
        data: {researcher_id: researcher_id, project_id: project_id},
        success: function (data) {
            parent.addClass("d-none");
            iziToast.success({
                rtl: true,
                message: "درخواست شما با موفقیت ثبت شد!",
                position: 'bottomLeft'
            });
        },
        error: function (data) {
            $(".confirm-researcher").prop('disabled', false);
            $(".refuse-researcher").prop('disabled', false);
            iziToast.error({
                rtl: true,
                message: "اتصال با سرور با مشکل رو به رو شده است.",
                position: 'bottomLeft'
            });
        }
    });
});