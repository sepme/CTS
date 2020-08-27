function load_dialog() {
    $(".title-back").each(function () {
        var title_back_width = $(this).prev().outerWidth() + 30;
        $(this).css("width", title_back_width);
    });
    $(".row-header > .header").each(function () {
        var divWidth = $(this).outerWidth();
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
            accept_project();
            $(dialogClass).removeAttr("id");
            $(dialogClass).attr("id", $(this).attr("id"));
        } else if (dialogClass === ".select-technique") {
            $(dialogClass).find("form").attr("id", $(element).closest(".fixed-back").attr("id"));
        }
    });
}

function showModal(dialogClass) {
    vote_dialog_init(dialogClass);
    $(".fixed-back").removeClass("show");
    $(".main").removeClass("blur-div");
    blur_div_toggle(".main");
    $(dialogClass).addClass("show");
    close_dialog(dialogClass);
    dialog_comment_init();
    load_dialog();
    if (dialogClass === ".showProject") {
        accept_project();
        $(dialogClass).removeAttr("id");
        $(dialogClass).attr("id", $(this).attr("id"));
    } else if (dialogClass === ".select-technique") {
        $(dialogClass).find("form").attr("id", $(element).closest(".fixed-back").attr("id"));
    }
}

function cancel_add(className) {
    div = "<span class='initial-value' style='border: 1px dashed #bdbdbd;width: fit-content;border-radius: 0.25em;padding: 5px 10px;font-size: 13px;font-weight: 300;'>برای افزودن سابقه جدید روی <i class='fas fa-plus'></i>  کلیک کنید!  </span>";
    $(".reject-btn").click(function () {
        if ($(className).html() === '') {
            $(className).append(div);
        }
    });
}

function accept_project() {
    $(".accept-btn").click(function () {
        $(".showProject").slideUp('slow').delay('slow');
        $(".project-details").delay('slow').slideDown('slow');
        close_dialog(".project-details");
        $('.add-researcher').hover(function () {
            $(this).addClass("hover");
        }, function () {
            $(this).removeClass("hover");
        });
        // vote_dialog_init();
        load_dialog();
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
        if ($(className).closest(".fixed-back").hasClass("show-question")) {
            $(className).find(".all-answers").html("");
            $(className).find(".question-attach").html('<ul class="inline-list">' +
                '<li class="list-item">' +
                '<a href="#" class="attach-file" dideo-checked="true">' +
                '<span class="attachment"></span>' +
                '<span class="attach-name">ضمیمه ای وجود ندارد</span>' +
                '</a>' +
                '</li>' +
                '</ul>');
        } else if (className === ".showProject") {
            $(".showProject .nav .nav-link").removeClass("active");
            $(".showProject .nav .nav-link#v-pills-majors-tab").addClass("active");
        } else if (className === ".researcher-info-dialog") {
            $('#researcher_scientific_record').html("<tr></tr>");
            $('#researcher_executive_record').html("<tr></tr>");
            $('#researcher_research_record').html("<tr></tr>");
        }
    });
}

function record_edit(className) {
    $(className + " .fa-pen").click(function () {
        if ($(className + " .ch-card-item").length === 0) {
            if (className === '.education') {
                var count = parseInt($(this).attr('id').replace('edit_edu_', ''));
                $(className).append(education_data_form(count));
                cancel_add(".education");
                $("#edu-section" + count).val($(this).closest('tr').children("td:nth-child(1)").text());
                $("#edu-subject" + count).val($(this).closest('tr').children("td:nth-child(2)").text());
                $("#university" + count).val($(this).closest('tr').children("td:nth-child(3)").text());
                $("#edu-city" + count).val($(this).closest('tr').children("td:nth-child(4)").text());
                $("#edu-year" + count).val($(this).closest('tr').children("td:nth-child(5)").text());
            } else if (className === '.executive') {
                var count = parseInt($(this).attr('id').replace('edit_exe_', ''));
                $(className).append(executive_data_form(count));
                cancel_add(".executive");
                $("#duty" + count).val($(this).closest('tr').children("td:nth-child(1)").text());
                $("#from" + count).val($(this).closest('tr').children("td:nth-child(2)").text());
                $("#until" + count).val($(this).closest('tr').children("td:nth-child(3)").text());
                $("#workplace" + count).val($(this).closest('tr').children("td:nth-child(4)").text());
                $("#exe-city" + count).vaal($(this).closest('tr').children("td:nth-child(5)").text());
            } else if (className === '.research') {
                var count = parseInt($(this).attr('id').replace('edit_stu_', ''));
                $(className).append(research_data_form(count));
                cancel_add(".research");
                $("#subject" + count).val($(this).closest('tr').children("td:nth-child(1)").text());
                $("#admin" + count).val($(this).closest('tr').children("td:nth-child(2)").text());
                $("#liable" + count).val($(this).closest('tr').children("td:nth-child(3)").text());
                $("#rank" + count).val($(this).closest('tr').children("td:nth-child(4)").text());
            } else if (className === '.paper') {
                var count = parseInt($(this).attr('id').replace('edit_art_', ''));
                $(className).append(paper_data_form(count));
                cancel_add(".paper");
                $("#paper-name" + art_count).val($(this).closest('tr').children("td:nth-child(1)").text());
                $("#publish-date" + art_count).val($(this).closest('tr').children("td:nth-child(2)").text());
                $("#published-at" + art_count).val($(this).closest('tr').children("td:nth-child(3)").text());
                $("#impact-factor" + art_count).val($(this).closest('tr').children("td:nth-child(4)").text());
                $("#referring-num" + art_count).val($(this).closest('tr').children("td:nth-child(5)").text());
            }
            input_focus();
        }
    });
    $(className + " .fa-trash-alt").click(function () {
        div = "<span class='initial-value' style='border: 1px dashed #bdbdbd;width: fit-content;border-radius: 0.25em;padding: 5px 10px;font-size: 13px;font-weight: 300;'>برای افزودن سابقه جدید روی <i class='fas fa-plus'></i>  کلیک کنید!  </span>";
        if (className === '.education') {
            var count = parseInt($(this).attr('id').replace('edit_edu_', ''));
            $(this).closest("tr").remove();
        } else if (className === '.executive') {
            var count = parseInt($(this).attr('id').replace('edit_exe_', ''));
            $(this).closest("tr").remove();
        } else if (className === '.research') {
            var count = parseInt($(this).attr('id').replace('edit_stu_', ''));
            $(this).closest("tr").remove();
        } else if (className === '.paper') {
            var count = parseInt($(this).attr('id').replace('edit_art_', ''));
            $(this).closest("tr").remove();
        }
        if ($(className + " > table > tbody > tr").length === 0) {
            $(className).html(div);
        }
    });
}

function sci_record_option() {
    $(".delete_sci").off("click ");
    $(".delete_sci").click(function () {
        let pk = $(this).attr("value");
        $.ajax({
            method: 'POST',
            url: "/expert/delete_scientific/",
            dataType: 'json',
            data: {pk: pk},
            success: function (data) {
                $(".row-sci-" + pk).remove();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت حذف شد!",
                    position: 'bottomLeft'
                });
            },
            error: function (data) {
                console.log(data);
            },
        });
    });
}

function exe_record_option() {
    $(".delete_exe").off();
    $(".delete_exe").click(function () {
        let pk = $(this).attr("value");
        $.ajax({
            method: 'POST',
            url: "/expert/delete_executive/",
            dataType: 'json',
            data: {pk: pk},
            success: function (data) {
                $(".row-exe-" + pk).remove();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت حذف شد!",
                    position: 'bottomLeft'
                });
            },
            error: function (data) {
                console.log(data);
            },
        });
    });
}

function research_record_option() {
    $(".delete_research").off();
    $(".delete_research").click(function () {
        let pk = $(this).attr("value");
        $.ajax({
            method: 'POST',
            url: "/expert/delete_research/",
            dataType: 'json',
            data: {pk: pk},
            success: function (data) {
                $(".row-research-" + pk).remove();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت حذف شد!",
                    position: 'bottomLeft'
                });
            },
            error: function (data) {
                console.log(data);
            },
        });
    });
}

function paper_record_option() {
    $(".delete_paper").off();
    $(".delete_paper").click(function () {
        let pk = $(this).attr("value");
        $.ajax({
            method: 'POST',
            url: "/expert/delete_paper/",
            dataType: 'json',
            data: {pk: pk},
            success: function (data) {
                $(".row-paper-" + pk).remove();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت حذف شد!",
                    position: 'bottomLeft'
                });
            },
            error: function (data) {
                console.log(data);
            },
        });
    });
}

function show_scientific_record(id) {
    if ($(".education table").length === 0) {
        let table = `
            <div class="res-table-container">
                <table class='table mtop-lg-25 text-center'>
                    <thead>
                    <tr>
                        <td scope="col">مقطع تحصیلی</td>
                        <td scope="col">رشته تحصیلی</td>
                        <td scope="col">دانشگاه</td>
                        <td scope="col">شهر محل تحصیل</td>
                        <td scope="col">سال اخذ مدرک</td>
                        <td scope="col"></td>
                    </tr>
                    </thead>
                        <tbody></tbody>
                </table>
            </div>
        `;
        $(".education").html(table);
    }

    let newRow = `
        <tr class="row-sci-${id}">
            <td>${$("#edu-section").val()}</td>
            <td>${$("#edu-subject").val()}</td>
            <td>${$("#university").val()}</td>
            <td>${$("#edu-city").val()}</td>
            <td>${$("#edu-year").val()}</td>
            <td>
                <i class='fas fa-trash-alt delete_sci'
                   value='${id}'></i>
            </td>
        </tr>
    `;
    $(".education table tbody").append(newRow);
    sci_record_option();
}

function show_executive_record(id) {
    if ($(".executive table").length === 0) {
        let table = `
            <div class="res-table-container">
                <table class='table mtop-lg-25 text-center'>
                    <thead>
                    <tr>
                        <td scope="col">سمت</td>
                        <td scope="col">از سال</td>
                        <td scope="col">تا سال</td>
                        <td scope="col">محل خدمت</td>
                        <td scope="col">شهر</td>
                        <td scope="col"></td>
                    </tr>
                    </thead>
                        <tbody></tbody>
                </table>
            </div>
        `;
        $(".executive").html(table);
    }

    let newRow = `
        <tr  class="row-exe-${id}">
            <td>${$("#duty").val()}</td>
            <td>${$("#from").val()}</td>
            <td>${$("#until").val()}</td>
            <td>${$("#workplace").val()}</td>
            <td>${$("#exe-city").val()}</td>
            <td>
                <i class='fas fa-trash-alt delete_exe'
                   value='${id}'></i>
            </td>
        </tr>
    `;

    $(".executive table tbody").append(newRow);
    exe_record_option();
}

function show_research_record(id) {
    if ($(".research table").length === 0) {
        let table = `
            <div class="res-table-container">
                <table class='table mtop-lg-25 text-center'>
                    <thead>
                    <tr>
                        <td scope="col">عنوان طرح پژوهشی</td>
                        <td scope="col">نام مجری</td>
                        <td scope="col">مسئول اجرا/همکار</td>
                        <td scope="col"></td>
                    </tr>
                    </thead>
                        <tbody></tbody>
                </table>
            </div>
        `;
        $(".research").html(table);
    }

    let newRow = `
        <tr class="row-research-${id}">
            <td>${$("#subject").val()}</td>
            <td>${$("#admin").val()}</td>
            <td>${$("#liable").val()}</td>
            <td>
                <i class='fas fa-trash-alt delete_research'
                   value='${id}'></i>
            </td>
        </tr>
    `;

    $(".research table tbody").append(newRow);
    research_record_option();
}

function show_paper_record(id) {
    if ($(".paper table").length === 0) {
        let table = `
            <div class="res-table-container">
                <table class='table mtop-lg-25 text-center'>
                    <thead>
                    <tr>
                        <td scope="col">عنوان مقاله</td>
                        <td scope="col">تاریخ انتشار</td>
                        <td scope="col">محل دقیق انتشار</td>
                        <td scope="col">Impact Factor</td>
                        <td scope="col">تعداد ارجاع به مقاله شما</td>
                        <td scope="col"></td>
                    </tr>
                    </thead>
                        <tbody></tbody>
                </table>
            </div>
        `;
        $(".paper").html(table);
    }

    let newRow = `
        <tr class="row-paper-${id}">
            <td>${$("#article-name").val()}</td>
            <td>${$("#publish-date").val()}</td>
            <td>${$("#published-at").val()}</td>
            <td>${$("#impact-factor").val()}</td>
            <td>${$("#referring-num").val()}</td>
            <td>
                <i class='fas fa-trash-alt delete_paper'
                   value='${id}'></i>
            </td>
        </tr>
    `;

    $(".paper table tbody").append(newRow);
    paper_record_option();
}

function show_new_research_question(pk) {
    if ($(".empty-page").length !== 0) {
        let container = `
            <div class="col-lg-12 text-right">
                <div class="project-info-tabs">
                    <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist"
                         aria-orientation="vertical">
                        <a class="nav-link active fs-15" id="all-questions" data-toggle="pill"
                           role="tab" aria-selected="true">
                            همه
                        </a>
                        <a class="nav-link fs-15" id="active-questions" data-toggle="pill"
                           role="tab" aria-selected="false">
                            فعال
                        </a>
                        <a class="nav-link fs-15" id="check-questions" data-toggle="pill"
                           role="tab" aria-selected="false">
                            درحال بررسی
                        </a>
                        <a class="nav-link fs-15" id="answered-questions" data-toggle="pill"
                           role="tab" aria-selected="false">
                            پاسخ داده شده
                        </a>
                    </div>
                </div>
                <div class="tab-content cover-page"></div>
            </div>
        `;
        $(".empty-page").closest(".row").html(container);
        $(".h3").removeClass("border-bottom");
    }
    let new_question = `
        <div class="card check-question box flow-root-display w-100">
            <div class="box-header">
                <h6>${$("#question-title").val()}</h6>
                <span class="check-status"></span>       
            </div>
            <div class="box-body">
                <div class="row">
                    <div class="col-md-6 col-9">
                        <div class="row">
                            <div class="col-6">
                                <div class="date text-center">
                                    <div class="label">زمان ثبت</div>
                                    <div class="value">
                                        <span>چند لحظه</span>
                                        <span>قبل</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="answers text-center">
                                    <div class="label">پاسخ های جدید</div>
                                    <div class="value">
                                        <span>0</span>
                                        <span></span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 col-3">
                        <button class="default-btn show-btn" id="${pk}" data-toggle="modal" data-target="#showQuestion">
                            مشاهده
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    $(".tab-content").append(new_question);
}

function dialog_comment_init() {
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
    // $(".new-comment-tools > label[for='comment-attach']").click(function () {
    //     let rows = $("textarea#comment").attr("rows");
    //     $("textarea#comment").attr("rows", ++rows);
    //     let padding_bottom = parseInt($("textarea#comment").css("padding-bottom")) + 30;
    //     $("textarea#comment").css("padding-bottom", padding_bottom);
    //
    //     if ($("div.attachment > div").last().hasClass("attach")) {
    //         let bottom_position = parseInt($("div.attachment > div").last().css("bottom"));
    //     } else {
    //         let bottom_position = 10;
    //     }
    //
    //     // $("div.attachment").append("<div class='attach'>" +
    //     //     "<span>" + "نام فایل" + "</span>" +
    //     //     "<div class='progress'>" +
    //     //     "<div class='progress-bar progress-bar-striped progress-bar-animated' role='progressbar' aria-valuenow='75' aria-valuemin='0' aria-valuemax='100' style='width: 75%'></div>" +
    //     //     "</div>" +
    //     //     "</div>");
    //     // $("div.attachment > div").last().css("bottom", bottom_position + 30);
    // });
    // replay to a comment
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
    // edit user comment
    // $(".comment-tools > .fa-pen").click(function () {
    //     text = $.trim($(this).closest("div").children(2).text());
    //     $("textarea#comment").html(text);
    //     $("textarea#comment").focus();
    // });
}

function vote_slider_industry(slide_count) {
    let industry_counter = 0;
    $(".industry-voting .next-button").click(function () {
        alert("industry_counter = " + industry_counter);
        if (industry_counter < slide_count - 1) {
            industry_counter++;
            let progressWidth = parseInt($(".industry-voting .vote-list > .vote-item").css('width'));
            let width = parseFloat($(".industry-voting .progress-line").css('width'));
            $(".industry-voting .progress-line").css('width', width + progressWidth);
            $(".industry-voting .swiper-wrapper").css({
                "transform": "translate3d(-" + 100 * industry_counter + "%, 0, 0)",
                "transition-duration": "0.3s"
            });
        }
        if (industry_counter === slide_count - 1) {
            $(this).html("<i class='fas fa-check'></i>" +
                "ثبت");
        }
        if (industry_counter > 0) {
            $(".industry-voting .prev-button").removeClass("disabled");
        }
    });
    $(".industry-voting .prev-button").click(function () {
        alert("industry_counter = " + industry_counter);
        if (industry_counter > 0) {
            industry_counter--;
            let progressWidth = parseInt($(".industry-voting .vote-list > .vote-item").css('width'));
            let width = parseFloat($(".industry-voting .progress-line").css('width'));
            $(".industry-voting .progress-line").css('width', width - progressWidth);
            $(".industry-voting .swiper-wrapper").css({
                "transform": "translate3d(-" + 100 * industry_counter + "%, 0, 0)",
                "transition-duration": "0.3s"
            });
        }
        if (industry_counter === slide_count - 2) {
            $(".industry-voting .next-button").html("<i class='fas fa-arrow-right'></i>" +
                "بعدی");
        }
        if (industry_counter === 0) {
            $(this).addClass('disabled');
        }
    });
}

function vote_slider_researcher(slide_count) {
    let researcher_counter = 0;
    $(".researcher-voting .next-button").click(function () {
        alert("researcher_counter = " + researcher_counter);
        if (researcher_counter < slide_count - 1) {
            researcher_counter++;
            let progressWidth = parseInt($(".researcher-voting .vote-list > .vote-item").css('width'));
            let width = parseFloat($(".researcher-voting .progress-line").css('width'));
            $(".researcher-voting .progress-line").css('width', width + progressWidth);
            $(".researcher-voting .swiper-wrapper").css({
                "transform": "translate3d(-" + 100 * researcher_counter + "%, 0, 0)",
                "transition-duration": "0.3s"
            });
        }
        if (researcher_counter === slide_count - 1) {
            $(this).html("<i class='fas fa-check'></i>" +
                "ثبت");
        }
        if (researcher_counter > 0) {
            $(".researcher-voting .prev-button").removeClass("disabled");
        }
    });
    $(".researcher-voting .prev-button").click(function () {
        alert("researcher_counter = " + researcher_counter);
        if (researcher_counter > 0) {
            researcher_counter--;
            let progressWidth = parseInt($(".researcher-voting .vote-list > .vote-item").css('width'));
            let width = parseFloat($(".researcher-voting .progress-line").css('width'));
            $(".researcher-voting .progress-line").css('width', width - progressWidth);
            $(".researcher-voting .swiper-wrapper").css({
                "transform": "translate3d(-" + 100 * researcher_counter + "%, 0, 0)",
                "transition-duration": "0.3s"
            });
        }
        if (researcher_counter === slide_count - 2) {
            $(".researcher-voting .next-button").html("<i class='fas fa-arrow-right'></i>" +
                "بعدی");
        }
        if (researcher_counter === 0) {
            $(this).addClass('disabled');
        }
    });
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
            console.log("expand on");
            $('.vote-dialog').slideDown();
            $('.vote').addClass('expand');
        } else {
            console.log("expand off");
            $('.vote-dialog').slideUp();
            $('.vote').removeClass('expand');
        }
    });
    $(".vote-dialog > .industry-back").hover(function () {
        $(this).addClass('hover');
    }, function () {
        $(this).removeClass('hover');
    }).click(function () {
        $(".project-details").slideUp('slow').delay('slow');
        $(".industry-voting").delay('slow').slideDown('slow');
        close_dialog('.industry-voting');
        vote_slider_industry(12);
        $(".progress-line").css("width", "calc(100% / 12)");
    });
    $(".vote-dialog > .researcher-back").hover(function () {
        $(this).addClass('hover');
    }, function () {
        $(this).removeClass('hover');
    }).click(function () {
        $(".project-details").slideUp('slow').delay('slow');
        $(".researcher-voting").delay('delay').slideDown('slow');
        close_dialog('.researcher-voting');
        vote_slider_researcher(10);
        $(".progress-line").css("width", "calc(100% / 10)");
    });
}

function question_page_init() {

}

function question_dialog_init() {
    // $(".answer").hover(function () {
    //     if (!$(this).find('button').hasClass('answered')) {
    //         $(this).find('.correct button').fadeIn('slow');
    //         $(this).find(".wrong button").fadeIn('slow');
    //     }
    // }, function () {
    //     if (!$(this).find('button').hasClass('answered')) {
    //         $(this).find('.correct button').fadeOut('slow');
    //         $(this).find(".wrong button").fadeOut('slow');
    //     }
    // });
    $(".answer .check .correct button").click(function () {
        // $(this).closest(".check").find(".wrong button").css("visibility", "hidden");
        // $(this).closest(".check").find(".wrong button").css("max-width", "0");
        //
        // $(this).closest(".check").find(".wrong").css("max-width", "0");
        $(this).closest(".check").addClass("loading").css("display", "block");
        $(this).closest(".check").find("button").attr("disabled", "true");
        let This = $(this);
        let id = $(this).attr("id");
        $.ajax({
            method: 'GET',
            url: '/expert/set_answer_situation/',
            dataType: 'json',
            data: {id: id, type: true},
            success: function (data) {
                This.closest(".check").removeClass("loading").addClass("correct-ans");
                This.closest(".check").find("loading");
                This.closest(".check").find(".wrong").remove();
                This.closest(".answer").attr("is-correct", "true");
                set_answer_true(This);
                iziToast.success({
                    rtl: true,
                    message: "وضعیت صحیح برای پاسخ ذخیره شد.",
                    position: 'bottomLeft'
                });
            },
            error: function (data) {
            },
        });
    });
    $(".answer .check .wrong button").click(function () {
        $(this).closest(".check").addClass("loading").css("display", "block");
        $(this).closest(".check").find("button").attr("disabled", "true");
        let This = $(this);
        let id = $(this).attr("id");
        $.ajax({
            method: 'GET',
            url: '/expert/set_answer_situation/',
            dataType: 'json',
            data: {id: id, type: false},
            success: function (data) {
                This.closest(".check").removeClass("loading");
                set_answer_wrong(This);
                iziToast.success({
                    rtl: true,
                    message: "وضعیت نادرست برای پاسخ ذخیره شد.",
                    position: 'bottomLeft'
                });
            },
            error: function (data) {
            },
        });
    });


    $(".question-attach input[type='file']").on('change', function () {
        console.log("attach");
        let fileType = $(this).val().split('.').pop().toLowerCase();
        let fileName = $(this).val().split('\\').pop();
        $(this).closest(".list-item").find(".attach-btn label span:last-child").html(fileName);
        $(this).closest(".list-item").find(".attach-btn label span.attach-icon").removeClass("attach-icon").addClass(fileType + "-file");
        // attach_li = "<li class='list-item'>" +
        //     "<a href='#' class='attach-file'>" +
        //     "<span class='" + fileType + "-file'></span>" +
        //     "<span dir='ltr'>" + fileName + "</span>" +
        //     "</a>" +
        //     "</li>";
        // $(this).closest('ul.inline-list').append(attach_li);
    });
}

function set_answer_wrong(item) {
    let div = "<span>پاسخ نادرست</span><i class='fas fa-times'></i>";
    item.closest('.answer').addClass("answered");
    item.closest('.check').find('.status').addClass('wrong-answer');
    item.closest('.check').find('.status').append(div);
    item.closest('.check').find('.status').fadeIn('slow');
    item.closest('.check').find("button").remove();
}

function set_answer_true(item) {
    let div = "<span>پاسخ صحیح</span><i class='fas fa-check'></i>";
    item.closest('.answer').addClass("answered");
    item.closest('.check').find('.status').addClass('correct-answer');
    item.closest('.check').find('.status').append(div);
    item.closest('.check').find('.status').fadeIn('slow');
    item.closest('.check').find("button").remove();
}

function returnFileType(type) {
    type = type.toLowerCase();
    if (type === "pdf" || type === "doc" || type === "gif" || type === "jpg" || type === "png"
        || type === "ppt" || type === "txt" || type === "wmv" || type === "zip") {
        return type;
    } else if (type === "jpeg")
        return "jpg";
    return "unknown";
}

function show_question_answers(data) {
    let answer = '';
    for (let i = 0; i < data.length; i++) {
        let file_type = data[i].answer_attachment.substring(data[i].answer_attachment.lastIndexOf(".") + 1).toUpperCase();
        let divider_line = "";
        if (i) {
            divider_line = "divider-top";
        }
        answer = answer +
            '<div class="col-lg-12 mbottom-10">' +
            '   <div class="answer ' + divider_line;
        if (data[i].is_correct !== "not_seen") {
            answer = answer + ' answered';
        }
        answer = answer +
            '" is-correct="' + data[i].is_correct + '">' +
            '       <span class="title">' + data[i].researcher_name + '</span>' +
            '       <span class="date">' + data[i].hand_out_date + '</span>' +
            '       <div class="answer-body">' +
            '           <span class="file-type image ' + returnFileType(file_type) + '"></span>' +
            '           <div class="file-name">' + data[i].file_name.substring(0, data[i].file_name.lastIndexOf(".")) + '</div>' +
            '           <span class="file-type text">' + file_type + ' File</span>' +
            '           <a href="' + data[i].answer_attachment + '" class="download">' +
            '               <i class="fas fa-download"></i>' +
            '           </a>' +
            '       </div>' +
            '       <div class="check">' +
            '           <span class="wait-load"></span>';
        if (data[i].is_correct === "not_seen") {
            answer = answer +
                '           <div class="correct">' +
                '               <button type="button" title="صحیح" id="' + data[i].answer_id + '">' +
                '                   <i class="fas fa-check"></i>' +
                '                   <span>درست</span>' +
                '               </button>' +
                '           </div>' +
                '           <div class="wrong">' +
                '               <button type="button" title="نادرست" id="' + data[i].answer_id + '">' +
                '                   <i class="fas fa-times"></i>' +
                '                   <span>نادرست</span>' +
                '               </button>' +
                '           </div>';
        }
        if (data[i].is_correct === "correct") {
            answer = answer +
                '           <div class="status correct-answer" style="display: block ruby;">' +
                '               <span>پاسخ صحیح</span>' +
                '               <i class="fas fa-check"></i>' +
                '           </div>';
        } else if (data[i].is_correct === "wrong") {
            answer = answer +
                '           <div class="status wrong-answer" style="display: block ruby;">' +
                '               <span>پاسخ نادرست</span>' +
                '               <i class="fas fa-times"></i>' +
                '           </div>';
        } else {
            answer = answer +
                '           <div class="status" style="display: block;"></div>';
        }
        answer = answer +
            '       </div>' +
            '   </div>' +
            '</div>';
    }
    $(".all-answers").html(answer);
    // $(".answer").each(function () {
    //     let is_correct = $(this).attr("is-correct");
    //     if (is_correct === 'correct') {
    //         set_answer_true($(this).find(".check").find(".correct").find("button"))
    //     } else if (is_correct === 'wrong') {
    //         set_answer_wrong($(this).find(".check").find(".correct").find("button"))
    //     }
    // });
}

function select_technique(className) {
    // $("li[role='treeitem']").click(function () {
    //     var tree = $("#fancy-tree").fancytree({
    //         activate: function (event, data) {
    //             node = data.node;
    //             $("input#technique-name").val(node.title);
    //             express();
    //             input_focus();
    //     }
    //});
    // $("li[role='treeitem']").click(function () {
    //     console.log("click");
    //     let tree = $("#fancy-tree").fancytree({
    //
    //     });
    // });
    $("#add-new-technique").keyup(function (e) {
        console.log($(this).val());
        console.log(e);
        if (e.keyCode === 13) {
            if ($(this).val() !== "") {
                $('#tags').addTag($(this).val());
                $(this).val("");
            }
        }
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
    $("#tags_tagsinput").find("#tags_tag").attr("placeholder", "افزودن");
    tag_input_label("tags");
}

function setComment(data, parent) {
    let comments_code = "";
    console.log(data);
    for (let i = 0; i < data.length; i++) {
        if (data[i].sender_type === "expert") { //expert
            let comment_body_classes = "comment-body";
            if (data[i].attachment !== "None") {
                comment_body_classes += " attached";
            }
            comments_code += "<div class='my-comment' id='" + data[i].pk + "' >" +
                "   <div class='comment-profile'></div>" +
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
                "           </span>" +
                "       <div class='" + comment_body_classes + "'>" +
                "<pre>" + data[i].text + "</pre>";
            if (data[i].attachment !== "None") {
                comments_code += "<a href='" + data[i].attachment + "' class='attached-file'>" +
                    "   <i class='fas fa-paperclip'></i>" +
                    "   <span>" + data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1) + "</span>" +
                    "</a>";
            }
            comments_code += "" +
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
                "       </span>" +
                "<pre>" + data[i].text + "</pre>";
            if (data[i].attachment !== "None") {
                comments_code += "<a href='" + data[i].attachment + "' class='attached-file'>" +
                    "   <i class='fas fa-paperclip'></i>" +
                    "   <span>" + data[i].attachment.substring(data[i].attachment.lastIndexOf("/") + 1) + "</span>" +
                    "</a>";
            }
            comments_code += "" +
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
    if (comments_code === "") {
        parent.find(".no-comment").addClass("show");
    }
    parent.find('.comments').html(comments_code).animate({scrollTop: parent.find('.comments').prop("scrollHeight")}, 1000);

    parent.find(".comments .fa-trash-alt").closest(".dropdown-item").click(function () {
        deleteComment($(this).closest('.my-comment'));
    });
    dialog_comment_init(parent);
}