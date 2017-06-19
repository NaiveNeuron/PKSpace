function Labeler(pic_width, pic_height)
{
    this.WIDTH = pic_width;
    this.HEIGHT = pic_height;
    this.canvas = document.getElementById('labcanvas');
    this.ctx = this.canvas.getContext("2d");
    this.ctx.canvas.width = this.WIDTH;
    this.ctx.canvas.height = this.HEIGHT;
    this.rect = this.canvas.getBoundingClientRect();

    this.image = null;
    this.polygons = {'spots': []};
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
    this.src = src;

    this.image = new Image();
    this.image.src = '/datasetimg/' + src;
    var _this = this;
    this.image.onload = function() {
        _this.redraw();
    };
    this.image.onerror = function () { alert('IMAGE NOT FOUND'); };
}

Labeler.prototype.is_inside = function(vs, x, y) {
    // ray-casting algorithm based on
    // http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html

    var inside = false;
    for (var i = 0, j = vs.length - 1; i < vs.length; j = i++) {
        var xi = vs[i][0], yi = vs[i][1];
        var xj = vs[j][0], yj = vs[j][1];
        var intersect = ((yi > y) != (yj > y))
            && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }
    return inside;
}

Labeler.prototype.clicked = function(x, y) {
    x = this.mouse_x(x);
    y = this.mouse_y(y);
    for (var i = 0; i < this.polygons['spots'].length; i++) {
        if (this.is_inside(this.polygons['spots'][i]['points'], x, y)) {
            if (this.occupies[i] == 1)
                this.occupies[i] = 0;
            else
                this.occupies[i] = 1;
            this.redraw();
            return;
        }
    }
}

Labeler.prototype.redraw = function() {
    draw_labeled_polygons(this.canvas, this.ctx, this.image, this.polygons['spots'], this.occupies);
}

Labeler.prototype.load_polygons = function() {
    try {
        this.occupies = [];
        for (var i = 0; i < this.polygons['spots'].length; i++) {
            this.occupies.push(0);
        }
        this.redraw();
    } catch(err) {
        alert('Not a valid json.');
    }
}

Labeler.prototype.save = function(saveurl) {
    if (this.polygons['spots'].length == 0)
        return;

    for (var i = 0; i < this.polygons['spots'].length; i++) {
        this.polygons['spots'][i]['occupied'] = this.occupies[i];
    }

    var toSend = {labeled: this.polygons};

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
                _this.polygons = response.polygons;
                _this.load_polygons();
            } else {
                alert('FAILED TO LOAD MASK');
            }
        },

        error: function(xhr, ajax_options, thrown_error) {
            console.log("XXXXXXXXXXXXXx");
            if(xhr.status == 404) {
                alert('JSON not found');
            }
        }
    });
}

Labeler.prototype.set_occupancy_of_all = function(occupancy) {
    for (var i = 0; i < this.polygons['spots'].length; i++) {
        this.occupies[i] = occupancy;
    }
    this.redraw();
}

Labeler.prototype.reverse_occupancy_of_all = function(occupancy) {
    for (var i = 0; i < this.polygons['spots'].length; i++) {
        this.occupies[i] = !this.occupies[i];
    }
    this.redraw();
}
