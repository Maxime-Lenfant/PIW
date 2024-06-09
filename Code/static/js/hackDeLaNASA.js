$(document).ready(function(){
    $("#infoEntrepot").hide();
    $("#entrepotIm").hover(function(){
        $("#infoEntrepot").show();
      },
      function(){
        $("#infoEntrepot").hide();
      });
    $("#entrepotIm").click(function(){
      $("#infoEntrepot").text("Entrepot - niv2");
    });

    $(".cercle").hover(function(){
      $(this).css("filter", "brightness(0.5)");
    },
    function(){
      $(this).css("filter", "brightness(1)");
    });
  $("#entrepotIm").click(function(){
    $("#infoEntrepot").text("Entrepot - niv2");
  });    

  });

