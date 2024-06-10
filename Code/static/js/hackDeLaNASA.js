$(document).ready(function(){
  // Cacher le texte d'info 
  $(".texteInfo").hide();

  // Texte sous l'entrepot
  $("#entrepotIm").hover(function(){
      $("#infoEntrepot").show();
    },
    function(){
      $("#infoEntrepot").hide();
    });

  // Changer le texte 
  $("#entrepotIm").click(function(){
    $("#infoEntrepot").text("Entrepot - niv2");
  });

  // Affciher le pop up
  $(".Batiment").hover(function(){
    $(this).css("filter", "brightness(0.5)");
  },
  function(){
    $(this).css("filter", "brightness(1)");
  });

  $("#entrepotIm").click(function(){
    $("#infoEntrepot").text("Entrepot - niv2");
  });
  

  $(".Batiment").click(function(){
    $(".popUp").css("display", "block");
  });

  $("#BoutonCroix").click(function() { 
    $(".popUp").css("display", "none");
  });


// test ajax post get

$(".Batiment").click(function() {
  $.ajax({
      url: "/infoBat",
      type: "GET",
      data: { "nom_bat" : $(this).attr("id") }, 
      success: function(response) {
          $("#titrePopUp").text(response.nom_bat+" niveau 1")
      },
      error: function(error) {
          console.log("PLEURE CHIALE MIAULE SALE FRAUDE", error);
      }
  });
});
  });

