function generate_results(){
    $("#bg-image").attr("blur", "true");
    if(place1 != "" && place2 != ""){

        var start_lat = place1.geometry.location.lat();
        var start_lon = place1.geometry.location.lng();

        var end_lat = place2.geometry.location.lat();
        var end_lon = place2.geometry.location.lng();

        $.ajax("/get_results?start_lat=" + start_lat + "&start_lon=" + start_lon + "&end_lat=" + end_lat + "&end_lon=" + end_lon)
            .done(function(resp){
                console.log(resp);
                $("#results-text").html(resp);
                $("#bg-image").attr("blur", "false");
            });
    } else {
         $("#results-text").html("Please enter start and end");
         setTimeout(function(){
            $("#bg-image").attr("blur", "false");
         }, 1000);
    }


}

$(document).ready(function(){
    $("#generate").click(function (){
        generate_results();
    })
    let width = window.innerWidth;
    //console.log("window width: " + width);
    //$("#main").css("min-width", width + "px;");
})