function Live(latest_json, latest_img, image_suffix)
{
    this.canvas = document.getElementById('livecanvas');
    this.ctx = this.canvas.getContext("2d");
    this.rect = this.canvas.getBoundingClientRect();

    this.prediction = latest_json;
    this.IMAGE_SUFFIX = image_suffix;

    this.image = new Image();
    this.image.src = '/image/captured/' + latest_img;
    var _this = this;
    this.image.onload = function() {
        _this.redraw();
    };
}

Live.prototype.redraw = function() {
    if (this.image !== null) {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.drawImage(this.image, 0, 0);
        
        var obj = this.prediction['spots'];
        for (var i = 0; i < obj.length; i++) {
            var polygon = obj[i]['points'];

            this.ctx.save();
            this.ctx.beginPath();
            this.ctx.strokeStyle = '#0AFC04';
            if (obj[i]['occupied'] == 1) {
                this.ctx.strokeStyle = 'red';
            }

            this.ctx.lineWidth = 3;
            this.ctx.moveTo(polygon[0][0], polygon[0][1]);

            for (var j = 1; j < polygon.length; j++) {
                this.ctx.lineTo(polygon[j][0], polygon[j][1]);
            }
            this.ctx.closePath();
            this.ctx.stroke();

            if (obj[i]['occupied'] == 1) {
                this.ctx.fillStyle = "rgba(255, 0, 0, 0.2)";
                this.ctx.fill();
            }
            this.ctx.restore();
        }
    }
}

Live.prototype.change_prediction = function(src) {
    this.load_image(src);
    this.load_prediction(src);
}

Live.prototype.load_prediction = function(key) {
    var _this = this;
    $.ajax({
        url: '/api/prediction/' + key,
        type: 'GET',
        contentType: 'application/json',

        success: function(response) {
            if (response.result == 'OK') {
                $('#tabs > div > span').css('border-color', '#ccc');
                key = key.replace(/[!"#$%&'()*+,.\/:;<=>?@[\\\]^`{|}~]/g, "\\$&");
                $('#tabs > div > span#' + key).css('border-color', 'blue');
                _this.prediction = response.polygons;
                _this.redraw();
            } else {
                alert('FAILED TO LOAD PREDICTION');
            }
        }
    });
}

Live.prototype.load_image = function(key) {
    this.image = new Image();
    this.image.src = '/image/captured/' + key.replace('.json', this.IMAGE_SUFFIX);
    var _this = this;
    this.image.onload = function() {
        _this.load_prediction(key);
    };
}
