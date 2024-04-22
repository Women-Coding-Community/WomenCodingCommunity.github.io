var controllerNavbar = (function (jQuery) {
  const NAVBAR_CLASS_ACTIVE = 'active-nav'

  var selectActiveMenu = function () {
    var pathSegments = jQuery(location).attr('pathname').split('/');
  
    var firstPathSegment = pathSegments[pathSegments.length - 1];
    var stringPathSegment = firstPathSegment.replaceAll('-', ' ');

    var activeLink;
    var activeSubLink;

    if (!stringPathSegment) {
      activeLink = jQuery("a.nav-link:contains('Home')");
    } else {
      var searchLinkText = stringPathSegment[0].toUpperCase() + stringPathSegment.slice(1, stringPathSegment.length);
      activeLink = jQuery("a.nav-link:contains('" + searchLinkText + "')");
      activeSubLink = jQuery("a.nav-link[href='" + firstPathSegment + "']")
    }

    activeLink.addClass(NAVBAR_CLASS_ACTIVE);
    if (activeSubLink) {
      activeSubLink.addClass(NAVBAR_CLASS_ACTIVE);
    }

  };

  return {
    init: selectActiveMenu
  };

}(jQuery));

controllerNavbar.init();
