$(window).on("load",function () {
    init_windowSize();
    load_dialog();
}).on("resize",function () {
    init_windowSize();
    load_dialog();
});
$(document).ready(function(){
    // variable
    edu_count = 0;
    exe_count = 0;
    stu_count = 0;
    init_dialog_btn(".message-body button, .message-body-sm button" , ".message-show");
    init_dialog_btn(".add-new-technique", ".add-technique");
    init_dialog_btn(".new-review-request", ".review-request");
    init_dialog_btn(".send-answer", ".thanks_response");
    init_dialog_btn(".start-question", ".confirmation");
    select_technique(".select-technique");
    init_dialog_btn(".education-btn", ".scientific_form");
    init_dialog_btn(".executive-btn", ".executive_form");
    init_dialog_btn(".research-btn", ".research_form");
    init_dialog_btn(".technique", ".technique-dialog-main");
    input_focus();
    search_input(".search_message");
    question();
    $('input#upload-input').change(function (event) {
        $("img.profile").fadeIn("fast").attr('src',URL.createObjectURL(event.target.files[0]));
    });
    if($(window).width() < 575.98){
        $(".main").removeClass("blur-div");
        $("#toggle").click(function () {
           if($(this).hasClass("on")){
               $(this).removeClass("on");
               $(".side-bar").css("right","-500px");
               $(".content").removeClass("blur-div");
           } else {
               $(this).addClass("on");
               $(".side-bar").css("right","0");
               $(".content").addClass("blur-div");
           }
        });
    }else{
        init_windowSize();
        init_dialog_btn(".chamran-btn-info" , ".showProject");
        $(".form-submit").click(function () {
            blur_div_toggle(".top-bar");
            blur_div_toggle(".side-bar");
            $(".mainInfo-body").css("display","none");
        });

        // education_record();
        // executive_record();
        // studious_record();

        $(".technique-list-item").click(function () {
        $(this).toggleClass("active");
        $(this).children("span").children(".fa-chevron-left").toggleClass("rotate--90");
        $(this).children(".sub-technique-list").toggleClass("display-toggle");
      });
        $("ul#project-list li a").click(function () {
          if(!$(this).hasClass("active")){
              $("ul#project-list li a").removeClass("active");
              $(this).addClass("active");
          }
      });
    }
});

// function executive_record() {
//     var form = $('.ajax-exe-form');
//     form.submit(function (event) {
//         event.preventDefault();
//         form.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
//             .attr("disabled", "true");
//         form.find("button[type='reset']").attr("disabled", "true");
//         form.find("label").addClass("progress-cursor");
//         form.closest(".fixed-back").find(".card").addClass("wait");
//         form.find("input").attr("disabled", "true").addClass("progress-cursor");

//         $.ajax({
//             method: 'POST',
//             url: form.attr('url'),
//             dataType: 'json',
//             data: form.serialize(),
//             success: function (data) {
//                 console.log("++++++++")
//                 console.log(data)
//                 form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
//                     .prop("disabled", false);
//                 form.find("button[type='reset']").prop("disabled", false);
//                 form.find("input").prop("disabled", false).removeClass("progress-cursor");
//                 form.find("label").removeClass("progress-cursor");
//                 form.closest(".fixed-back").find(".card").removeClass("wait");
//                 if (data.success === "successful") {
//                     $(".ajax-exe-form").css("display", "none");
//                     $(".main").removeClass("blur-div");
//                     // show_scientific_record();
//                     iziToast.success({
//                         rtl: true,
//                         message: "اطلاعات با موفقیت ذخیره شد!",
//                         position: 'bottomLeft'
//                     });
//                     form[0].reset();
//                 }
//             },
//             error: function (data) {
//                 console.log("-----------")
//                 console.log(data)
//                 var obj = JSON.parse(data.responseText);
//                 form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
//                     .prop("disabled", false);
//                 form.find("button[type='reset']").prop("disabled", false);
//                 form.find("input").prop("disabled", false).removeClass("progress-cursor");
//                 form.find("label").removeClass("progress-cursor");
//                 form.closest(".fixed-back").find(".card").removeClass("wait");
//                 if (obj.post) {
//                     console.log(obj.post)
//                     $("#duty").closest("div").append("<div class='error'>" +
//                         "<span class='error-body'>" +
//                         "<ul class='errorlist'>" +
//                         "<li>" + obj.post + "</li>" +
//                         "</ul>" +
//                         "</span>" +
//                         "</div>");
//                     $("input#duty").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
//                 }
//                 if (obj.start) {
//                     console.log(obj.start)
//                     $("#from").closest("div").append("<div class='error'>" +
//                         "<span class='error-body'>" +
//                         "<ul class='errorlist'>" +
//                         "<li>" + obj.start + "</li>" +
//                         "</ul>" +
//                         "</span>" +
//                         "</div>");
//                     $("input#from").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
//                 }
//                 if (obj.end) {
//                     console.log(obj.end);
//                     $("#until").closest("div").append("<div class='error'>" +
//                         "<span class='error-body'>" +
//                         "<ul class='errorlist'>" +
//                         "<li>" + obj.end + "</li>" +
//                         "</ul>" +
//                         "</span>" +
//                         "</div>");
//                     $("input#until").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
//                 }
//                 if (obj.place) {
//                     console.log(obj.place);
//                     $("#workplace").closest("div").append("<div class='error'>" +
//                         "<span class='error-body'>" +
//                         "<ul class='errorlist'>" +
//                         "<li>" + obj.place + "</li>" +
//                         "</ul>" +
//                         "</span>" +
//                         "</div>");
//                     $("input#workplace").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
//                 }
//                 if (obj.city) {
//                     $("#exe-city").closest("div").append("<div class='error'>" +
//                         "<span class='error-body'>" +
//                         "<ul class='errorlist'>" +
//                         "<li>" + obj.city + "</li>" +
//                         "</ul>" +
//                         "</span>" +
//                         "</div>");
//                     $("input#exe-city").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
//                 }
//             },
//         })
//     })
// }

var scientificForm = $('#ajax-sci-form');
scientificForm.submit(function (event) {
    event.preventDefault();
    scientificForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    scientificForm.find("button[type='reset']").attr("disabled", "true");
    scientificForm.find("label").addClass("progress-cursor");
    scientificForm.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = scientificForm.attr('url');
    var data = $(this).serialize();
    scientificForm.find("input").attr("disabled", "true").addClass("progress-cursor");
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
                $("#ajax-sci-form").css("display", "none");
                $(".main").removeClass("blur-div");
                show_research_record();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                scientificForm[0].reset();
            }
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            console.log(obj);
            scientificForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            scientificForm.find("button[type='reset']").prop("disabled", false);
            scientificForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            scientificForm.find("label").removeClass("progress-cursor");
            scientificForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.grade) {
                $("#edu-section").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.grade + "</li>" +
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
            if (obj.place) {
                $("#edu-city").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.place + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#edu-city").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.graduated_year) {
                $("#year").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.graduated_year + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#year").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
        },
    })
});

var researchForm = $('.ajax-std-form');
researchForm.submit(function (event) {
    event.preventDefault();
    researchForm.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    researchForm.find("button[type='reset']").attr("disabled", "true");
    researchForm.find("label").addClass("progress-cursor");
    researchForm.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = researchForm.attr('url');
    var data = $(this).serialize();
    researchForm.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        success: function (data) {
            researchForm.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            researchForm.find("button[type='reset']").prop("disabled", false);
            researchForm.find("input").prop("disabled", false).removeClass("progress-cursor");
            researchForm.find("label").removeClass("progress-cursor");
            researchForm.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".ajax-std-form").css("display", "none");
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
            if (obj.responsible) {
                $("#liable").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.responsible + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#liable").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.title) {
                $("#subject").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.title + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#subject").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.presenter) {
                $("#admin").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.presenter + "</li>" +
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

var executive_form = $('.ajax-exe-form');
executive_form.submit(function (event) {
    event.preventDefault();
    executive_form.find("button[type='submit']").addClass("loading-btn").attr("disabled", "true").css("color", "transparent");
    executive_form.find("button[type='reset']").attr("disabled", "true");
    executive_form.find("label").addClass("progress-cursor");
    executive_form.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = executive_form.attr('url');
    var data = $(this).serialize();
    executive_form.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        success: function (data) {
            executive_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            executive_form.find("button[type='reset']").prop("disabled", false);
            executive_form.find("input").prop("disabled", false).removeClass("progress-cursor");
            executive_form.find("label").removeClass("progress-cursor");
            executive_form.closest(".fixed-back").find(".card").removeClass("wait");
            if (data.success === "successful") {
                $(".ajax-exe-form").css("display", "none");
                $(".main").removeClass("blur-div");
                show_research_record();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
                executive_form[0].reset();
            }
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            executive_form.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            executive_form.find("button[type='reset']").prop("disabled", false);
            executive_form.find("input").prop("disabled", false).removeClass("progress-cursor");
            executive_form.find("label").removeClass("progress-cursor");
            executive_form.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.post) {
                $("#duty").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.post + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#duty").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.start) {
                $("#from").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.start + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#from").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.end) {
                $("#until").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.end + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#until").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
            if (obj.place) {
                $("#workplace").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.place + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
                $("input#workplace").addClass("error").css("color", "rgb(255, 69, 69)").prev().css("color", "rgb(255, 69, 69)");
            }
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
        },
    })
});

var technique_review = $('#technique_review');
technique_review.submit(function (event) {
    event.preventDefault();
    technique_review.find("button[type='submit']").css("color", "transparent").addClass("loading-btn")
        .attr("disabled", "true");
    technique_review.find("button[type='reset']").attr("disabled", "true");
    technique_review.find("label").addClass("progress-cursor");
    technique_review.closest(".fixed-back").find(".card").addClass("wait");
    var $thisURL = technique_review.attr('url');
    var data = $(this).serialize();
    technique_review.find("input").attr("disabled", "true").addClass("progress-cursor");
    $.ajax({
        method: 'POST',
        url: $thisURL,
        dataType: 'json',
        data: data,
        success: function (data) {
            technique_review.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            technique_review.find("button[type='reset']").prop("disabled", false);
            technique_review.find("input").prop("disabled", false).removeClass("progress-cursor");
            technique_review.find("label").removeClass("progress-cursor");
            technique_review.closest(".fixed-back").find(".card").removeClass("wait");
            
            if (data.success === "successful") {
                $("#technique_review").css("display", "none");
                $(".main").removeClass("blur-div");
                show_research_record();
                iziToast.success({
                    rtl: true,
                    message: "اطلاعات با موفقیت ذخیره شد!",
                    position: 'bottomLeft'
                });
            }
        },
        error: function (data) {
            var obj = JSON.parse(data.responseText);
            technique_review.find("button[type='submit']").css("color", "#ffffff").removeClass("loading-btn")
                .prop("disabled", false);
            technique_review.find("button[type='reset']").prop("disabled", false);
            technique_review.find("input").prop("disabled", false).removeClass("progress-cursor");
            technique_review.find("label").removeClass("progress-cursor");
            technique_review.closest(".fixed-back").find(".card").removeClass("wait");
            if (obj.resume) {
                $("#upload-new-resume").closest("div").append("<div class='error'>" +
                    "<span class='error-body'>" +
                    "<ul class='errorlist'>" +
                    "<li>" + obj.resume + "</li>" +
                    "</ul>" +
                    "</span>" +
                    "</div>");
            }
        }
    })
})
