const controllerNavbar = (function (jQuery) {
  const NAVBAR_CLASS_ACTIVE = 'active-nav'

  const selectActiveMenu = function () {
    const currentPath = window.location.pathname;
  
    jQuery('.nav-link').each(function () {
      const menuItemHref = jQuery(this).attr('href');
      if (currentPath === menuItemHref) {
        jQuery(this).addClass(NAVBAR_CLASS_ACTIVE);
      }
    });
  };

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