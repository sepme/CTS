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
    $("[data-target='#showQuestion']").off();
    $("[data-target='#showQuestion']").click(function () {
        const dialog = $("#showQuestion");
        let id = $(this).attr("id");
        dialog.css("display", "none");
        mBackdrop = setTimeout("haveBackdrop()", 100);
        $.ajax({
            method: 'GET',
            url: '/expert/show_research_question/',
            dataType: 'json',
            data: {id: id},
            success: function (data) {
                if (data.question_status === "waiting") {
                    $('.close-answer').hide();
                    dialog.find(".modal-footer").append(`<button class="default-btn w-100" disabled>پاسخ های این سوال بسته شده است!</button>`);
                    $('.close-answer').prop('disabled', true);
                    dialog.find(".question-status").html("در حال بررسی");
                } else if (data.question_status === "not_answered") {
                    $('.close-answer').show();
                    $('.close-answer').prop('disabled', false);
                    dialog.find(".question-status").html("فعال");
                } else if (data.question_status === "answered") {
                    $('.close-answer').hide();
                    dialog.find(".modal-footer").append(`<button class="default-btn w-100" disabled>پاسخ های این سوال بسته شده است!</button>`);
                    $('.close-answer').prop('disabled', true);
                    dialog.find(".question-status").html("پاسخ داده شده");
                }
                dialog.find(".modal-header .modal-title").html(data.question_title);
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
                    dialog.find(".no-comment").attr("style", "display: block");
                    dialog.on("hidden.bs.modal", function () {
                        $(this).find(".no-comment").removeAttr("style");
                    });
                }

                question_dialog_init();
                $(".modal-backdrop div.lds-roller").css("display", "none");
                dialog.css("display", "block");

                dialog.on('hidden.bs.modal', function () {
                    $(this).find(".all-answers").html("");
                    if ($(this).find(".modal-footer button:not(.close-answer)").length) {
                        $(this).find(".modal-footer button:not(.close-answer)").remove();
                    }
                });
            },
            error: function (data) {

            },
        });
    });
}

function init_confirm_project() {
    $(".confirm_project").click(function () {
        $('#showProject').modal('toggle');
        $('#selectTechniques').modal('toggle');
        $('#selectTechniques .close__redirect').click(function () {
            $('#selectTechniques').modal('toggle');
            $('#showProject').modal('toggle');
        });
        $.ajax({
            method: 'GET',
            url: '/expert/show_technique/',
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
                $("#selectTechniques").find("#fancy-tree").fancytree({
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
                select_technique("#selectTechniques");
            },
        });
        $('#tags').tagsInput({
            'height': 'FIT-CONTENT',
            'width': '100%',
            'defaultText': '',
            'onAddTag': newItem_label,
            'onRemoveTag': newItem_label
        });
        $("#tags_tagsinput #tags_addTag").css("display", "none");
        $('#tags_tagsinput').addClass("border-0 mt-0");
        $("#tags_tagsinput").find("#tags_tag").on("focus", function () {
            $(this).css("width", "fit-content");
        });
        tag_input_label("tags");
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
    // init_dialog_btn(".preview-project", ".showProject");
    // init_dialog_btn(".preview-project.type-2", ".project-details");
    // init_dialog_btn(".preview-project", ".project-details");
    // init_dialog_btn(".confirm_project", ".select-technique");
    // init_dialog_btn("#accept-techniques", ".project-details");
    init_dialog_btn(".message-body button, .message-body-sm button", ".message-show");
    // init_dialog_btn(".add-new-question", ".add-question");
    // init_dialog_btn(".education-btn", ".scientific_form");
    // init_dialog_btn(".executive-btn", ".executive_form");
    // init_dialog_btn(".research-btn", ".research_form");
    // init_dialog_btn(".paper-btn", ".paper_form");
    init_dialog_btn(".technique", ".technique-dialog-main");
    search_input(".search_message");
    researcherRequest();

    // Auto scroll to active project tab when exists
    let activeTab = $(".tab-pane#nav-active-projects");
    if (activeTab.length && activeTab.find(".card").length) {
        $("#nav-all-projects-tab").removeClass("active");
        $("#nav-active-projects-tab").addClass("active");
        $("#nav-all-projects").removeClass('show active');
        activeTab.tab('show');
    }

    $('.content').scroll(function () {
        if ($(".content").scrollTop() > 300) {
            $("a.top-button").addClass('show');
        } else {
            $("a.top-button").removeClass('show');
        }
    });

    $(".add-comment").each(function () {
        let comment_form = $(this).find('#comment_form');
        comment_form.submit(function (event) {
            event.preventDefault();
            console.log("sending...");
            comment_form.find("button[type='submit']").attr("disabled", "true");
            let thisUrl = "";
            if (comment_form.find(".researcher_id").val() === "")
                thisUrl = "/expert/industry_comment/";
            else
                thisUrl = "/expert/researcher_comment/";
            if (comment_form.closest("#showProject").length > 0) {
                $(".project_id").attr('value', $('.showProject').attr("id"));
            } else {
                $(".project_id").attr('value', $(this).closest(".add-comment").attr("id"));
            }
            let form = new FormData(comment_form.get(0));
            console.log(form);
            $.ajax({
                method: 'POST',
                url: thisUrl,
                data: form,
                processData: false,
                contentType: false,
                success: function (data) {
                    comment_form.find("button[type='submit']").prop("disabled", false);
                    let comment_code = addComment(data);
                    if (comment_form.closest(".section").find(".project-comment-innerDiv").find(".no-comment").length > 0) {
                        comment_form.closest(".section").find(".project-comment-innerDiv").find(".no-comment").attr("style", "display: none;");
                    }
                    comment_form.closest(".section").find(".project-comment-innerDiv").find(".comments").append(comment_code);
                    iziToast.success({
                        rtl: true,
                        message: "پیام با موفقیت ارسال شد!",
                        position: 'bottomLeft'
                    });

                    comment_form.closest(".section").find(".comments .fa-trash-alt").closest(".dropdown-item").click(function () {
                        deleteComment($(this).closest('.my-comment'));
                    });

                    comment_form[0].reset();
                    comment_form.closest(".section").find("textarea#description").removeClass("error");
                    comment_form.closest(".section").find('.error').remove();
                    comment_form.closest(".section").find('.file-name').html("");
                    comment_form.closest(".section").find(".send-comment-container .comment-input").removeClass("attached");
                    comment_form.closest(".section").find('.comments').animate({scrollTop: comment_form.closest(".section").find('.comments').prop("scrollHeight")}, 1000);
                    comment_form.find("textarea#description").css("height", "41px");
                },
                error: function (data) {
                    console.log(data);
                    let obj = JSON.parse(data.responseText);
                    comment_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                        .prop("disabled", false);
                    comment_form.find("label").removeClass("progress-cursor");
                    comment_form.closest(".fixed-back").find(".card").removeClass("wait");
                    if (obj.description) {
                        comment_form.closest(".section").find("#description").closest("div").append("<div class='error'>" +
                            "<span class='error-body'>" +
                            "<ul class='errorlist'>" +
                            "<li>" + obj.description + "</li>" +
                            "</ul>" +
                            "</span>" +
                            "</div>");
                        comment_form.closest(".section").find("textarea#description").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                    }
                    comment_form[0].reset();
                },
            });
        });
    });

    // Check user id
    if ($("#userID").length) {
        $("input#userID").on("focusout", function () {
            $(".userId-error").remove();
            let thisFormGroup = $(this).closest(".form-group");
            if ($(this).val()) {
                thisFormGroup.find(".form-group__status").removeClass("check").removeClass("success")
                    .removeClass("fail");
                thisFormGroup.find(".form-group__status").addClass("check");
                thisFormGroup.find("input").removeClass("error");
                $.ajax({
                    method: "POST",
                    url: "/expert/checkUserId",
                    data: {"user_id": $(this).val()},
                    success: function (data) {
                        thisFormGroup.find(".form-group__status").removeClass("check");
                        if (data.invalid_input) {
                            thisFormGroup.find(".form-group__status").addClass("fail");
                            thisFormGroup.find("input").addClass("error");
                        } else if (data.is_unique) {
                            thisFormGroup.find(".form-group__status").addClass("success");
                        } else {
                            thisFormGroup.find(".form-group__status").addClass("fail");
                            thisFormGroup.find("input").addClass("error");
                        }
                    },
                    error: function (data) {
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

    init_confirm_project();

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
        // iziToast.success({
        //     rtl: true,
        //     message: "درخواست شما ارسال شد.",
        //     position: 'bottomLeft',
        //     duration: 9999,
        // });
        $.ajax({
            traditional: true,
            method: 'POST',
            url: $(this).attr('data-url'),
            data: {technique: data, id: id},
            dataType: 'json',
            success: function (data) {
                iziToast.success({
                    rtl: true,
                    message: data.message,
                    position: 'bottomLeft',
                });
                $('#selectTechniques').modal('toggle');
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
            }
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
        // education_record();
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
    //  User Info
    //****************************************//

    if (window.location.href.indexOf('/expert/userInfo/') > -1) {
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
                <button class="btn btn-primary mt-4" type="button" id="changeAttachment">حذف فایل</button>
            `;
                $(this).closest(".attach__container").find(".form-group").remove();
                $(this).closest(".attach__container").append(attachment);
                $("#changeAttachment").click(function () {
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
                    </div>
                    <input type="file" class="form-control-file"
                                id="uploadResume" name="resume" hidden>
                `);
                    putAttachment($("input#uploadResume"));
                });
            });
        }

        if ($("input#uploadResume").length) {
            putAttachment($("input#uploadResume"));
        }

        if ($("#changeAttachment").length) {
            $("#changeAttachment").click(function () {
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
                    </div>
                    <input type="file" class="form-control-file"
                            id="uploadResume" name="resume" hidden>
                `);
                putAttachment($("input#uploadResume"));
            });
        }

        sci_record_option();
        exe_record_option();
        research_record_option();
        paper_record_option();

        let scientificForm = $('.ajax-sci-form');
        scientificForm.submit(function (event) {
            event.preventDefault();

            scientificForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
                .attr("disabled", "true");
            scientificForm.find("button[type='reset']").attr("disabled", "true");
            scientificForm.find("label").addClass("progress-cursor");
            scientificForm.closest(".fixed-back").find(".card").addClass("wait");
            let $thisURL = scientificForm.attr('action');
            let data = $(this).serialize();
            scientificForm.find("input").attr("disabled", "true").addClass("progress-cursor");

            $("input#edu-city").removeClass("error").css("color", "").prev().css("color", "");
            $("input#edu-year").removeClass("error").css("color", "").prev().css("color", "");
            $("input#edu-section").removeClass("error").css("color", "").prev().css("color", "");
            $("input#edu-subject").removeClass("error").css("color", "").prev().css("color", "");
            $("input#university").removeClass("error").css("color", "").prev().css("color", "");
            $('.error').remove();

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
                        show_scientific_record(data.id);
                        scientificForm[0].reset();
                        scientificForm.closest(".modal").modal("hide");
                        iziToast.success({
                            rtl: true,
                            message: "اطلاعات با موفقیت ذخیره شد!",
                            position: 'bottomLeft'
                        });
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
                    display_error(scientificForm);
                },
            })
        });

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

            $("input#exe-city").removeClass("error").css("color", "").prev().css("color", "");
            $("input#from").removeClass("error").css("color", "").prev().css("color", "");
            $("input#until").removeClass("error").css("color", "").prev().css("color", "");
            $("input#duty").removeClass("error").css("color", "").prev().css("color", "");
            $("input#workplace").removeClass("error").css("color", "").prev().css("color", "");
            $(".error").remove();

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
                        show_executive_record(data.id);
                        executiveForm[0].reset();
                        executiveForm.closest(".modal").modal("hide");
                        iziToast.success({
                            rtl: true,
                            message: "اطلاعات با موفقیت ذخیره شد!",
                            position: 'bottomLeft'
                        });
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
                    if (obj.date_end_post) {
                        $("#until").closest("div").append("<div class='error'>" +
                            "<span class='error-body'>" +
                            "<ul class='errorlist'>" +
                            "<li>" + obj.date_end_post + "</li>" +
                            "</ul>" +
                            "</span>" +
                            "</div>");
                        $("input#until").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
                    }
                    if (obj.date_start_post) {
                        $("#from").closest("div").append("<div class='error'>" +
                            "<span class='error-body'>" +
                            "<ul class='errorlist'>" +
                            "<li>" + obj.date_start_post + "</li>" +
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
                    display_error(executiveForm);
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

            $("input#liable").removeClass("error").css("color", "").prev().css("color", "");
            $("input#subject").removeClass("error").css("color", "").prev().css("color", "");
            $("input#admin").removeClass("error").css("color", "").prev().css("color", "");
            $("input#rank").removeClass("error").css("color", "").prev().css("color", "");
            $('.error').remove();

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
                        $(".research_form").removeClass("show");
                        $(".main").removeClass("blur-div");
                        show_research_record(data.id);
                        researchForm[0].reset();
                        researchForm.closest(".modal").modal("hide");
                        iziToast.success({
                            rtl: true,
                            message: "اطلاعات با موفقیت ذخیره شد!",
                            position: 'bottomLeft'
                        });
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
                        $("#subject").closest("div").append("<div class='error'>" +
                            "<span class='error-body'>" +
                            "<ul class='errorlist'>" +
                            "<li>" + obj.research_title + "</li>" +
                            "</ul>" +
                            "</span>" +
                            "</div>");
                        $("input#subject").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
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
                    display_error(researchForm);
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

            $("input#referring-num").removeClass("error").css("color", "").prev().css("color", "");
            $("input#publish-date").removeClass("error").css("color", "").prev().css("color", "");
            $("input#published-at").removeClass("error").css("color", "").prev().css("color", "");
            $("input#article-name").removeClass("error").css("color", "").prev().css("color", "");
            $("input#impact-factor").removeClass("error").css("color", "").prev().css("color", "");
            $('.error').remove();

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
                        $(".paper_form").removeClass("show");
                        $(".main").removeClass("blur-div");
                        show_paper_record(data.id);
                        paperForm[0].reset();
                        paperForm.closest(".modal").modal("hide");
                        iziToast.success({
                            rtl: true,
                            message: "اطلاعات با موفقیت ذخیره شد!",
                            position: 'bottomLeft'
                        });
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
                    display_error(paperForm);
                },
            })
        });

        $("#waitToGet .modal-footer button.btn-primary").click(function (event) {
            let btnClicked = $(this);
            btnClicked.closest(".modal-footer").find("button").addClass("d-none");
            btnClicked.closest(".modal-content").find(".modal-header .modal-title").addClass("d-none");
            btnClicked.closest(".modal-content").find(".modal-body #insertLink").addClass("d-none");
            btnClicked.closest(".modal-content").find(".modal-body #waitingToCheck").removeClass("d-none");
            let webScrappingForm = btnClicked.closest(".modal-content").find("#ajax-web-scrapping-form");
            $.ajax({
                method: webScrappingForm.attr("method"),
                url: webScrappingForm.attr("action"),
                data: webScrappingForm.serialize(),
                success: function (data) {
                    btnClicked.closest(".modal-footer").find("button").removeClass("d-none");
                    btnClicked.closest(".modal-content").find(".modal-header .modal-title").removeClass("d-none");
                    btnClicked.closest(".modal-content").find(".modal-body #insertLink").removeClass("d-none");
                    btnClicked.closest(".modal-content").find(".modal-body #waitingToCheck").addClass("d-none");
                    webScrappingForm.closest(".modal").modal("hide");
                    $("#resumeValidation").modal("show");
                    console.log(data);
                    $("#resumeValidation #expertUniDetected").html(data.university.replace("دانشگاه", ""));
                },
                error: function (data) {
                    btnClicked.closest(".modal-footer").find("button").removeClass("d-none");
                    btnClicked.closest(".modal-content").find(".modal-header .modal-title").removeClass("d-none");
                    btnClicked.closest(".modal-content").find(".modal-body #insertLink").removeClass("d-none");
                    btnClicked.closest(".modal-content").find(".modal-body #waitingToCheck").addClass("d-none");
                    iziToast.error({
                        rtl: true,
                        message: "ارتباط با سرور با مشکل مواجه شد.\nلطفا دوباره امتحان کنید!",
                        position: 'bottomLeft'
                    });
                }
            })
        });
    }

    //****************************************//
    //  End User Info
    //****************************************//


    // init_dialog_btn(".researcher-card-button-show", ".researcher-info-dialog");
    //****************************************//
    //  Questions Page
    //****************************************//
    if (window.location.href.indexOf('questions') > -1) {
        // init_dialog_btn(".show-btn", ".show-question");

        $(".close-answer").click(function () {
            let id = $(this).attr("id");
            let modalFooter = $(this).closest(".modal-footer");
            $.ajax({
                method: 'GET',
                url: '/expert/terminate_research_question/',
                dataType: 'json',
                data: {id: id},
                success: function (data) {
                    modalFooter.find("button.close-answer").hide().prop("disabled", true);
                    modalFooter.append(`<button class="default-btn w-100" disabled>پاسخ های این سوال بسته شده است!</button>`);
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
            // init_dialog_btn(".show-btn", ".show-question");
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
                        show_new_research_question(data.id);
                        let questions = getAllQuestions();
                        $(".nav-tabs .nav-item .nav-link").click(function () {
                            questionsNav(questions, this);
                        });
                        showQuestion();
                        iziToast.success({
                            rtl: true,
                            message: "سوال پژوهشی با موفقیت ذخیره شد. " +
                                "لطفا منتظر تایید آن توسط ادمین بمانید.",
                            position: 'bottomLeft'
                        });
                        ResearchQuestionForm[0].reset();
                    }
                    $('#addNewQuestion').modal('toggle');
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


    /*
    Show researchers information for expert
     */
    $("button[data-target='#researcherInfo']").click(function () {
        let id = $(this).attr("id");
        let url = $(this).attr("data-url");
        let project_id = $(this).attr("value");
        // console.log("id ", id);
        // console.log("url ", url);
        // console.log("p_id ", project_id);
        $.ajax({
            method: 'GET',
            url: url,
            dataType: 'json',
            data: {id: id, project_id: project_id},
            success: function (data) {
                // console.log(data);
                if (data.status === "justComment") {
                    $('.request-response').attr("style", "display : none;");
                    $(".confirm-researcher").prop('disabled', true);
                    $(".refuse-researcher").prop('disabled', true);
                } else {
                    $('.request-response').attr("style", "display : block;");
                    $(".confirm-researcher").prop('disabled', false);
                    $(".refuse-researcher").prop('disabled', false);
                }
                $("#researcherInfo").find(".add-comment").attr("id", project_id);
                $(".researcher_id").attr("value", id);
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
                console.log(data);
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
                    for (i = 0; i < scientific_record.length; i++) {
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
                    for (i = 0; i < executive_record.length; i++) {
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
                setComment(data.comments, $(".modal#researcherInfo"));
                //TODO(@sepehrmetanat): Add Researcher Techniques using a method on related Model
            },
            error: function (data) {

            },
        });
    });

    // $("#active-project").click(function () {
    //     $(".new-project").attr("style", "display :none;");
    //     $(".done-project").attr("style", "display :none;");
    //     $(".your-project").attr("style", "display :block;");
    // });
    //
    // $("#new-projects").click(function () {
    //     $(".new-project").attr("style", "display :block");
    //     $(".done-project").attr("style", "display :none");
    //     $(".your-project").attr("style", "display :none");
    // });
    //
    // $("#done-project").click(function () {
    //     $(".new-project").attr("style", "display :none");
    //     $(".your-project").attr("style", "display :none");
    //     $(".done-project").attr("style", "display :block");
    // });
});

function setDates(date) {
    $(".project-details .project-progress .start").html(date[0]);
    $(".project-details .project-progress .first_phase").html(date[1]);
    $(".project-details .project-progress .second_phase").html(date[2]);
    $(".project-details .project-progress .third_phase").html(date[3]);
    $(".project-details .project-progress .date_finished").html(date[4]);
}

function projectDetail(data) {
    $(".project-details").find(".card-head").html(data.persian_title + "<br>" + ' ( ' + data.english_title + ' )');
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
    $("#enforcer-name").html(data.enforcer_name);
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
        let thisUrl = "/expert/request_researcher/";
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
                requestForm[0].reset();
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
}

let showInfo = $('.preview-project');
showInfo.click(function (event) {
    let project_id = $(this).attr('id');
    $(this).closest(".card").find('.unseen-comments').html("");
    $.ajax({
        url: $(this).attr('data-url'),
        method: 'GET',
        data: {
            id: project_id
        },
        dataType: 'json',
        success: function (data) {
            console.log(data);
            if (data.applied === true) {
                $("#accept-project").attr("disabled", "disabled").css("pointer-events", "none");
                let btn = $("#accept-project").closest(".modal-footer").html();
                $("#accept-project").closest(".modal-footer").html(
                    `<span tabindex="0" data-placement='right' data-toggle="tooltip" data-html="true"
                        title="<p class='m-0' dir='rtl'>شما تکنیک های لازم برای پروژه را ثبت کرده اید!</p>">
                        ${btn}
                    </span>`
                );
                $('#accept-project').closest("span").tooltip();
                $(".modal#showProject").on("hidden.bs.modal", function () {
                    $(this).closest(".modal-footer").html(`
                        <button class="btn btn-primary save-btn confirm_project" id="accept-project">
                            تایید و انتخاب تکینک
                        </button>
                    `);
                    init_confirm_project();
                });
            }
            $('.project_id').attr('value', project_id);
            $('.ajax-select-techniques').attr('id', project_id);
            if (data.status === "non active") {
                $(".hidden").attr("style", "display : none;");
                $("#showProject").find(".modal-header .modal-title").html(data.persian_title + "<br>" + data.english_title);
                $("#showProject").find(".establish-time .time-body").html(data.date);
                $("#showProject").find(".time-left .time-body").html(data.deadline);
                const keys = JSON.parse(data.key_words);
                let keys_code = '';
                for (let i = 0; i < keys.length; i++) {
                    keys_code = keys_code + "<span class='border-span'>" + keys[i].pk + "</span>"
                }
                $(".techniques").html(keys_code);
                setMajors(data);
                setValue(data);
                setComment(data.comments, $(".modal#showProject"));
                // vote_dialog_init(".showProject");
            } else {
                $(".project_id").attr("value", project_id);
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

// "<div>" +
// "<div class='question'>" +
// "<span class='question-mark'>" +
// "<i class='far fa-question-circle'></i>" +
// "</span>" +
// "برآورد شما از سود مالی این پروژه چگونه است؟" +
// "</div>" +
// "<div class='answer'>" +
// numbersComma(data.predict_profit) + " ریال" +
// "</div></div>";

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


function addComment(data) {
    let comment_body_classes = "comment-body";
    if (data.attachment !== "None") {
        comment_body_classes += " attached";
    }
    let comment_code = "<div class='my-comment' id='" + data.pk + "' >" +
        "<div class='comment-profile'></div>" +
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
        "                   <i class='fas fa-trash-alt'></i>" +
        "                   <span>حذف پیام</span>" +
        "               </div>" +
        "           </div>" +
        "       </div>" +
        // "       <i class='fas fa-reply' value=" + data.pk + ">" +
        // "           <div class='reply'></div>" +
        // "       </i>" +
        "   </span>" +
        "       <div class='" + comment_body_classes + "'>" +
        "<pre>" + data.description + "</pre>";
    if (data.attachment !== "None") {
        comment_code +=
            "<a href='/" + data.attachment + "' class='attached-file'>" +
            "   <i class='fas fa-paperclip'></i>" +
            "   <span>" + data.attachment.substring(data.attachment.lastIndexOf("/") + 1) + "</span>" +
            "</a>"
    }
    comment_code += "" +
        "   </div>" +
        "</div>";
    return comment_code;
}

// Researcher Request Page
if (window.location.href.indexOf("expert/researcher/") > 0) {

    // $.each($(".box.no-border").toArray(), function (key, val) {
    //     let score = parseInt($(val).find(".box-score .score-amount").text());
    //     $(val).find(".box-score .score-amount").text(score);
    //     for (let i = 2; i < 7; i++) {
    //         let circle = $(val).find(".box-score .circle:nth-child(" + i + ")");
    //         if (score - 2 >= 0) {
    //             circle.addClass("fill");
    //         } else if (score - 2 === -1) {
    //             circle.addClass("semi-fill");
    //             break
    //         }
    //         score -= 2;
    //     }
    // });

    $('.confirm-researcher').click(function () {
        const thisBtn = $(this);
        $.ajax({
            method: "POST",
            url: 'confirmResearcher/',
            dataType: "json",
            data: {
                researcher_id: $(this).attr("id"),
                project_id: $(this).val(),
            },
            success: function (data) {
                iziToast.success({
                    rtl: true,
                    message: "پژوهشگر با موفقیت به پروژه اضافه شد.",
                    position: 'bottomLeft'
                });
                $(thisBtn).closest(".card").closest("div.col-12").remove();
                if ($(".container > .row:nth-child(3)").find("div").length === 0) {
                    $(".container > .row:nth-child(3)").html(
                        `<div class="col-12 text-center">
                            <div class="empty-page">
                                <div class="empty-page-container">
                                    <img src="../../static/img/empty-tray.svg" alt="">
                                    <pre>هنوز پژوهشگری برای پروژه‌های شما درخواست نداده است.</pre>
                                </div>
                            </div>
                        </div>`
                    );
                }
            },
            error: function (data) {
                console.log("Error");
            }
        });
    });
    $(".refuse-researcher").click(function () {
        const thisBtn = $(this);
        $.ajax({
            method: "POST",
            url: 'refuseResearcher/',
            dataType: "json",
            data: {
                researcher_id: $(this).attr("id"),
                project_id: $(this).val(),
            },
            success: function (data) {
                iziToast.success({
                    rtl: true,
                    message: "درخواست پژوهشگر با موفقیت رد شد.",
                    position: 'bottomLeft'
                });
                $(thisBtn).closest(".card").closest("div.col-12").remove();
                if ($(".container > .row:nth-child(3)").find("div").length === 0) {
                    $(".container > .row:nth-child(3)").html(
                        `<div class="col-12 text-center">
                            <div class="empty-page">
                                <div class="empty-page-container">
                                    <img src="../../static/img/empty-tray.svg" alt="">
                                    <pre>هنوز پژوهشگری برای پروژه‌های شما درخواست نداده است.</pre>
                                </div>
                            </div>
                        </div>`
                    );
                }
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