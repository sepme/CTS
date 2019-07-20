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
      $(".education-btn > i.fa-plus").click(function (){
        div = document.createElement("div");
        $(div).addClass('card').addClass('ch-card-item');
        $(div).attr("id",edu_count);
        $(div).html("<form action='' method='post'><div class='row'>" +
            "<div class='col-lg-6'>" +
              "<label for=\"edu-section"+edu_count+"\">مقطع تحصیلی</label>\n" +
              "<input type=\"text\" id=\"edu-section"+edu_count+"\" class=\"w-100\">" +
            "</div>" +
            "<div class='col-lg-6'>" +
              "<label for=\"edu-subject"+edu_count+"\">رشته تحصیلی</label>\n" +
              "<input type=\"text\" id=\"edu-subject"+edu_count+"\" class=\"w-100\">" +
            "</div>" +
            "</div>"+
            "</div>" +
            "<div class='row'>" +
            "<div class='col-lg-5'>" +
              "<label for=\"university"+edu_count+"\">دانشگاه</label>\n" +
              "<input type=\"text\" id=\"university"+edu_count+"\" class=\"w-100\">" +
            "</div>" +
            "<div class='col-lg-4'>" +
              "<label for=\"edu-city"+edu_count+"\">شهر محل تحصیل</label>\n" +
              "<input type=\"text\" id=\"edu-city"+edu_count+"\" class=\"w-100\">" +
            "</div>" +
            "<div class='col-lg-3'>" +
              "<label for=\"year"+edu_count+"\">سال اخذ مدرک</label>\n" +
              "<input type=\"text\" id=\"year"+edu_count+"\" class=\"w-100\">" +
            "</div>" +
            "</div>" +
            "<div class='row mtop-lg-25'>" +
                "<div class='col-lg-9'>" +
                    "<button type='button' id='"+edu_count+"' class='w-100 accept-btn btn'>افزودن</button>" +
                "</div>"+
                "<div class='col-lg-3'>" +
                    "<button type='button' id='"+edu_count+"' class='w-100 refuse-btn btn'>لغو</button>" +
                "</div>" +
            "</div></form>");
        if($(".education > .initial-value").hasClass("initial-value")) {
            $(".education").html(div);
        }else {
            $('.education').append(div);
        }
        delete_item(".education");
        input_focus();
        edu_count ++;
      });
      $(".executive-btn > i.fa-plus").click(function () {
        div = document.createElement("div");
        $(div).addClass('card').addClass('ch-card-item');
        $(div).attr("id",exe_count);
        $(div).html("<form action='' method='post'><div class='row'>" +
              "<div class='col-lg-5'>" +
                "<label for='duty"+ exe_count +"'>سمت</label>" +
                "<input type='text' id='duty"+ exe_count +"' class='w-100'>" +
              "</div>"+
              "<div class='col-lg-1'>" +
                "<span class='center-vr'>زمان :</span>" +
              "</div>" +
              "<div class='col-lg-3'>" +
                "<label for='from"+ exe_count +"'>از تاریخ</label>" +
                "<input type='text' id='from"+ exe_count +"' class='w-100'>" +
              "</div>" +
              "<div class='col-lg-3'>" +
                "<label for='until"+ exe_count +"'>تا تاریخ</label>" +
                "<input type='text' id='until"+ exe_count +"' class='w-100'>" +
              "</div>" +
            "</div>"+
            "<div class='row'>" +
              "<div class='col-lg-5'>" +
                "<label for='workplace"+ exe_count +"'>محل خدمت</label>" +
                "<input type='text' id='workplace"+ exe_count +"' class='w-100'>" +
              "</div>"+
              "<div class='col-lg-4'>" +
                "<label for='exe-city"+ exe_count +"'>شهر</label>" +
                "<input type='text' id='exe-city"+ exe_count +"' class='w-100'>" +
              "</div>"+
              "<div class='col-lg-3'></div>" +
            "</div>" +
            "<div class='row mtop-lg-25'>" +
                "<div class='col-lg-9'>" +
                    "<button type='button' id='"+exe_count+"' class='w-100 accept-btn btn'>افزودن</button>" +
                "</div>"+
                "<div class='col-lg-3'>" +
                    "<button type='button' id='"+exe_count+"' class='w-100 refuse-btn btn'>لغو</button>" +
                "</div>" +
            "</div></form>");
        if($(".executive > .initial-value").hasClass("initial-value")){
            $(".executive").html(div);
        }else {
            $('.executive').append(div);
        }
        delete_item(".executive");
        input_focus();
        $("#from"+ exe_count).persianDatepicker({

        });
        $("#until"+ exe_count).persianDatepicker({

        });
        exe_count ++;
      });
      $(".studious-btn > i.fa-plus").click(function () {
        div = document.createElement("div");
        $(div).addClass('card').addClass('ch-card-item');
        $(div).attr("id",stu_count);
        $(div).html("<form action='' method='post'><div class='row'>" +
              "<div class='col-lg-5'>" +
                "<label for='subject"+ stu_count +"'>عنوان طرح پژوهشی</label>" +
                "<input type='text' id='subject"+ stu_count +"' class='w-100'>" +
              "</div>"+
              "<div class='col-lg-3'>" +
                "<label for='admin"+ stu_count +"'>نام مجری</label>" +
                "<input type='text' id='admin"+ stu_count +"' class='w-100'>" +
              "</div>"+
              "<div class='col-lg-4'>" +
                "<label for='liable"+ stu_count +"'>مسئول اجرا/همکار</label>" +
                "<input type='text' id='liable"+ stu_count +"' class='w-100'>" +
              "</div>"+
            "</div>"+
            "<div class='row'>" +
              "<div class='col-lg-7 rankDiv'>" +
                "<label class='rankLabel' for='rank' style='width:245px'>وضعیت طرح پژوهشی</label>" +
                "<select id='rank'>" +
                  "<option selected dir='rtl'>انتخاب کنید ...</option>" +
                  "<option value='1'>در دست  اجرا</option>" +
                  "<option value='2'>خاتمه یافته</option>" +
                  "<option value='3'>متوقف</option>" +
                "</select>" +
              "</div>"+
              "<div class='col-lg-5'></div>" +
            "</div>" +
            "<div class='row mtop-lg-25'>" +
                "<div class='col-lg-9'>" +
                    "<button type='button' id='"+stu_count+"' class='w-100 accept-btn btn'>افزودن</button>" +
                "</div>"+
                "<div class='col-lg-3'>" +
                    "<button type='button' id='"+stu_count+"' class='w-100 refuse-btn btn'>لغو</button>" +
                "</div>" +
            "</div></form>");
        if($(".studious > .initial-value").hasClass("initial-value")){
            $(".studious").html(div);
        }else {
            $('.studious').append(div);
        }
        delete_item(".studious");
        input_focus();
        stu_count ++;
      });
      $(".article-btn > i.fa-plus").click(function () {
        div = document.createElement("div");
        $(div).addClass('card').addClass('ch-card-item');
        $(div).attr("id",art_count);
        $(div).html("<form action='' method='post'><div class='row'>" +
              "<div class='col-lg-4'>" +
                "<label for='article-name"+ art_count +"'>عنوان مقاله</label>" +
                "<input type='text' id='article-name"+ art_count +"' class='w-100'>" +
              "</div>"+
              "<div class='col-lg-4'>" +
                "<label for='publish-date"+ art_count +"'>تاریخ انتشار</label>" +
                "<input type='text' id='publish-date"+ art_count +"' class='w-100'>" +
              "</div>"+
              "<div class='col-lg-4'>" +
                "<label for='published-at"+ art_count +"'>محل دقیق انتشار</label>" +
                "<input type='text' id='published-at"+ art_count +"' class='w-100'>" +
              "</div>"+
            "</div>" +
            "<div class='row'>" +
              "<div class='col-lg-5'>" +
                "<label for='impact-factor"+ art_count +"'>Impact Factor</label>" +
                "<input type='text' id='impact-factor"+ art_count +"' class='w-100'>" +
              "</div>"+
              "<div class='col-lg-4'>" +
                "<label for='referring-num"+ art_count +"'>تعداد ارجاع به مقاله شما</label>" +
                "<input type='text' id='referring-num"+ art_count +"' class='w-100'>" +
              "</div>"+
              "<div class='col-lg-3'></div>" +
            "</div>" +
            "<div class='row mtop-lg-25'>" +
                "<div class='col-lg-9'>" +
                    "<button type='button' id='"+art_count+"' class='w-100 accept-btn btn'>افزودن</button>" +
                "</div>"+
                "<div class='col-lg-3'>" +
                    "<button type='button' id='"+art_count+"' class='w-100 refuse-btn btn'>لغو</button>" +
                "</div>" +
            "</div></form>");
        if($(".article > .initial-value").hasClass("initial-value")){
            $(".article").html(div);
        }else {
            $('.article').append(div);
        }
        delete_item(".article");
        input_focus();
        art_count ++;
      });
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