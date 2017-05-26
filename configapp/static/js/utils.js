function draw_labeled_polygons(canvas, ctx, image, polygons, occupies)
{
    try {
        if (image !== null) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(image, 0, 0);
            
            for (var i = 0; i < polygons.length; i++) {
                var polygon = polygons[i]['points'];

                ctx.save();
                ctx.beginPath();
                ctx.strokeStyle = '#0AFC04';
                
                if ((occupies == null && polygons[i]['occupied'] == 1) ||
                    (occupies != null && occupies[i] == 1)) {
                    ctx.strokeStyle = 'red';
                }

                ctx.lineWidth = 3;
                ctx.moveTo(polygon[0][0], polygon[0][1]);

                for (var j = 1; j < polygon.length; j++) {
                    ctx.lineTo(polygon[j][0], polygon[j][1]);
                }
                ctx.closePath();
                ctx.stroke();

                if ((occupies == null && polygons[i]['occupied'] == 1) ||
                    (occupies != null && occupies[i] == 1)) {
                    ctx.fillStyle = "rgba(255, 0, 0, 0.2)";
                    ctx.fill();
                }

                ctx.restore();
            }
        }
    } catch (err) {
        alert('Not a valid json');
    }
}
