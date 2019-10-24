$(window).on("load", function () {
    init_windowSize();
    load_dialog();
    // $(".page-loader").css("display", "none");
    // $(".main").removeClass("blur-div");
}).on("resize", function () {
    init_windowSize();
    load_dialog();
});
$(document).ready(function () {
    $('*').persiaNumber();
    input_focus();
    question_dialog_init();
    question_page_init();
    init_dialog_btn(".chamran-btn-info", ".showProject");
    init_dialog_btn(".message-body button, .message-body-sm button", ".message-show");
    init_dialog_btn(".show-btn", ".show-question");
    init_dialog_btn(".add-new-question", ".add-question");
    init_dialog_btn(".education-btn", ".scientific_form");
    init_dialog_btn(".executive-btn", ".executive_form");
    init_dialog_btn(".research-btn", ".research_form");
    init_dialog_btn(".paper-btn", ".paper_form");
    init_dialog_btn(".technique", ".technique-dialog-main");
    init_dialog_btn(".confirm_project", ".select-technique");

    /*
    */
    function RemoveTag() {
        $("#tags_tagsinput .tags_clear").css("display", "none");
        $("#tags_tagsinput span.tag a").html("<i class='fas fa-times'></i>");

    }

    function AddTag() {
        $("#tags_tagsinput .tags_clear").css("display", "none");
        $("#tags_tagsinput span.tag a").html("<i class='fas fa-times'></i>");

    }

    $('#tags').tagsInput({
        'height': 'FIT-CONTENT',
        'width': '100%',
        'defaultText': '',
        'onAddTag': AddTag,
        'onRemoveTag': RemoveTag,
    });
    $("#accept-techniques").click(function () {
       var techniques = $("#tags").val();
       /*
        * Add Ajax code here ,Mr Hamid ;)
        */
    });
    $("#tags_tagsinput .tags_clear").css("display", "none");
    $("#tags_tagsinput span.tag a").html("<i class='fas fa-times'></i>");

    $("#fancy-tree").fancytree({
        extensions: ["glyph"],
        checkbox: false,
        selectMode: 2,
        checkboxAutoHide: true,
        clickFolderMode: 2,
        lazyLoad: function (event, data) {
            data.result = {url: "https://cdn.rawgit.com/mar10/fancytree/72e03685/demo/ajax-sub2.json"};
        },
        select: function (event, data) {
            alert(event.type + ": " + data.node.isSelected() + " " + data.node);
        },
        activate: function (event, data) {
            node = data.node;
            $('#tags').addTag(node.title);
        },
        source: [
            {
                "title": "histology", "key": "1", "folder": true, "children": [
                    {
                        "title": "Sterile Tissue Harvest", "key": "101", "folder": true, "children": [
                            {"title": "Sterile Tissue Harvest", "key": "10101"},
                            {"title": "Diagnostic Necropsy and Tissue Harvest", "key": "10102"}
                        ]
                    },
                    {"title": "Tissue Cryopreservation", "key": "102"},
                    {"title": "Tissue Fixation", "key": "103"},
                    {"title": "Microtome Sectioning", "key": "104"},
                    {"title": "Cryostat Sectioning", "key": "105"},
                    {"title": "H&E staining", "key": "106"},
                    {"title": "Histochemistry", "key": "107"},
                    {"title": "Histoflouresence", "key": "108"}
                ]
            },
            {
                "title": "general lab", "key": "2", "folder": true, "children": [
                    {"title": "An Introduction to the Centrifuge", "key": "201"},
                    {"title": "Regulating Temperature in the Lab Preserving Sample Using Cold", "key": "202"},
                    {"title": "Introduction to the Bunsen Burner", "key": "203"},
                    {"title": "Introduction to Serological Pipettes and Pipettor", "key": "204"},
                    {"title": "An Introduction to the Micropipettor", "key": "205"},
                    {"title": "Making Solutions in the Laboratory", "key": "206"},
                    {"title": "Understanding Concentration and Measuring Volums", "key": "207"},
                    {"title": "Introduction to the Microplate Reader", "key": "208"},
                    {"title": "Regulation Temperature in the Lab Applying Heat", "key": "209"},
                    {"title": "Common Lab Glassware and Users", "key": "210"},
                    {"title": "Solutions and Concentrations", "key": "211"},
                    {"title": "Determining the Density of a Solid and Liquid", "key": "212"},
                    {"title": "Determining the Mass Percent Composition in an Aqueous Solution", "key": "213"},
                    {"title": "Determining the Empirical Formula", "key": "214"},
                    {"title": "Determining the Solubility Rules of Ionic Compounds", "key": "215"},
                    {"title": "Using a pH Meter", "key": "216"},
                    {"title": "Introduction to Titration", "key": "217"},
                    {"title": "Ideal Gas Law", "key": "218"}
                ]
            }
        ],
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

    /*
     */
    search_input(".search_message");
    if ($(window).width() < 575.98) {
        // toggle slide-bar => all views
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
});

function education_record() {
    var myForm = $('.ajax-sci-form');
    myForm.submit(function (event) {
        event.preventDefault();
        myForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
            .attr("disabled", "true");
        myForm.find("button[type='reset']").attr("disabled", "true");
        myForm.find("label").addClass("progress-cursor");
        myForm.closest(".fixed-back").find(".card").addClass("wait");
        var $thisURL = myForm.attr('data-url');
        var data = $(this).serialize();
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
                var obj = JSON.parse(data.responseText);
                console.log(data);
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

var executiveForm = $('.ajax-executive-form');
executiveForm.submit(function (event) {
    event.preventDefault();
    executiveForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    executiveForm.find("button[type='reset']").attr("disabled", "true");
    executiveForm.find("label").addClass("progress-cursor");
    executiveForm.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = executiveForm.attr('data-url');
    var data = $(this).serialize();
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
            var obj = JSON.parse(data.responseText);
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

var researchForm = $('.ajax-research-form');
researchForm.submit(function (event) {
    event.preventDefault();
    researchForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    researchForm.find("button[type='reset']").attr("disabled", "true");
    researchForm.find("label").addClass("progress-cursor");
    researchForm.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = researchForm.attr('data-url');
    var data = $(this).serialize();
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
            var obj = JSON.parse(data.responseText);
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

var paperForm = $('.ajax-paper-form');
paperForm.submit(function (event) {
    event.preventDefault();
    paperForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    paperForm.find("button[type='reset']").attr("disabled", "true");
    paperForm.find("label").addClass("progress-cursor");
    paperForm.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = paperForm.attr('data-url');
    var data = $(this).serialize();
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
            var obj = JSON.parse(data.responseText);
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

var showInfo = $('.chamran-btn-info');

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
        "                                    <div class='question'>" +
        "                                        <span class='question-mark'>" +
        "                                            <i class='far fa-question-circle'></i>" +
        "                                        </span>" +
        "جهت انجام پروژه خود به چه امکانات یا آزمایشگاه هایی احتیاج دارید؟" +
        "                                    </div>" +
        "                                    <div class='answer'>" +
        data.required_lab_equipment +
        "                                    </div>" +
        "                                </div>" +
        "<div>" +
        "                                    <div class='question'>" +
        "                                        <span class='question-mark'>" +
        "                                            <i class='far fa-question-circle'></i>" +
        "                                        </span>" +
        "جهت انجام پروژه خود به چه تخصص ها و چه تکنیک ها آزمایشگاهی ای احتیاج دارید؟" +
        "                                    </div>" +
        "                                    <div class='answer'>" +
        data.required_technique +
        "                                    </div>" +
        "                                </div>" +
        "<div>" +
        "                                    <div class='question'>" +
        "                                        <span class='question-mark'>" +
        "                                            <i class='far fa-question-circle'></i>" +
        "                                        </span>" +
        "لطفا مراحل انجام پروژه خود را مشخص کنید." +
        "                                    </div>" +
        "                                    <div class='answer'>" +
        data.project_phase +
        "                                    </div>" +
        "                                </div>" +
        "<div>" +
        "                                    <div class='question'>" +
        "                                        <span class='question-mark'>" +
        "                                            <i class='far fa-question-circle'></i>" +
        "                                        </span>" +
        "پروژه شما به چه مقدار بودجه نیاز دارد؟" +
        "                                    </div>" +
        "                                    <div class='answer'>" +
        data.required_budget +
        "                                    </div>" +
        "                                </div>";
    $(".project-info-content").html(resources);
}

function setApproach(data) {
    approach = "<div>" +
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
        data.predict_profit +
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

showInfo.click(function (event) {
    var id = "accept-project";
    var acceptButton = $('#accept-project');
    acceptButton.attr('id', $(this).attr('id'));
    $.ajax({
        url: $(this).attr('data-url'),
        data: {
            'id': $(this).attr("id")
        },
        dataType: 'json',
        success: function (data) {
            var dialog = $(".showProject");
            dialog.find(".card-head").html(data.project_title_persian + " (" + data.project_title_english + ")");
            dialog.find(".establish-time .time-body").html(data.date);
            dialog.find(".time-left .time-body").html(data.deadline);
            for (let i = 0; i < JSON.parse(data.key_words).length; i++) {
                dialog.find(".techniques").append(
                    "<span class='border-span'>" +
                    JSON.parse(data.key_words)[i].pk
                    + "</span>"
                );
            }
            setMajors(data);
            setValue(data);
        },
        error: function (data) {
            console.log(data)
        }

    })
});

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

var acceptProject = $('#accept-project');
acceptProject.click(function (event) {
    $.ajax({
        url: $(this).attr('data-url'),
        data: {
            'id': $(this).attr('id')
        },
        dataType: 'json',
        method: 'GET',
        success: function (data) {
            console.log(data)
        },
        error: function (data) {
            console.log(data)
        }
    })
});
