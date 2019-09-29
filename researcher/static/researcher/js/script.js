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
    input_focus();
    search_input(".search_message");
    question();
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

        education_record();
        executive_record();
        studious_record();

        $(".chamran_btn.technique").click(function () {
        $(".main").addClass("blur-div");
        $(".dialog-main").css("display","block");
        close_dialog('.technique-dialog-main');
      });
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