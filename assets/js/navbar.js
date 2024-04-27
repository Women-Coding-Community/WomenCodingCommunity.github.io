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
      activeLink = jQuery("a.nav-link").filter(() => jQuery(this).text().trim() === searchLinkText)
      activeSubLink = jQuery("a.nav-link[href='" + firstPathSegment + "']")
    }

    activeLink.addClass(NAVBAR_CLASS_ACTIVE);
    if (activeSubLink) {
      activeSubLink.addClass(NAVBAR_CLASS_ACTIVE);
    }
  }

  const setupDropdownMenus = function () {
    const dropdownMenuList = jQuery('.dropdown');

    dropdownMenuList.each(function () {
      const dropdownMenu = jQuery(this);
      const dropdownToggle = dropdownMenu.find('.dropdown-toggle');
      const dropdownMenuContent = dropdownMenu.find('.dropdown-menu');

      dropdownToggle.on('mouseenter', function () {
        dropdownMenuContent.addClass('show');
      })

      dropdownMenu.on('mouseleave', function () {
        dropdownMenuContent.removeClass('show');
      })
    });
  }

  return {
    init: function () {
      selectActiveMenu();
      setupDropdownMenus();
    }
  };

}(jQuery));

controllerNavbar.init();