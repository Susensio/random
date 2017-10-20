scale = 20;

function Snake() {
    this.body = [createVector(20,20)];
    this.direction = createVector(1,0);
    this.direction = createVector(1,0);

    this.show = function () {
        for (var i = this.body.length - 1; i >= 0; i--) {
            fill(0,200,0);
            rect(scale*this.body[i].x, scale*this.body[i].y, scale*0.9, scale*0.9);
        }
    }

    this.update = function (fruit) {
        var head = createVector(this.body[0].x+this.direction.x, this.body[0].y+this.direction.y);
        if (head.x<0) head.x = width/scale-1;
        if (head.x>width/scale-1) head.x = 0;

        if (head.y<0) head.y = height/scale-1;
        if (head.y>height/scale-1) head.y = 0;

        this.body.unshift(head);
        if (this.position(fruit)){
            fruit.new()
            frameRate(ceil(frameRate()*1.2));
        }
        else {
            this.body.pop();
        }
        this.oldDirection = this.direction;
    }

    this.position = function (pos) {
        return this.body[0].x == pos.x && this.body[0].y == pos.y;
    }

    this.getScore = function () {
        return "Score: " + this.body.length;
    }

    this.gameOver = function () {
        var gameOver = false;
        for (var i = this.body.length - 1; i >= 3; i--) {
            if (this.body[0].x == this.body[i].x && this.body[0].y == this.body[i].y){
                gameOver = true;
                break;
            }
        }
        return gameOver;
    }
}

function Apple(){
    this.x = int(random(width/scale));
    this.y = int(random(height/scale));
    
    this.show = function () {
        fill(220,0,0);
        rect(scale*this.x, scale*this.y, scale*0.9, scale*0.9);
    }

    this.new = function () {
        this.x = int(random(width/scale));
        this.y = int(random(height/scale));
    }
}