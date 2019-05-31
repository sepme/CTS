$(document).ready(function(){
  // variable
  edu_count = 0;
  exe_count = 0;
  stu_count = 0;
  art_count = 0;
  // functions
  function input_focus(){
      $("input,textarea").on("focus", function () {
        var inputLabel = "label[for='"+$(this).attr("id")+"']";
        $(inputLabel).css({
          "font-size":"13px",
          "top":"0px",
          "right":"15px",
          "color":"#3CCD1C"
        });
      $(this).css("color","#3ccd1c");
      }).on("focusout", function () {
        var inputLabel = "label[for='"+$(this).attr("id")+"']";
        $(inputLabel).css("color","#bdbdbd");
        if($(this).val() === ''){
          $(inputLabel).css({
            "font-size":"14px",
            "top":"28px",
            "right":"25px",
            "color":"#bdbdbd"
          });
        } else {
          $(this).css("color","#8d8d8d");
          $(inputLabel).css("color","#8d8d8d");
        }
      });
  }
  function delet_item(className){
    $(".delete-item").click(function () {
      $(className+ " div#" + $(this).attr("id")).remove();
    });
  }
  //codes
  input_focus();
  $(".form-submit").click(function () {
    $(".main").removeClass("blur-div");
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
    delet_item(".education");
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
    delet_item(".executive");
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
    delet_item(".studious");
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
    delet_item(".article");
    input_focus();
    art_count ++;
  });
  // var sideBar = $(".side-bar");
  // $(".menu").click(function() {
  //   if(sideBar.hasClass('min')) {
  //     sideBar.removeClass('min');
  //     sideBar.css("width","250px");
  //     $(".menu").css("right","250px");
  //     $(".chamranteam").attr("src","img/logoName.png");
  //   }else {
  //     sideBar.addClass('min');
  //     sideBar.css("width","120px");
  //     $(".menu").css("right","120px");
  //     // $(".chamranteam").attr("src","img/logo.png");
  //
  //   }
  // });
  var contentWidth = $(document).innerWidth() - 250;
  $(".content").css({"width":contentWidth,
    "height":"90%"});
  $(".side-bar").css("height","100%");
  // $(window).on("resize", function () {
  //   var contentHeight = $(document).height()-70;
  //   var contentWidth = $(document).innerWidth() - 250;
  //   $(".content").css({"width":contentWidth,
  //     "height":contentHeight});
  //   $(".side-bar").css("height",$(document).height());
  // });
  // document.getElementsByTagName("body")[0].onresize = function () {
  //   var contentHeight = $(document).height()-70;
  //   var contentWidth = $(document).innerWidth() - 250;
  //   $(".content").css({"width":contentWidth,
  //     "height":contentHeight});
  //   $(".side-bar").css("height",$(document).height());
  // };

});
