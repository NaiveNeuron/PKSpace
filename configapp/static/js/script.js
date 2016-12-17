function Point(x, y)
{
    this.x = x;
    this.y = y;
}

Point.prototype.dump = function() {
    return [this.x, this.y];
}

function Polygons()
{
    this.WIDTH = 640;
    this.HEIGHT = 480;
    this.RADIUS = 6;

    this.polygons = [];
    this.current_polygon = [];
    this.rotation = 0;
    this.canvas = document.getElementById("canvas");
    this.ctx = this.canvas.getContext("2d");
    this.canvas2 = document.getElementById("canvas-mask")
    this.ctx2 = this.canvas2.getContext("2d");
    this.rect = this.canvas.getBoundingClientRect();
    this.image = null;
    this.rotated = false;

    this.drag_points = false;
    this.dragging = false;
    this.drag_point = null;
}

Polygons.prototype.start_drag_points = function() {
    this.drag_points = !this.drag_points;
    if (this.drag_points)
        this.save_polygon();
    this.redraw();
}

Polygons.prototype.save_polygon = function() {
    this.polygons.push([this.current_polygon, this.rotation]);
    this.current_polygon = [];
    this.rotation = 0;
    this.redraw();
}

Polygons.prototype.contains = function(x1, y1, x2, y2) {
    var dx = Math.abs(x1-x2);
    var dy = Math.abs(y1-y2);
    return Math.sqrt(dx*dx + dy*dy) < this.RADIUS;
}

Polygons.prototype.get_clicked = function(x, y) {
    for (var i = 0; i < this.polygons.length; i++) {
        var polygon = this.polygons[i][0];
        for (var j = 0; j < polygon.length; j++) {
            if (this.contains(x-this.rect.left-1, y-this.rect.top-1,
                              polygon[j].x, polygon[j].y))
                return polygon[j];
        }
    }
    return false;
}

Polygons.prototype.stop_dragging = function() {
    this.drag_point = null;
    this.dragging = false;
}

Polygons.prototype.move_point = function(x, y) {
    if (this.drag_point != null) {
        this.drag_point.x = x-this.rect.left-1;
        this.drag_point.y = y-this.rect.top-1;
        this.redraw();
    }
}

Polygons.prototype.add_point = function(x, y) {
    if (this.image == null) {
        alert("You have to choose image firstly");
        return;
    }

    /* if user wants to drag points, remember that one to be dragged */
    if (this.drag_points) {
        this.dragging = !this.dragging;
        if (this.dragging)
            this.drag_point = this.get_clicked(x, y);
        else
            this.drag_point = null;
    } else {
        /* -1 because of 1px border around canvas */
        var point = new Point(x-this.rect.left-1, y-this.rect.top-1);
        this.current_polygon.push(point)
    }
    this.redraw();
}

Polygons.prototype.undo = function() {
    if (this.current_polygon.length)
        this.current_polygon.pop();
    else if (this.polygons.length) {
        var tmp = this.polygons.pop();
        this.current_polygon = tmp[0];
        this.rotation = tmp[1];
    }

    this.redraw();
}

Polygons.prototype.set_image = function(image) {
    this.image = image;
    this.redraw();
}

Polygons.prototype.rotate_image = function() {
    this.rotated = !this.rotated;
    this.redraw();
}

Polygons.prototype.redraw = function() {
    if (this.image !== null) {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.draw_image();
        this.draw_polygons();
        this.draw_mask();
    }
}

Polygons.prototype.draw_image = function() {
    if (this.rotated) {
        this.ctx.save();
        this.ctx.translate(this.WIDTH/2, this.HEIGHT/2);
        this.ctx.rotate(Math.PI);
        this.ctx.drawImage(this.image, -this.WIDTH/2, -this.HEIGHT/2);
        this.ctx.restore();
    } else {
        this.ctx.drawImage(this.image, 0, 0);
    }
}

Polygons.prototype.draw_polygon = function(polygon, color, points) {
    if (polygon.length) {
        this.ctx.save();
        this.ctx.beginPath();
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = 3;
        this.ctx.moveTo(polygon[0].x, polygon[0].y);

        for (var i = 1; i < polygon.length; i++) {
                this.ctx.lineTo(polygon[i].x, polygon[i].y);
        }
        this.ctx.closePath();
        this.ctx.stroke();
        
        if (points) {
            for (var i = 0; i < polygon.length; i++) {
                this.ctx.beginPath();
                this.ctx.arc(polygon[i].x, polygon[i].y, this.RADIUS,
                             0, 2*Math.PI);
                this.ctx.closePath();
                this.ctx.stroke();
            }
        }
    }
}

Polygons.prototype.draw_polygons = function() {
    this.draw_polygon(this.current_polygon, 'red', true);

    for (var i = 0; i < this.polygons.length; i++) {
        this.draw_polygon(this.polygons[i][0], '#0AFC04', this.drag_points);
    }
}

Polygons.prototype.rotate_point = function(x, y, centerx, centery) {
    var angle = this.rotation * Math.PI / 180;
    x -= centerx;
    y -= centery;

    var _x = x*Math.cos(angle) - y*Math.sin(angle);
    var _y = x*Math.sin(angle) + y*Math.cos(angle);

    return [_x+centerx, _y+centery];
}

Polygons.prototype.draw_mask = function() {
    this.ctx2.clearRect(0, 0, this.canvas2.width, this.canvas2.height);
    if (this.current_polygon.length) {
        this.ctx2.save();
        
        this.ctx2.beginPath();
        
        var centerx = 0;
        var centery = 0;
        for (var i = 0; i < this.current_polygon.length; i++){
            centerx += this.current_polygon[i].x;
            centery += this.current_polygon[i].y;
        }
        centerx = centerx / this.current_polygon.length;
        centery = centery / this.current_polygon.length;

        var moved = this.rotate_point(this.current_polygon[0].x,
                                      this.current_polygon[0].y,
                                      centerx, centery);
        this.ctx2.moveTo(moved[0], moved[1]);
        for (var i = 1; i < this.current_polygon.length; i++) {
            moved = this.rotate_point(this.current_polygon[i].x,
                                      this.current_polygon[i].y,
                                      centerx, centery);
            this.ctx2.lineTo(moved[0], moved[1]);
        }
        this.ctx2.closePath();
        this.ctx2.clip();
        this.ctx2.translate(centerx, centery);
        this.ctx2.rotate(this.rotation * Math.PI / 180);
        this.ctx2.drawImage(this.image, -centerx, -centery);
        this.ctx2.restore();
    }
}

Polygons.prototype.update_rotation = function(degrees) {
    this.rotation = degrees;
    this.draw_mask();
}

Polygons.prototype.generate_output = function(selector) {
    $(selector).val('{' + JSON.stringify(this.polygons) + '}');
}
