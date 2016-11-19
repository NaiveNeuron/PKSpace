$('.btn-choose').click(function() {
    $('#image-previews').slideToggle();
});

$('#image-previews img').click(function() {
    $('#image-previews img').css('border-color', '#ffffff');

    $(this).css('border-color', '#4A42DE');

    var c = document.getElementById("canvas");
    var ctx = c.getContext("2d");
    ctx.drawImage(this, 0, 0);
});
