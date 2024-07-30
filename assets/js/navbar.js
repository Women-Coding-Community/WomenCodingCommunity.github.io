const controllerNavbar = (function (jQuery) {
  const NAVBAR_CLASS_ACTIVE = 'active-nav';
  const SHOW_CLASS = 'show';

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

      // Toggle dropdown menu when clicking the dropdown toggle
      dropdownToggle.on('click', function (e) {
        e.preventDefault();
        
        jQuery('.dropdown-menu').not(dropdownMenuContent).removeClass(SHOW_CLASS);
        
        dropdownMenuContent.toggleClass(SHOW_CLASS);
      });

      jQuery(document).on('click', function (e) {
        if (!dropdownMenu.is(e.target) && dropdownMenu.has(e.target).length === 0 
          && !dropdownToggle.is(e.target) && dropdownToggle.has(e.target).length === 0) {
          dropdownMenuContent.removeClass(SHOW_CLASS);
        }
      });
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