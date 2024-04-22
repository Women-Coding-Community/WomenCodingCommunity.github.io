var controllerHome = (function(jQuery) {
    var adjustHomeLink = function() {
        if (document.location.hostname === 'localhost') {
            jQuery('.navbar-brand').attr('href', '/');
            jQuery('#nav-0').attr('href', '/');
        }
    };

    return {
        init: adjustHomeLink
    };

}(jQuery));

controllerHome.init();
