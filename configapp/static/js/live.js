function Live(latest_json, latest_img, image_suffix)
{
    this.canvas = document.getElementById('livecanvas');
    this.ctx = this.canvas.getContext("2d");
    this.rect = this.canvas.getBoundingClientRect();

    this.prediction = latest_json;
    this.IMAGE_SUFFIX = image_suffix;

    this.image = null;

    this.change_prediction(latest_img, false);
}

Live.prototype.redraw = function() {
    draw_labeled_polygons(this.canvas, this.ctx, this.image, this.prediction['spots'], null);
}

Live.prototype.change_prediction = function(key, load) {
    this.image = new Image();
    this.image.src = '/image/captured/' + key.replace(/\.json$/, this.IMAGE_SUFFIX);
    var _this = this;
    this.image.onload = function() {
        if (load) {
            _this.load_prediction(key);
        } else {
            _this.redraw();
        }
    };
    this.image.onerror = function () { alert('IMAGE NOT FOUND'); };
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
                _this.redraw();
            } else {
                alert('FAILED TO LOAD PREDICTION');
            }
        },

        error: function(xhr, ajax_options, thrown_error){
            if(xhr.status == 404) {
                alert('JSON NOT FOUND');
            }
        }
    });
}
