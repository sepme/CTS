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
    art_count = 0;
    $('*').persiaNumber();
    input_focus();
    init_dialog_btn(".chamran-btn-info" , ".showProject");
    init_dialog_btn(".message-body button, .message-body-sm button" , ".message-show");
    search_input(".search_message");
    if($(window).width() < 575.98){
    // toggle slide-bar => all views
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
    // nav-tabs change => index view
        $(".nav-link").click(function () {
           $(".nav-link").removeClass("active");
           $(this).addClass("active");
           $(".nav").animate({
               scrollLeft: $(this).offset().left
           }, "slow");
        });

    }else{
        // loading();
        $(function () {
            $('[data-toggle="tooltip"]').tooltip();
        });
        init_windowSize();
        init_dialog_btn(".researcher-card-button-show" , ".researcher-info-dialog");
        // if($(".mainInfo-body").css("display") === "block"){
        //     blur_div_toggle(".top-bar");
        //     blur_div_toggle(".side-bar");
        // }
      $(".form-submit").click(function () {
        blur_div_toggle(".top-bar");
        blur_div_toggle(".side-bar");
        $(".mainInfo-body").css("display","none");
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
        $("img.profile").fadeIn("fast").attr('src',URL.createObjectURL(event.target.files[0]));
      });
      education_record();
      executive_record();
      studious_record();
      article_record();
      $(".chamran_btn.technique").click(function () {
        $(".main").addClass("blur-div");
        $(".dialog-main").css("display","block");
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
          if(!$(this).hasClass("active")){
              $("ul#project-list li a").removeClass("active");
              $(this).addClass("active");
          }
      });
    }
});