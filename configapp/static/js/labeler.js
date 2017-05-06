function Point(x, y)
{
    this.x = x;
    this.y = y;
}

function Labeler()
{
    this.canvas = document.getElementById('labcanvas');
    this.ctx = this.canvas.getContext("2d");
    this.rect = this.canvas.getBoundingClientRect();
    this.image = null;
    this.polygons = [];
    this.occupies = [];
    this.src = '';
}

Labeler.prototype.mouse_x = function(x) {
    return Math.round(x-this.rect.left-1);
}

Labeler.prototype.mouse_y = function(y) {
    return Math.round(y-this.rect.top-1);
}

Labeler.prototype.change_image = function(src) {
    /*this.image = document.createElement("IMG");
    this.image.src = '/datasetimg/' + src;*/

    this.src = src;

    this.image = new Image();
    this.image.src = '/datasetimg/' + src;
    var _this = this;
    this.image.onload = function() {
        _this.redraw();
    };
}

Labeler.prototype.is_inside = function(vs, x, y) {
    // ray-casting algorithm based on
    // http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html

    var inside = false;
    for (var i = 0, j = vs.length - 1; i < vs.length; j = i++) {
        var xi = vs[i].x, yi = vs[i].y;
        var xj = vs[j].x, yj = vs[j].y;
        var intersect = ((yi > y) != (yj > y))
            && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }
    return inside;
}

Labeler.prototype.clicked = function(x, y) {
    x = this.mouse_x(x);
    y = this.mouse_y(y);
    for (var i = 0; i < this.polygons.length; i++) {
        if (this.is_inside(this.polygons[i][0], x, y)) {
            if (this.occupies[i] == 1)
                this.occupies[i] = 0;
            else
                this.occupies[i] = 1;
            this.redraw();
            return;
        }
    }
}

Labeler.prototype.draw_polygon = function(polygon, occupied) {
    this.ctx.save();
    this.ctx.beginPath();
    this.ctx.strokeStyle = '#0AFC04';
    if (occupied == 1) {
        this.ctx.strokeStyle = 'red';
    }

    this.ctx.lineWidth = 3;
    this.ctx.moveTo(polygon[0].x, polygon[0].y);

    for (var i = 1; i < polygon.length; i++) {
        this.ctx.lineTo(polygon[i].x, polygon[i].y);
    }
    this.ctx.closePath();
    this.ctx.stroke();

    if (occupied == 1) {
        this.ctx.fillStyle = "rgba(255, 0, 0, 0.2)";
        this.ctx.fill();
    }
    this.ctx.restore();
}

Labeler.prototype.draw_polygons = function() {
    for (var i = 0; i < this.polygons.length; i++) {
        this.draw_polygon(this.polygons[i][0], this.occupies[i]);
    }
}

Labeler.prototype.redraw = function() {
    if (this.image != null) {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.drawImage(this.image, 0, 0);
        this.draw_polygons();
    }
}

Labeler.prototype.load_polygons = function(obj) {
    try {
        var obj = obj['spots'];
        var tmp = [];
        for (var i = 0; i < obj.length; i++) {
            tmp.push([[]]);
            for (var j = 0; j < obj[i]['points'].length; j++) {
                tmp[i][0].push(new Point(obj[i]['points'][j][0], obj[i]['points'][j][1]));
            }
            tmp[i].push(obj[i]['rotation']);
            this.occupies.push(0);
        }
        this.polygons = tmp;
        this.redraw();
    } catch(err) {
        alert('Not a valid json.');
    }
}

Labeler.prototype.save = function(saveurl) {
    if (this.polygons.length == 0)
        return;

    var imagejson = {'spots': []};

    for (var i = 0; i < this.polygons.length; i++) {
        var spot = {'id': i, 'rotation': this.polygons[i][1],
                    'occupied': this.occupies[i]};

        var points = [];
        for (var j = 0; j < this.polygons[i][0].length; j++) {
            points.push([this.polygons[i][0][j].x, this.polygons[i][0][j].y]);
        }
        spot['points'] = points;
        imagejson['spots'].push(spot);
    }

    var toSend = {labeled: imagejson};

    $.ajax({
        url: '/savelabel/' + this.src,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(toSend),

        success: function(response) {
            if (response.result == 'OK') {
                var imgid = "#" +
                    response.imgid.replace(/[!"#$%&'()*+,.\/:;<=>?@[\\\]^`{|}~]/g, "\\$&");
                $(imgid).addClass('green');
            }
        }
    });
}

Labeler.prototype.change_mask = function(selector) {
    var name = selector.attr('data-key');
    var _this = this;
    $.ajax({
        url: '/api/mask/' + name,
        type: 'GET',
        contentType: 'application/json',
        
        success: function(response) {
            if (response.result == 'OK') {
                selector.css('border-color', 'blue');
                _this.load_polygons(response.polygons);
            } else {
                alert('FAILED TO LOAD MASK');
            }
        }
    });
}

Labeler.prototype.set_occupancy_of_all = function(occupancy) {
    for (var i = 0; i < this.polygons.length; i++) {
        this.occupies[i] = occupancy;
    }
    this.redraw();
}

Labeler.prototype.reverse_occupancy_of_all = function(occupancy) {
    for (var i = 0; i < this.polygons.length; i++) {
        this.occupies[i] = !this.occupies[i];
    }
    this.redraw();
}
