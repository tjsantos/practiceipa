var audioControls = {
    setup: function() {
        var playButton = '<button class="btn btn-s play-audio">' +
            '<span class="glyphicon glyphicon-volume-up"></span></button>';
        $('audio').addClass('hide').after(playButton);
        $('.play-audio').on('click', function() {
            $(this).prev('audio').trigger('play');
        });
    }
};
$(audioControls.setup);

var resetProgress = {
    setup: function() {
        $('#reset-progress').on('click', function() {
            return confirm('Reset progress?');
        });
    }
};
$(resetProgress.setup);
