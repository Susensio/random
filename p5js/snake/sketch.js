var player;
var fruit;
const scale = 20;
var topscore = 0;

function setup() {
    createCanvas(640, 480);
    frameRate(3);
    player = new Snake();
    fruit = new Apple();
    fruit.show();
    player.show();
}

function draw() {
    clear();
    background(51);

    player.update(fruit);
    fruit.show();
    player.show();

    fill(255);
    text(player.getScore(),5,20);
    text("Top score: " + topscore, 60,20);

    if (player.gameOver()) {
        topscore = player.getScore();
        player.body = [createVector(20,20)];
        frameRate(3);
    }
}

function keyPressed(){
    if (keyCode === LEFT_ARROW) {
        if (player.oldDirection.x != 1) player.direction = createVector(-1,0);
    } else if (keyCode === RIGHT_ARROW) {
        if (player.oldDirection.x != -1) player.direction = createVector(1,0);
    } else if (keyCode === UP_ARROW) {
        if (player.oldDirection.y != 1) player.direction = createVector(0,-1);
    } else if (keyCode === DOWN_ARROW) {
        if (player.oldDirection.y != -1) player.direction = createVector(0,1);
    }
}