$(document).ready(function(){
  var batimentOuvert ;
  // Cacher le texte d'info 
  $(".texteInfo").hide();

  actualiseRessources();

  function actualiseRessources(){
    $.ajax({
      url: "/infoRessources",
      type: "GET",
      data: {}, 
      success: function(response) {
          $("#nbGens").text(response.nbGens);
          $("#nbBouphe").text(response.nbBouphe);
          $("#nbKayou").text(response.nbKayou);
          $("#nbBois").text(response.nbBois);
      },
      error: function(error) {
          console.log("PLEURE CHIALE MIAULE SALE FRAUDE", error);
      }
  });
  }

  // Texte sous l'entrepot
  $("#entrepotIm").hover(function(){
      $("#infoEntrepot").show();
    },
    function(){
      $("#infoEntrepot").hide();
    });

    // Texte sous les icones de ressources
    /*
    $(".hoverAble").hover(function(){
      $("")
    },
    function(){
      $("#infoEntrepot").hide();
    });
    */

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
    $("#popUpStat").css("display", "block");
  });

  $("#BoutonCroix").click(function() { 
    $("#popUpStat").css("display", "none");
    batimentOuvert = "";
  });


// test ajax post get

$(".Batiment").click(function() {
  batimentOuvert = $(this).attr("id");
  $.ajax({
      url: "/infoBat",
      type: "GET",
      data: { "nom_bat" : $(this).attr("id") }, 
      success: function(response) {
          $("#titrePopUp").text(response.nom_bat+" -  niveau "+response.niveau_bat)
      },
      error: function(error) {
          console.log("PLEURE CHIALE MIAULE SALE FRAUDE", error);
      }
  });
});


$("#ameliorer").click(function() {
  $.ajax({
      url: "/amelioreBat",
      type: "GET",
      data: {"batimentOuvert": batimentOuvert}, 
      success: function(response) {
        if(response.ameliore == true){
          $("#titrePopUp").text(response.nom_bat+" -  niveau "+response.niveau_bat)
        }
        else{
          alert("les ressources sont insuffisantes")
        }
      },
      error: function(error) {
          console.log("PLEURE CHIALE MIAULE SALE FRAUDE", error);
      }
  });
});
});

