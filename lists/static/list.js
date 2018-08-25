window.Superlists = {};
window.Superlists.initialise = function() {
    $('input[name="text"]').on('keypress', function() {
        $('.has-error').hide();
    });
};
