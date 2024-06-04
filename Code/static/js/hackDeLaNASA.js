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
  });
