$(window).on("load", function () {
    init_windowSize();
    load_dialog();
    // $(".page-loader").css("display", "none");
    // $(".main").removeClass("blur-div");
}).on("resize", function () {
    init_windowSize();
    load_dialog();
});

function numbersComma(num) {
    let newNum = num.toString();
    return newNum.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
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

function showQuestion() {
    $(".show-btn").click(function () {
        const dialog = $(".show-question");
        let id = $(this).attr("id");
        $.ajax({
            method: 'GET',
            url: '/expert/show_research_question/',
            dataType: 'json',
            data: {id: id},
            success: function (data) {
                if (data.question_status === "waiting") {
                    dialog.find(".question-status").html("در حال بررسی");
                } else if (data.question_status === "not_answered") {
                    dialog.find(".question-status").html("فعال");
                } else if (data.question_status === "answered") {
                    dialog.find(".question-status").html("پاسخ داده شده");
                }
                dialog.find(".card-head").html(data.question_title);
                dialog.find(".question-date").html(data.question_date);
                dialog.find("pre#question-body").html(data.question_body);
                dialog.find(".close-answer").attr("id", id);

                if (data.question_attachment_type) {
                    dialog.find(".attach-file").attr("href", data.question_attachment_path);
                    dialog.find(".attach-name").html(data.question_attachment_name);

                    if (data.question_attachment_type === 'pdf') {
                        dialog.find(".attachment").addClass("pdf-file");
                    } else if (data.question_attachment_type === 'doc' || data.question_attachment_type === 'docx') {
                        dialog.find(".attachment").addClass("doc-file");
                    } else if (data.question_attachment_type === 'jpg' || data.question_attachment_type === 'jpeg') {
                        dialog.find(".attachment").addClass("jpg-file");
                    } else if (data.question_attachment_type === 'png') {
                        dialog.find(".attachment").addClass("png-file");
                    } /* else delete the attachments row */
                }

                let answer_list_obj = data.question_answers_list;
                if (answer_list_obj.length !== 0) {
                    show_question_answers(answer_list_obj);
                } else {
                    let no_answer = "<div class='no-comment'>متاسفانه، هنوز پاسخی به سوال شما داده نشده است.</div>";
                    dialog.find(".all-answers").html(no_answer);
                }

                question_dialog_init();

            },
            error: function (data) {

            },
        });
    });
}

$(document).ready(function () {
    /*
    * I didn't find a better place to put this;
    * so please move this part to a section you prefer.
    * By the way, it has a big problem (expect those told earlier in comments),
    * after clicking on 'show-btn' of a new research question, 'attachments' and
    * 'answers' of the previous one is still shown (in the case the previous one had it).
    */
    init_setup();
    input_focus();
    showQuestion();
    // $('*').persiaNumber();
    question_dialog_init();
    question_page_init();
    init_dialog_btn(".preview-project", ".showProject");
    init_dialog_btn(".preview-project.type-2", ".project-details");
    // init_dialog_btn(".preview-project", ".project-details");
    init_dialog_btn(".confirm_project", ".select-technique");
    init_dialog_btn("#accept-techniques", ".project-details");
    init_dialog_btn(".message-body button, .message-body-sm button", ".message-show");
    init_dialog_btn(".add-new-question", ".add-question");
    init_dialog_btn(".education-btn", ".scientific_form");
    init_dialog_btn(".executive-btn", ".executive_form");
    init_dialog_btn(".research-btn", ".research_form");
    init_dialog_btn(".paper-btn", ".paper_form");
    init_dialog_btn(".technique", ".technique-dialog-main");
    search_input(".search_message");

    $('.content').scroll(function () {
        if ($(".content").scrollTop() > 300) {
            $("a.top-button").addClass('show');
        } else {
            $("a.top-button").removeClass('show');
        }
    });

    // $(".question-info").find(".status span").html(numbersComma($(".question-info").find(".status span").html()));

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

    $(".confirm_project").click(function () {
        $.ajax({
            method: 'GET',
            url: '/expert/show_technique/',
            dataType: 'json',
            data: {'id': "None"},
            success: function (data) {
                console.log(data);
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
                $(".select-technique").find("#fancy-tree").fancytree({
                    extensions: ["glyph"],
                    checkbox: false,
                    selectMode: 1,
                    checkboxAutoHide: true,
                    clickFolderMode: 2,
                    lazyLoad: function (event, data) {
                        data.result = {url: "https://cdn.rawgit.com/mar10/fancytree/72e03685/demo/ajax-sub2.json"};
                    },
                    activate: function (event, data) {
                        $('#tags').addTag(data.node.title);
                    },
                    select: function (event, data) {

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
                select_technique(".select-technique");
            },
        });
        $('#tags').tagsInput({
            'height': 'FIT-CONTENT',
            'width': '100%',
            'defaultText': '',
            'onAddTag': newItem_label,
            'onRemoveTag': newItem_label
        });
        $("#tags_tagsinput").css("border", "none");
        $("#tags_tagsinput").find("#tags_tag").on("focus", function () {
            $(this).css("width", "fit-content");
        });
        tag_input_label("tags");
        let techniquesForm = $('.ajax-select-techniques');
        $(techniquesForm).on('keyup keypress', function (e) {
            let keyCode = e.keyCode || e.which;
            if (keyCode === 13) {
                e.preventDefault();
                return false;
            }
        });
        techniquesForm.submit(function (event) {
            event.preventDefault();
            let data = [];
            let id = $(this).attr("id");
            $.each($("#tags_tagsinput").find(".tag"), function (index, value) {
                data[index] = $(this).find("span").text();
            });
            // console.log(id);
            $.ajax({
                traditional: true,
                method: 'POST',
                url: $(this).attr('data-url'),
                data: {technique: data, id: id},
                dataType: 'json',
                success: function (data) {
                    iziToast.success({
                        rtl: true,
                        message: data.success,
                        position: 'bottomLeft'
                    });
                    $(".main").removeClass("blur-div");
                },
                error: function (data) {

                }
            });
        });
    });
    if ($(window).width() < 767) {
        // toggle slide-bar => all views
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
        // nav-tabs change => index view
        $(".nav-link").click(function () {
            $(".nav-link").removeClass("active");
            $(this).addClass("active");
            $(".nav").animate({
                scrollLeft: $(this).offset().left
            }, "slow");
        });

    } else {
        // loading();
        $(function () {
            $('[data-toggle="tooltip"]').tooltip();
        });
        init_windowSize();
        init_dialog_btn(".researcher-card-button-show", ".researcher-info-dialog");
        // $(".form-submit").click(function () {
        //     blur_div_toggle(".top-bar");
        //     blur_div_toggle(".side-bar");
        //     $(".mainInfo-body").css("display", "none");
        // });
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
        education_record();
        // executive_record();
        // research_record();
        // paper_record();
        $(".chamran_btn.technique").click(function () {
            $(".main").addClass("blur-div");
            $(".dialog-main").css("display", "block");
            close_dialog(".technique-dialog-main");
        });
        // $(".main").addClass("blur-div");
        // $(".dialog-main").css("display","block");
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
    //  Questions Page
    //****************************************//
    if (window.location.href.indexOf('questions') > -1) {
        init_dialog_btn(".show-btn", ".show-question");

        function getAllQuestions() {
            return $(".tab-content div.card").toArray();
        }

        function questionsNav(questions, element) {
            if ($(element).attr("id") === "active-questions") {
                $(".tab-content").html("");
                $.each(questions, function (i, val) {
                    if ($(val).closest("div").hasClass("active-question")) {
                        $(".tab-content").append(val);
                    }
                });
                if ($(".tab-content").is(":empty")) {
                    console.log("not active question");
                }
            } else if ($(element).attr("id") === "check-questions") {
                $(".tab-content").html("");
                $.each(questions, function (i, val) {
                    if ($(val).closest("div").hasClass("check-question")) {
                        $(".tab-content").append(val);
                    }
                });
                if ($(".tab-content").is(":empty")) {
                    console.log("not check question");
                }
            } else if ($(element).attr("id") === "answered-questions") {
                $(".tab-content").html("");
                $.each(questions, function (i, val) {
                    if ($(val).closest("div").hasClass("close-question")) {
                        $(".tab-content").append(val);
                    }
                });
                if ($(".tab-content").is(":empty")) {
                    console.log("not answered question");
                }
            } else if ($(element).attr("id") === "all-questions") {
                $(".tab-content").html(questions);
            }
            init_dialog_btn(".show-btn", ".show-question");
            showQuestion();
        }

        let questions = getAllQuestions();
        $(".nav-pills .nav-link").click(function () {
            questionsNav(questions, this);
        });

        let ResearchQuestionForm = $('.ajax-new-rq-form');
        ResearchQuestionForm.submit(function (event) {
            event.preventDefault();
            ResearchQuestionForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
                .attr("disabled", "true");
            ResearchQuestionForm.find("button[type='reset']").attr("disabled", "true");
            ResearchQuestionForm.find("label").addClass("progress-cursor");
            ResearchQuestionForm.closest(".fixed-back").find(".card").addClass("wait");
            let $thisURL = ResearchQuestionForm.attr('data-url');
            let data = new FormData(ResearchQuestionForm.get(0));
            ResearchQuestionForm.find("input").attr("disabled", "true").addClass("progress-cursor");
            // console.log(data);
            // console.log($(this).find("input[type='file']").get(0).files.item(0));
            $.ajax({
                method: 'POST',
                url: $thisURL,
                // dataType: 'json',
                data: data,
                cache: false,
                processData: false,
                contentType: false,
                success: function (data) {
                    ResearchQuestionForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                        .prop("disabled", false);
                    ResearchQuestionForm.find("button[type='reset']").prop("disabled", false);
                    ResearchQuestionForm.find("input").prop("disabled", false).removeClass("progress-cursor");
                    ResearchQuestionForm.find("label").removeClass("progress-cursor");
                    ResearchQuestionForm.closest(".fixed-back").find(".card").removeClass("wait");
                    if (data.success === "successful") {
                        $(".add-question").css("display", "none");
                        $(".main").removeClass("blur-div");
                        $(".empty-question").remove();
                        show_new_research_question();
                        let questions = getAllQuestions();
                        $(".nav-tabs .nav-item .nav-link").click(function () {
                            questionsNav(questions, this);
                        });
                        iziToast.success({
                            rtl: true,
                            message: "سوال پژوهشی با موفقیت ذخیره شد. " +
                                "لطفا منتظر تایید آن توسط ادمین بمانید.",
                            position: 'bottomLeft'
                        });
                        ResearchQuestionForm[0].reset();
                    }
                },
                error: function (data) {
                    let obj = JSON.parse(data.responseText);
                    ResearchQuestionForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                        .prop("disabled", false);
                    ResearchQuestionForm.find("button[type='reset']").prop("disabled", false);
                    ResearchQuestionForm.find("input").prop("disabled", false).removeClass("progress-cursor");
                    ResearchQuestionForm.find("label").removeClass("progress-cursor");
                    ResearchQuestionForm.closest(".fixed-back").find(".card").removeClass("wait");
                    if (obj.question_title) {
                        $("#question-title").closest("div").append("<div class='error'>" +
                            "<span class='error-body'>" +
                            "<ul class='errorlist'>" +
                            "<li>" + obj.question_title + "</li>" +
                            "</ul>" +
                            "</span>" +
                            "</div>");
                        $("input#question-title").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                    }
                    if (obj.question_title !== "undefined") {
                        $("#question-body").closest("div").append("<div class='error'>" +
                            "<span class='error-body'>" +
                            "<ul class='errorlist'>" +
                            "<li>" + obj.question_text + "</li>" +
                            "</ul>" +
                            "</span>" +
                            "</div>");
                        $("input#question-body").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                    }
                },
            })
        });
    }
    //****************************************//
    //  End Questions Page
    //****************************************//
    $(".close-answer").click(function () {
        let id = $(this).attr("id");
        $.ajax({
            method: 'GET',
            url: '/expert/terminate_research_question/',
            dataType: 'json',
            data: {id: id},
            success: function (data) {
                $('.close-answer').remove();

                iziToast.success({
                    rtl: true,
                    message: "از این به بعد پاسخی برای این سوال دریافت نخواهد شد.",
                    position: 'bottomLeft'
                });
            },
            error: function (data) {

            },
        });
    });


    /*
    Show researchers information for expert
     */
    $(".researcher-card-button-show").click(function () {
        let id = $(this).attr("id");
        let url = $(this).attr("data-url");
        let project_id = $(this).attr("value");
        $.ajax({
            method: 'GET',
            url: url,
            dataType: 'json',
            data: {id: id, project_id: project_id},
            success: function (data) {
                $(".researcher_id").attr("value", id);
                $(".project_id").attr("value", project_id);
                $('#researcher_photo').attr("src", data.photo);
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
                    tech += "<span class='border-span'>" + data.techniques[index] + "</span>";
                $("#researcher_techniques").html(tech)
                $('#researcher_university').html(data.university);
                $('#researcher_entry_year').html(data.entry_year);

                let scientific_record = JSON.parse(data.scientific_record);
                if (scientific_record.length !== 0) {
                    let table_row = "";
                    for (i = 0; i < scientific_record.length; i++) {
                        table_row = table_row + "<tr>" +
                            "<td>" + scientific_record[i].fields.major + "</td>" +
                            "<td>" + scientific_record[i].fields.grade + "</td>" +
                            "<td>" + scientific_record[i].fields.university + "</td>" +
                            "<td>" + scientific_record[i].fields.place + "</td>" +
                            "<td>" + scientific_record[i].fields.graduated_year + "</td>" +
                            "</tr>"
                        $('#researcher_scientific_record').html(table_row)
                    }
                } //TODO: Add a message saying "هیچ اطلاعاتی توسط کاربر ثبت نشده"

                let executive_record = JSON.parse(data.executive_record);
                if (executive_record.length !== 0) {
                    let table_row = "";
                    for (i = 0; i < executive_record.length; i++) {
                        table_row = table_row + "<tr>" +
                            "<td>" + executive_record[i].fields.post + "</td>" +
                            "<td>" + executive_record[i].fields.place + "</td>" +
                            "<td>" + executive_record[i].fields.city + "</td>" +
                            "<td>" + executive_record[i].fields.start + "</td>" +
                            "<td>" + executive_record[i].fields.end + "</td>" +
                            "</tr>"
                        $('#researcher_executive_record').html(table_row)
                    }
                } //TODO: Add a message saying "هیچ اطلاعاتی توسط کاربر ثبت نشده"

                let research_record = JSON.parse(data.research_record);
                if (research_record.length !== 0) {
                    let table_row = "";
                    let status = "";
                    for (i = 0; i < research_record.length; i++) {
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
                            "</tr>"
                        $('#researcher_research_record').html(table_row)
                    }
                } //TODO: Add a message saying "هیچ اطلاعاتی توسط کاربر ثبت نشده"
                setComment(data.comments);
                //TODO(@sepehrmetanat): Add Researcher Techniques using a method on related Model
            },
            error: function (data) {

            },
        });
    });
});

function education_record() {
    let myForm = $('.ajax-sci-form');
    myForm.submit(function (event) {
        event.preventDefault();
        myForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
            .attr("disabled", "true");
        myForm.find("button[type='reset']").attr("disabled", "true");
        myForm.find("label").addClass("progress-cursor");
        myForm.closest(".fixed-back").find(".card").addClass("wait");
        let $thisURL = myForm.attr('data-url');
        let data = $(this).serialize();
        myForm.find("input").attr("disabled", "true").addClass("progress-cursor");
        $.ajax({
            method: 'POST',
            url: $thisURL,
            dataType: 'json',
            data: data,
            // headers: {'X-CSRFToken': '{{ csrf_token }}'},
            // contentType: 'application/json; charset=utf-8',
            success: function (data) {
                myForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                    .prop("disabled", false);
                myForm.find("button[type='reset']").prop("disabled", false);
                myForm.find("input").prop("disabled", false).removeClass("progress-cursor");
                myForm.find("label").removeClass("progress-cursor");
                myForm.closest(".fixed-back").find(".card").removeClass("wait");
                if (data.success === "successful") {
                    $(".scientific_form").css("display", "none");
                    $(".main").removeClass("blur-div");
                    show_scientific_record();
                    iziToast.success({
                        rtl: true,
                        message: "اطلاعات با موفقیت ذخیره شد!",
                        position: 'bottomLeft'
                    });
                    myForm[0].reset();
                }
            },
            error: function (data) {
                let obj = JSON.parse(data.responseText);
                myForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                    .prop("disabled", false);
                myForm.find("button[type='reset']").prop("disabled", false);
                myForm.find("input").prop("disabled", false).removeClass("progress-cursor");
                myForm.find("label").removeClass("progress-cursor");
                myForm.closest(".fixed-back").find(".card").removeClass("wait");
                if (obj.city) {
                    $("#edu-city").closest("div").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.city + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $("input#edu-city").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                }
                if (obj.date_of_graduation) {
                    $("#edu-year").closest("div").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.date_of_graduation + "</li>" +
                        "</ul>" +
                        "</span>" +
                        "</div>");
                    $("input#edu-year").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                }
                if (obj.degree) {
                    $("#edu-section").closest("div").append("<div class='error'>" +
                        "<span class='error-body'>" +
                        "<ul class='errorlist'>" +
                        "<li>" + obj.degree + "</li>" +
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
            },
        })
    })
}

let executiveForm = $('.ajax-executive-form');
executiveForm.submit(function (event) {
    event.preventDefault();
    executiveForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    executiveForm.find("button[type='reset']").attr("disabled", "true");
    executiveForm.find("label").addClass("progress-cursor");
    executiveForm.closest(".fixed-back").find(".card").addClass("wait");
    let $thisURL = executiveForm.attr('data-url');
    let data = $(this).serialize().toString();
    executiveForm.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            executiveForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            executiveForm.find("button[type='']").prop("disabled", false);
            executiveForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            executiveForm.find("label").removeClass("progress-cursor");
            executiveForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".executive_form").css("display", "none");
                $(".main").removeClass("blur-div");
                show_executive_record();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                executiveForm[0].reset();
            }
        },
        error: function (data) {
            let obj = JSON.parse(data.responseText);
            executiveForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            executiveForm.find("button[type='']").prop("disabled", false);
            executiveForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            executiveForm.find("label").removeClass("progress-cursor");
            executiveForm.closest(".fixed-back").find(".card").removeClass("wait");
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
            if (obj.data_end_post) {
                $("#until").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.data_end_post + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#until").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.data_start_post) {
                $("#from").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.city + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#from").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.executive_post) {
                $("#duty").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.executive_post + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#duty").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.organization) {
                $("#workplace").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.organization + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#workplace").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
        },
    })
});

let researchForm = $('.ajax-research-form');
researchForm.submit(function (event) {
    event.preventDefault();
    researchForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    researchForm.find("button[type='reset']").attr("disabled", "true");
    researchForm.find("label").addClass("progress-cursor");
    researchForm.closest(".fixed-back").find(".card").addClass("wait");
    let $thisURL = researchForm.attr('data-url');
    let data = $(this).serialize().toString();
    researchForm.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
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
            let obj = JSON.parse(data.responseText);
            researchForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            researchForm.find("button[type='reset']").prop("disabled", false);
            researchForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            researchForm.find("label").removeClass("progress-cursor");
            researchForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.co_researcher) {
                $("#liable").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.co_researcher + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#liable").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.research_title) {
                $("#research_title").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.research_title + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#research_title").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.researcher) {
                $("#admin").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.researcher + "</li>" +
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

let paperForm = $('.ajax-paper-form');
paperForm.submit(function (event) {
    event.preventDefault();
    paperForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    paperForm.find("button[type='reset']").attr("disabled", "true");
    paperForm.find("label").addClass("progress-cursor");
    paperForm.closest(".fixed-back").find(".card").addClass("wait");
    let $thisURL = paperForm.attr('data-url');
    let data = $(this).serialize().toString();
    paperForm.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        // headers: {'X-CSRFToken': '{{ csrf_token }}'},
        // contentType: 'application/json; charset=utf-8',
        success: function (data) {
            paperForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            paperForm.find("button[type='reset']").prop("disabled", false);
            paperForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            paperForm.find("label").removeClass("progress-cursor");
            paperForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".paper_form").css("display", "none");
                $(".main").removeClass("blur-div");
                show_paper_record();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                paperForm[0].reset();
            }
        },
        error: function (data) {
            let obj = JSON.parse(data.responseText);
            paperForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            paperForm.find("button[type='reset']").prop("disabled", false);
            paperForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            paperForm.find("label").removeClass("progress-cursor");
            paperForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.citation) {
                $("#referring-num").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.citation + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#referring-num").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.date_published) {
                $("#publish-date").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.date_published + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#publish-date").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.published_at) {
                $("#published-at").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.published_at + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#published-at").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.research_title) {
                $("#article-name").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.research_title + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#article-name").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.impact_factor) {
                $("#impact-factor").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.impact_factor + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#impact-factor").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
        },
    })
});

function setDates(date) {
    $(".project-details .project-progress .start").html(date[0]);
    $(".project-details .project-progress .first_phase").html(date[1]);
    $(".project-details .project-progress .second_phase").html(date[2]);
    $(".project-details .project-progress .third_phase").html(date[3]);
    $(".project-details .project-progress .date_finished").html(date[4]);
}

function projectDetail(data) {
    $(".project-details").find(".card-head").html(data.project_title_persian + ' ( ' + data.project_title_english + ' )');
    $(".project-details").find(".establish-time .time-body").html(data.date);
    $(".project-details").find(".time-left .time-body").html(data.deadline);

    let techniques = "";
    for (let tech_index = 0; tech_index < data.techniques.length; tech_index++) {
        let element = data.techniques[tech_index];
        techniques += "<span class='border-span'>" +
            element +
            "</span>";
    }
    $(".techniques").html(techniques);

    $("#industry-name").html(data.industry_name);
    $("#enforced-name").html(data.enforced_name);
    $("#executive-info").html(data.executive_info);
    $("#industry_logo").attr("src", data.industry_logo);
    $(".budget-amount").html(data.budget_amount);
    setDates(data.timeScheduling);
    setMajors(data);
    setValue(data);
    setComment(data.comments);
    researcherRequest();
}

function researcherRequest() {
    let requestForm = $("#researcher-request-ajax");
    requestForm.submit(function (event) {
        event.preventDefault();
        $(".project").attr("value", $('.showProject').attr('id'));
        let thisUrl = "request_researcher/";
        let form = new FormData(requestForm.get(0));
        $.ajax({
            method: 'POST',
            url: thisUrl,
            data: form,
            processData: false,
            contentType: false,
            success: function (data) {
                requestForm[0].reset();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
            },
            error: function (data) {

                requestForm[0].reset();
            },
        });
    });
}

let showInfo = $('.preview-project');
showInfo.click(function (event) {
    project_id = $(this).attr('id');
    $(this).closest(".card").find('.unseen-comments').html("");
    $.ajax({
        url: $(this).attr('data-url'),
        method: 'GET',
        data: {
            id: project_id
        },
        dataType: 'json',
        success: function (data) {
            $('.project_id').attr('value', project_id);
            if (data.status === "non active") {
                $(".hidden").attr("style", "display : none;");
                $(".showProject").find(".card-head").html('(' + data.project_title_english + ') ' + data.project_title_persian);
                $(".showProject").find(".establish-time .time-body").html(data.date);
                $(".showProject").find(".time-left .time-body").html(data.deadline);
                const keys = JSON.parse(data.key_words);
                let keys_code = '';
                for (let i = 0; i < keys.length; i++) {
                    keys_code = keys_code + "<span class='border-span'>" + keys[i].pk + "</span>"
                }
                $(".techniques").html(keys_code);
                setMajors(data);
                setValue(data);
                setComment(data.comments);

                if (data.applied === true) {
                    $("#accept-project").attr("disabled", "disabled");
                }
            } else {
                projectDetail(data);
            }
        },
        error: function (data) {
        }

    })
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
        data.required_method +
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
        numbersComma(data.required_budget) + " ریال" +
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
        "</div></div>" +
        "<div>" +
        "<div class='question'>" +
        "<span class='question-mark'>" +
        "<i class='far fa-question-circle'></i>" +
        "</span>" +
        "برآورد شما از سود مالی این پروژه چگونه است؟" +
        "</div>" +
        "<div class='answer'>" +
        numbersComma(data.predict_profit) + " ریال" +
        "</div></div>";
    $(".project-info-content").html(majors);
}

function setValue(data) {
    $("#v-pills-roles-tab").click(function () {
        setRole(data);
        $('*').persiaNumber();
    });
    $("#v-pills-resources-tab").click(function () {
        setResources(data);
        $('*').persiaNumber();
    });
    $("#v-pills-approaches-tab").click(function () {
        setApproach(data);
        $('*').persiaNumber();
    });
    $("#v-pills-majors-tab").click(function () {
        setMajors(data);
        $('*').persiaNumber();
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
            comments_code += "<div class='my-comment' id='" + data[i].pk + "' >" +
                "   <div class='comment-profile'></div>" +
                "       <div class='" + comment_body_classes + "'>" +
                "           <span class='comment-tools'>" +
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
                "           </span>";
            if (data[i].attachment !== "None") {
                comments_code += "<a href='/" + data[i].attachment + "' class='attached-file'>" +
                    "   <i class='fas fa-paperclip'></i>" +
                    "   <span>" + data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1) + "</span>" +
                    "</a>";
            }
            comments_code += "<pre>" + data[i].text + "</pre>" +
                "   </div>" +
                "</div>";
        } else if (data[i].sender_type === "researcher" || data[i].sender_type === "industry") { //researcher or industry
            let comment_body_classes = "comment-body";
            if (data[i].attachment !== "None") {
                comment_body_classes += " attached";
            }
            comments_code += "<div class='your-comment'>" +
                "   <div class='" + comment_body_classes + "' dir='ltr'>" +
                "       <span class='comment-tools'>" +
                // "           <i class='fas fa-reply'" + data[i].pk + "></i>" +
                "       </span>";
            if (data[i].attachment !== "None") {
                comments_code += "<a href='/" + data[i].attachment + "' class='attached-file'>" +
                    "   <i class='fas fa-paperclip'></i>" +
                    "   <span>" + data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1) + "</span>" +
                    "</a>";
            }
            comments_code += "<pre>" + data[i].text + "</pre>" +
                "   </div>" +
                "</div>";
        } else { //system
            comments_code += "<div class='system-comment'>" +
                "<div class='comment-body' dir='ltr'>" +
                "<pre>" +
                data[i].text +
                "</pre>" +
                "</div>" +
                "</div>";
        }
    }
    $('.comments').html(comments_code).animate({scrollTop: $('.comments').prop("scrollHeight")}, 1000);
    $(".comments .fa-trash-alt").closest(".dropdown-item").click(function () {
        deleteComment($(this).closest('.my-comment'));
    });
}

function addComment(data) {
    let comment_body_classes = "comment-body";
    if (data.attachment !== "None") {
        comment_body_classes += " attached";
    }
    let comment_code = "<div class='my-comment' id='" + data.pk + "' >" +
        "<div class='" + comment_body_classes + "' dir='ltr'>" +
        "   <span class='comment-tools'>" +
        "       <div class='btn-group dropdown'>" +
        "           <button type='button' class='dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>" +
        "               <i class='fas fa-cog'></i>" +
        "           </button>" +
        "           <div class='dropdown-menu'>" +
        // "               <div class='dropdown-item'>" +
        // "                   <span>ویرایش پیام</span>" +
        // "                   <i class='fas fa-pen'></i>" +
        // "               </div>" +
        "               <div class='dropdown-item'>" +
        "                   <span>حذف پیام</span>" +
        "                   <i class='fas fa-trash-alt'></i>" +
        "               </div>" +
        "           </div>" +
        "       </div>" +
        // "       <i class='fas fa-reply' value=" + data.pk + ">" +
        // "           <div class='reply'></div>" +
        // "       </i>" +
        "   </span>";
    if (data.attachment !== "None") {
        comment_code +=
            "<a href='/" + data.attachment + "' class='attached-file'>" +
            "   <i class='fas fa-paperclip'></i>" +
            "   <span>" + data.attachment.substring(data.attachment.lastIndexOf("/") + 1) + "</span>" +
            "</a>"
    }
    comment_code += "<pre>" + data.description + "</pre>" +
        "   </div>" +
        "</div>";
    return comment_code;
}

let comment_form = $('#comment_form');
comment_form.submit(function (event) {
    event.preventDefault();
    comment_form.find("button[type='submit']").attr("disabled", "true");
    let thisUrl = "";
    if (comment_form.find(".researcher_id").val() === "")
        thisUrl = "/expert/industry_comment/";
    else
        thisUrl = "/expert/researcher_comment/";
    $(".project_id").attr('value', $('.showProject').attr("id"));
    let form = new FormData(comment_form.get(0));
    $.ajax({
        method: 'POST',
        url: thisUrl,
        data: form,
        processData: false,
        contentType: false,
        success: function (data) {
            comment_form.find("button[type='submit']").prop("disabled", false);
            comment_form.closest(".fixed-back").find(".card").removeClass("wait");
            let comment_code = addComment(data);
            $(".project-comment-innerDiv").find(".comments").append(comment_code);
            iziToast.success({
                rtl: true,
                message: "پیام با موفقیت ارسال شد!",
                position: 'bottomLeft'
            });

            $(".comments .fa-trash-alt").closest(".dropdown-item").click(function () {
                deleteComment($(this).closest('.my-comment'));
            });

            comment_form[0].reset();
            $('.error').remove();
            $('.file-name').html("");
            $(".send-comment-container .comment-input").removeClass("attached");
            $('.comments').animate({scrollTop: $('.comments').prop("scrollHeight")}, 1000);

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
            comment_form[0].reset();
        },
    });
});

// Researcher Request Page
if (window.location.href.indexOf("expert/researcher/") > 0) {

    $.each($(".box.no-border").toArray(), function (key, val) {
        let score = parseInt($(val).find(".box-score .score-amount").text());
        $(val).find(".box-score .score-amount").text(score);
        for (let i = 2; i < 7; i++) {
            let circle = $(val).find(".box-score .circle:nth-child(" + i + ")");
            if (score - 2 >= 0) {
                circle.addClass("fill");
            } else if (score - 2 === -1){
                circle.addClass("semi-fill");
                break
            }
            score -= 2;
        }
    });

    $('.confirm-researcher').click(function () {
        $.ajax({
            method: "POST",
            url: 'confirmResearcher/',
            dataType: "json",
            data: {
                researcher_id: $(this).attr("id"),
                project_id: $('.div_project_id').attr("id")
            },
            success: function (data) {
                iziToast.success({
                    rtl: true,
                    message: "پژوهشگر با موفقیت به پروژه اضافه شد.",
                    position: 'bottomLeft'
                });
            },
            error: function (data) {
                console.log("Error");
            }
        });
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
        return cookieValue;
    }
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