function Point(x, y)
{
    this.x = x;
    this.y = y;
}

function Live()
{
    this.canvas = document.getElementById('livecanvas');
    this.ctx = this.canvas.getContext("2d");
    this.rect = this.canvas.getBoundingClientRect();
    this.polygons = [];
    
    this.image = new Image();
    this.image.src = '/live/image';
    var _this = this;
    this.image.onload = function() {
        _this.redraw();
    };
}

Live.prototype.redraw = function() {
    if (this.image !== null) {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.drawImage(this.image, 0, 0);
        //this.draw_polygons();
    }
}

Labeler.prototype.draw_polygons = function() {
    for (var i = 0; i < this.polygons.length; i++) {
        this.draw_polygon(this.polygons[i][0], this.occupies[i]);
    }
}

Live.prototype.load_polygons = function(str) {
    // TODO: change this to load polygons along with their occupation
    try {
        var obj = JSON.parse(str)['spots'];
        var tmp = [];
        for (var i = 0; i < obj.length; i++) {
            tmp.push([[]]);
            for (var j = 0; j < obj[i][0].length; j++) {
                tmp[i][0].push(new Point(obj[i][0][j][0], obj[i][0][j][1]));
            }
            tmp[i].push(obj[i][1]);
        }
        this.polygons = tmp;
        this.redraw();
    } catch(err) {
        alert('Not a valid json.');
    }
}
