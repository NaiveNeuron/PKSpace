function Polygons()
{
    this.polygons = [];
    this.current_polygon = [];
    this.canvas = document.getElementById("canvas");
    this.ctx = this.canvas.getContext("2d");
    this.rect = this.canvas.getBoundingClientRect();
    this.image = null;
}

Polygons.prototype.save_polygon = function() {
    this.polygons.push(this.current_polygon);
    this.current_polygon = [];
    this.redraw();
}

Polygons.prototype.add_point = function(x, y) {
    if (this.image == null) {
        alert("You have to choose image firstly");
        return;
    }

    /* -1 because of 1px border around canvas */
    this.current_polygon.push([x-this.rect.left-1, y-this.rect.top-1]);
}

Polygons.prototype.undo = function() {
    this.current_polygon.pop();
    this.redraw();
}

Polygons.prototype.set_image = function(image) {
    this.image = image;
    this.redraw();
}

Polygons.prototype.redraw = function() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.draw_image();
    this.draw_polygons();
}

Polygons.prototype.draw_image = function() {
    this.ctx.drawImage(this.image, 0, 0);
}

Polygons.prototype.draw_polygon = function(polygon, color) {
    if (polygon.length) {
        this.ctx.beginPath();
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = 3;
        this.ctx.moveTo(polygon[0][0], polygon[0][1]);
        for (var i = 1; i < polygon.length; i++) {
                this.ctx.lineTo(polygon[i][0], polygon[i][1])
        }
        this.ctx.closePath();
        this.ctx.stroke();
    }
}

Polygons.prototype.draw_polygons = function() {
    this.draw_polygon(this.current_polygon, 'red');

    for (var i = 0; i < this.polygons.length; i++) {
        this.draw_polygon(this.polygons[i], '#0AFC04');
    }
}

