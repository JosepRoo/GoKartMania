$(document).ready(function(){
   $('.containerSlider').slick(
     {
       autoplay: false,
       dots: true,
       autoplaySpeed: 5000 
     }
   );

   $('.containerSlider').on('afterChange', function(event, slick, currentSlide, nextSlide){
    currentItem = $("#slick-slide0"+currentSlide)
    sliderText = currentItem.find(".sliderText")[0]
    sliderButton = currentItem.find(".sliderButton")[0]
    
    $(".sliderText").removeClass("fadeInUp")
    $(sliderText).delay( 800 ).addClass("fadeInUp")
    $(".sliderButton").removeClass("bounceInUp")
    $(sliderButton).delay(1200).addClass("bounceInUp")
  });

  $('.containerSlider').on('init', function(event,slick){
    currentItem = $("#slick-slide0"+currentSlide)
    sliderText = currentItem.find(".sliderText")[0]
   });
 });

 $(function () {
  var waitForFinalEvent=function(){var b={};return function(c,d,a){a||(a="I am a banana!");b[a]&&clearTimeout(b[a]);b[a]=setTimeout(c,d)}}();
  var fullDateString = new Date();  
  function isBreakpoint(alias) {
      return $('.device-' + alias).is(':visible');
  }

  width = $('.grid-stack').width();
  p_size = width / 3;
  gridHeight = (p_size*9)/8; 
  var grid = $('.grid-stack').data('gridstack');
  if(width < 900 ){
    p_size = width;
  }else{
    gridHeight = (p_size*9)/8;
    $('.grid-stack').gridstack({
      cellHeight: gridHeight,
      disableDrag: true,
      disableResize: true,
      staticGrid: true,
    });
  }

  $(document).on("click","#iconMenu",function(){
    $("#menuMobile").addClass('active');
  });
  $(document).on("tap","#iconMenu",function(){
    $("#menuMobile").addClass('active');
  });

  $(document).on("click","#menuMobile",function(e){
    if (e.target !== this)
    return;
  
    $(this).removeClass('active');
  });

  $(document).on("tap","#menuMobile",function(e){
    if (e.target !== this)
    return;
  
    $(this).removeClass('active');
  });

  $(document).on("click","#closeMenu",function(e){    
    $("#menuMobile").removeClass('active');
  });

  //  $(window).resize(function () {
  //     waitForFinalEvent(function() {
  //     width = $('.grid-stack').width();
  //     p_size = width / 3;
  //     var grid = $('.grid-stack').data('gridstack');
  //     if(width < 900 ){
  //       p_size = width;
  //       gridHeight = (p_size*9)/16;
  //     }
     
  //     gridHeight = (p_size*9)/8; 
  //     grid.cellHeight(gridHeight);
  //     resizeGrid();
  //     }, 300, fullDateString.getTime());
  // });
 });

 $('#equipoGaleria .slider-for').slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: false,
  fade: true,
  asNavFor: '#equipoGaleria .slider-nav'
});
$('#equipoGaleria .slider-nav').slick({
  slidesToShow: 5,
  slidesToScroll: 1,
  asNavFor: '#equipoGaleria .slider-for',
  dots: true,
  centerMode: true,
  focusOnSelect: true
});

$('#Eventos .slider-for').slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: false,
  fade: true,
  asNavFor: '#Eventos .slider-nav'
});
$('#Eventos .slider-nav').slick({
  slidesToShow: 5,
  slidesToScroll: 1,
  asNavFor: '#Eventos .slider-for',
  dots: true,
  centerMode: true,
  focusOnSelect: true
});

$('#Clinicas .slider-for').slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: false,
  fade: true,
  asNavFor: '#Clinicas .slider-nav'
});
$('#Clinicas .slider-nav').slick({
  slidesToShow: 5,
  slidesToScroll: 1,
  asNavFor: '#Clinicas .slider-for',
  dots: true,
  centerMode: true,
  focusOnSelect: true
});


$(".promocionestoggle .toggler").each(function(number, item){
  
  childl = $(this);
  childId = childl.attr('id');
  childCheck = $(this).prop('checked');

  
  if(childCheck){
    switch(childId){
      case "toggleCarso":
        $(".promocionesItem").hide();
        $(".promo_carso, .promo_todas").show();
      break;
      case "toggleTlane":
        $(".promocionesItem").hide();
        $(".promo_tlane, .promo_todas").show();
      break;
      default:
      $(".promocionesItem").show();
    
    }
  }
})

$(document).on("click",".toggle",function(){
  childl = $(this).find('input');
  childId = childl.attr('id');
  childCheck = $(this).find('input').prop('checked');  
  
  $(".promocionestoggle .toggler").each(function(number, item){
    if($(item).attr("id") !== childId && childCheck){
      $(item).bootstrapToggle('off');
  }

switch(childId){
  case "toggleCarso":
    $(".promocionesItem").hide();
    $(".promo_carso, .promo_todas").show();
  break;
  case "toggleTlane":
    $(".promocionesItem").hide();
    $(".promo_tlane, .promo_todas").show();
  break;
  default:
  $(".promocionesItem").show();

}
  });
  
});

$(document).on("click",".modal-seguridad a",function(event){
  event.preventDefault();
  $("#modalSeguridad").modal("show");
})


 
