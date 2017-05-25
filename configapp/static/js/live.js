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
        util_draw_polygons(_this.canvas, _this.ctx, _this.image, _this.prediction['spots'], null);
    };
}

Live.prototype.change_prediction = function(key) {
    this.image = new Image();
    this.image.src = '/image/captured/' + key.replace(/\.json$/, this.IMAGE_SUFFIX);
    var _this = this;
    this.image.onload = function() {
        _this.load_prediction(key);
    };
}

Live.prototype.load_prediction = function(key) {
    var _this = this;
    var escaped = key.replace(/[!"#$%&'()*+,.\/:;<=>?@[\\\]^`{|}~]/g, "\\$&");
    $('#tabs > div > span#' + escaped).css('border-color', 'red');

    $.ajax({
        url: '/api/prediction/' + key,
        type: 'GET',
        contentType: 'application/json',

        success: function(response) {
            if (response.result == 'OK') {
                $('#tabs > div > span').css('border-color', '#ccc');
                $('#tabs > div > span#' + escaped).css('border-color', 'blue');
                _this.prediction = response.polygons;
                util_draw_polygons(_this.canvas, _this.ctx, _this.image, _this.prediction['spots'], null);
            } else {
                alert('FAILED TO LOAD PREDICTION');
            }
        }
    });
}
