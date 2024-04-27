const controllerNavbar = (function (jQuery) {
  const NAVBAR_CLASS_ACTIVE = 'active-nav'

  const selectActiveMenu = function () {
    const pathSegments = jQuery(location).attr('pathname').split('/');
  
    const firstPathSegment = pathSegments[pathSegments.length - 1];
    const stringPathSegment = firstPathSegment.replaceAll('-', ' ');

    const activeLink;
    const activeSubLink;

    if (!stringPathSegment) {
      activeLink = jQuery("a.nav-link:contains('Home')");
    } else {
      const searchLinkText = stringPathSegment[0].toUpperCase() + stringPathSegment.slice(1, stringPathSegment.length);
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