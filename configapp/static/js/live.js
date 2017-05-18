function Live(json_string)
{
    this.canvas = document.getElementById('livecanvas');
    this.ctx = this.canvas.getContext("2d");
    this.rect = this.canvas.getBoundingClientRect();

    this.json_string = json_string;
    
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
        
        var obj = JSON.parse(this.json_string)['spots'];
        console.log(obj);
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

Live.prototype.load_prediction = function(key) {

}

Live.prototype.load_image = function(key) {

}
