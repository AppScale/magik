$(function() {
    $("[name=cloud]").click(function(){
        $('.toHideCloud').hide();
        $("#cloud-"+$(this).val()).show('slow');
    });

    $("[name=directive]").click(function(){
        $('.toHideDirective').hide();
        $("#directive-"+$(this).val()).show('slow');
    });
});
