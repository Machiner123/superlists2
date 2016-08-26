jQuery(document).ready(function () {
    $("input[name='text']").keypress(function () { 
        $('.has-error').hide();
    });
});
/*
jQuery(document).ready(function () {
    $('input').on('keypress', '#texties', function(){
        $('.has-error').hide();
    });
});
*/