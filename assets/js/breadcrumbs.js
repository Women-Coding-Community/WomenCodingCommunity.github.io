const controllerBreadcrumbs = (function (jQuery) {
    const BREADCRUMB_CLASS_ACTIVE = 'active'
  
    const selectActiveMenu = function () {
      const currentPath = window.location.pathname;
    
      jQuery('.breadcrumb-item').each(function () {
        const menuItemHref = jQuery(this).find("a").attr('href');
        if (currentPath === menuItemHref) {
          jQuery(this).addClass(BREADCRUMB_CLASS_ACTIVE);
        }
      });
    };
  
    return {
      init: function () {
        selectActiveMenu();
      }
    };
  
  }(jQuery));
  
  controllerBreadcrumbs.init();