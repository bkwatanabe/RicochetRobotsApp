$( document ).ready(function() {

$("#start_game").click(function(event){
    $.post("game", function(data){
        // console.log("data", data);
        window.location.replace("./game/" + data);
    });
});

});