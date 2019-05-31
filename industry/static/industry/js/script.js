$(document).ready(function(){
  // variable

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
  //codes
  input_focus();
  $(".form-submit").click(function () {
    $(".main").removeClass("blur-div");
    $(".mainInfo-body").css("display","none");
  });
  $("i.fa-plus").click(function () {
    if ($("input#keys").val() !== '') {
      div = document.createElement("div");
      $(div).addClass("key-item");
      $(div).html("<i class='fas fa-times'></i><span>" + $("input#keys").val() + "</span>");
      $(".selected_keys").append(div);
      $("input#keys").val('').focus();
    }
  });
  $(".fa-times").click(function () {
    $($(".fa-times").closest(div)).remove();
  });
  $('input#upload-input').change(function (event) {
    $("img.profile").fadeIn("fast").attr('src',URL.createObjectURL(event.target.files[0]));
  });
  var contentWidth = $(document).innerWidth() - 250;
  $(".content").css({"width":contentWidth,
    "height":"90%"});
  $(".side-bar").css("height","100%");
});
