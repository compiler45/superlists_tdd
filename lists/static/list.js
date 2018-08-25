var initialise = function () {
    $('input[name="text"]').on('keypress', function() {
        $('.has-error').hide();
    });
}
