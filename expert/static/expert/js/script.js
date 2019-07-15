$('*').persiaNumber();
function load_dialog(){
        $(".title-back").each(function () {
            var title_back_width = $(this).prev().outerWidth() + 30;
            $(this).css("width", title_back_width);
        });

        $(".row-header > .header").each(function () {
            var divWidth = $(this).outerWidth();
            divWidth = $(this).closest("div").innerWidth() - divWidth;
            $(this).prev().css("width",divWidth/2 - 10);
            $(this).next().css("width",divWidth/2 - 10);
            $(this).css("left", (divWidth)/2 );
        });
    }
    function init_windowSize() {
         if($(window).width() < 575.98){

         }else {
             var contentWidth = $(document).innerWidth() - 250;
             var contentMargin = 0.0862 * contentWidth - 63.9655;
             $(".info-card").css({
                 "margin-right": contentMargin,
                 "margin-left": contentMargin
             });
             $(".content").css({
                 "width": contentWidth,
                 "height": "90%"
             });
             $(".side-bar").css("height", "100%");
         }
    }
    function loading() {
        $(".main").addClass("blur-div");
        var canvas = $("#loading-canvas");
        canvas.drawArc({
            strokeStyle: '#000',
            strokeWidth: 4,
            rounded: true,
            endArrow: true,
            arrowRadius: 15,
            arrowAngle: 90,
            x: 160, y: 120,
            start: 90,
            end: 360,
            radius: 50
        });
    }
    function blur_div_toggle(content) {
            if($(content).hasClass("blur-div")) {
                $(content).removeClass("blur-div");
            }else {
                $(content).addClass("blur-div");
            }
    }
    function init_dialog_btn(element, dialogClass) {
        $(element).click(function (){
            blur_div_toggle(".main");
            $(dialogClass).css("display","block");
            close_dialog(dialogClass);
            load_dialog();
            if( dialogClass === ".showProject"){
                accept_project();
            }
        });
    }
    function input_focus(){
        if( $("input,textarea").prop("disabled") ) {
            $(this).each(function () {
                var inputLabel = "label[for='"+$(this).attr("id")+"']";
                $(inputLabel).css({
                    "font-size":"13px",
                    "top":"0px",
                    "right":"15px",
                    "color":"#8d8d8d"
                });
            });
        }
        $("input,textarea").on("focus", function () {
            if($(this).hasClass("solid-label"))
                return false;
            var inputLabel = "label[for='"+$(this).attr("id")+"']";
            $(inputLabel).css({
                "font-size":"13px",
                "top":"0px",
                "right":"15px",
                "color":"#3CCD1C"
            });
            $(this).css("color","#3ccd1c");
        }).on("focusout", function () {
            if($(this).hasClass("solid-label"))
                return false;
            var inputLabel = "label[for='"+$(this).attr("id")+"']";
            $(inputLabel).css("color","#6f7285");
            if($(this).val() === ''){
                $(inputLabel).css({
                    "font-size":"14px",
                    "top":"28px",
                    "right":"25px",
                    "color":"#6f7285"
                });
            }else {
                $(this).css("color","#8d8d8d");
                $(inputLabel).css("color","#8d8d8d");
            }
        });
    }
    function delete_item(className){
        $(".delete-item").click(function () {
            $(className+ " div#" + $(this).attr("id")).remove();
        });
    }
    function accept_project(){
        $(".accept-btn").click(function () {
            $(".showProject").slideUp('slow').delay('slow');
            $(".project-details").delay('slow').slideDown('slow');
            close_dialog(".project-details");
            load_dialog();
        });
    }
    function close_dialog(className){
        $(".close").click(function (){
            $(className).css("display","none");
            $(".main").removeClass("blur-div");
        });
    }
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

    input_focus();
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
        // loading();
        init_windowSize();
        init_dialog_btn(".chamran-btn-info" , ".showProject");
        init_dialog_btn(".researcher-card-button-show" , ".researcher-info-dialog");
        // if($(".mainInfo-body").css("display") === "block"){
        //     blur_div_toggle(".top-bar");
        //     blur_div_toggle(".side-bar");
        // }
        express_btn();
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
      $(".chamran_btn.education-btn").click(function () {
        div = document.createElement("div");
        $(div).addClass('card').addClass('ch-card-item');
        $(div).attr("id",edu_count);
        $(div).html("<div class='row'>" +
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
            "<div class='col-lg-4'>" +
              "<label for=\"university"+edu_count+"\">دانشگاه</label>\n" +
              "<input type=\"text\" id=\"university"+edu_count+"\" class=\"w-100\">" +
            "</div>" +
            "<div class='col-lg-3'>" +
              "<label for=\"edu-city"+edu_count+"\">شهر محل تحصیل</label>\n" +
              "<input type=\"text\" id=\"edu-city"+edu_count+"\" class=\"w-100\">" +
            "</div>" +
            "<div class='col-lg-3'>" +
              "<label for=\"year"+edu_count+"\">سال اخذ مدرک</label>\n" +
              "<input type=\"text\" id=\"year"+edu_count+"\" class=\"w-100\">" +
            "</div>" +
            "<div class='col-lg-2' style='display:flex'>" +
              "<div class='wait-item' id='"+edu_count+"'>" +
                "<span>منتظر تایید....</span>"+
                "<i class='fas fa-clock'></i>" +
              "</div>" +
              "<div class='delete-item' id='"+edu_count+"'>" +
                "<span>حذف</span>"+
                "<i class='fas fa-trash'></i>" +
              "</div>" +
            "</div>" +
            "</div>");
        $('.education').append(div);
        delete_item(".education");
        input_focus();
        edu_count ++;
      });
      $(".chamran_btn.executive-btn").click(function () {
        div = document.createElement("div");
        $(div).addClass('card').addClass('ch-card-item');
        $(div).attr("id",exe_count);
        $(div).html("<div class='row'>" +
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
              "<div class='col-lg-3' style='display:flex'>" +
                "<div class='wait-item' id='"+exe_count+"'>" +
                  "<span>منتظر تایید....</span>"+
                  "<i class='fas fa-clock'></i>" +
                "</div>" +
                "<div class='delete-item' id='"+exe_count+"'>" +
                  "<span>حذف</span>"+
                  "<i class='fas fa-trash'></i>" +
                "</div>" +
              "</div>" +
            "</div>");
        $('.executive').append(div);
        delete_item(".executive");
        input_focus();
        $("#from"+ exe_count).persianDatepicker({

        });
        $("#until"+ exe_count).persianDatepicker({

        });
        exe_count ++;
      });
      $(".chamran_btn.studious-btn").click(function () {
        div = document.createElement("div");
        $(div).addClass('card').addClass('ch-card-item');
        $(div).attr("id",stu_count);
        $(div).html("<div class='row'>" +
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
              "<div class='col-lg-5' style='display:flex'>" +
                "<div class='wait-item' id='"+stu_count+"'>" +
                  "<span>منتظر تایید....</span>"+
                  "<i class='fas fa-clock'></i>" +
                "</div>" +
                "<div class='delete-item' id='"+stu_count+"'>" +
                  "<span>حذف</span>"+
                  "<i class='fas fa-trash'></i>" +
                "</div>" +
              "</div>" +
            "</div>");
        $('.studious').append(div);
        delete_item(".studious");
        input_focus();
        stu_count ++;
      });
      $(".chamran_btn.article-btn").click(function () {
        div = document.createElement("div");
        $(div).addClass('card').addClass('ch-card-item');
        $(div).attr("id",art_count);
        $(div).html("<div class='row'>" +
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
              "<div class='col-lg-3' style='display:flex'>" +
                "<div class='wait-item' id='"+art_count+"'>" +
                  "<span>منتظر تایید....</span>"+
                  "<i class='fas fa-clock'></i>" +
                "</div>" +
                "<div class='delete-item' id='"+art_count+"'>" +
                  "<span>حذف</span>"+
                  "<i class='fas fa-trash'></i>" +
                "</div>" +
              "</div>" +
            "</div>");
        $('.article').append(div);
        delete_item(".article");
        input_focus();
        art_count ++;
      });
      $(".chamran_btn.technique").click(function () {
        $(".main").addClass("blur-div");
        $(".dialog-main").css("display","block");
        close_dialog();
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