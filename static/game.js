$( document ).ready(function() {

var xCoord = $("#x-coord");
var yCoord = $("#y-coord");
var body = $("body");
var board;
var selected_color = "red";

var url_split = window.location.href.split("/")
var game_id = url_split[url_split.length - 1]


$(".color").click(function(event){
    $(".color").removeClass("highlighted");
    var radioValue = this.innerText.toLowerCase();
    if(radioValue){
        selected_color = radioValue;
    }
    $(this).addClass("highlighted");
});


var socket = io({
    query: {
        game_id: game_id
    }
});

socket.on('set board', (boardData, robotData) => {
    board = JSON.parse(boardData);
    console.log("board", board);
    setupBoard();

    var robots = JSON.parse(robotData);

    set_robots(robots);
});

$('form').submit(function(){
    socket.emit('chat message', $('#m').val());
    $('#m').val('');
    return false;
});

socket.on('chat message', function(msg){
    $('#messages').append($('<li>').text(msg));
});

socket.on("robot moved", (data) => {
    var robot = JSON.parse(data);
    refreshCoords(robot);
});

body.keydown(function(event) {
    switch (event.which) {
        //left
        case 37:
            //if(x>0) {--x;}
            socket.emit("move robot", selected_color, "left", game_id);
            break;
        //up
        case 38:
            //if(y<15) {++y;}
            //websocket
            socket.emit("move robot", selected_color, "up", game_id);
            break;
        //right
        case 39:
            //if(x<15) {++x;}
            //websocket
            socket.emit("move robot", selected_color, "right", game_id);
            break;
        //down
        case 40:
            //if(y>0) {--y;}
            //websocket
            socket.emit("move robot", selected_color, "down", game_id);
    }
});

function refreshCoords(robot) {
    // xCoord.text(x);
    // yCoord.text(y);
    // $(".cell").removeClass("red");
    console.log("robot", robot);
    $(".cell").removeClass(robot.color);
    $("#"+robot.current_coords[0].toString()+'_'+robot.current_coords[1].toString()).addClass(robot.color);
}

function set_robots(robots) {
    $(".cell").removeClass(selected_color);
    for(var i = 0; i < robots.length; i++){
        var coords = robots[i].current_coords;
        var color = robots[i].color;
        $("#"+coords[0].toString()+'_'+coords[1].toString()).addClass(color);
    }
}

function setupBoard() {
    // edges
    var left_cells = $("[id^=0_]");
    left_cells.addClass("left");
    var right_cells = $("[id^=15_]");
    right_cells.addClass("right");
    var top_cells = $("[id$=_15]");
    top_cells.addClass("top");
    var bottom_cells = $("[id$=_0]");
    bottom_cells.addClass("bottom");

    // x_walls
    for(var x = 0; x < 16; x++){
        var y_coords = board.x_walls[x];
        for(var y in y_coords){
            $("#"+x+"_"+y_coords[y]).addClass("top");
        }
    }

    // y_walls
    for(var y = 0; y < 16; y++){
        var x_coords = board.y_walls[y];
        for(var x in x_coords){
            $("#"+x_coords[x]+"_"+y).addClass("right");
        }
    }
}

});