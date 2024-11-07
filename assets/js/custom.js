var controllerHome = (function (jQuery) {
  const CONSENT = 'consentGiven';
  const consentBanner = jQuery("#consent-banner");
  const acceptCookiesButton = jQuery("#accept-cookies");
  const denyCookiesButton = jQuery("#deny-cookies");
  const gtagId = "{{ site.gtagId }}";

  var adjustHomeLink = function () {
    if (document.location.hostname === "localhost") {
      jQuery(".navbar-brand").attr("href", "/");
      jQuery("#nav-0").attr("href", "/");
    }
  };

  let initializeConsentMode = function () {
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      window.dataLayer.push(arguments);
    }
    gtag("consent", "default", {
      ad_storage: "denied",
      analytics_storage: "denied",
    });
  };

  // Function to enable Google Analytics
  let enableAnalytics = function () {
    if (localStorage.getItem(CONSENT) === "true") {
      window.dataLayer = window.dataLayer || [];
      function gtag() {
        window.dataLayer.push(arguments);
      }
      gtag("js", new Date());
      gtag("config", gtagId);
    }
  };

 
  let displayConsentBanner = function () {
    if (!localStorage.getItem(CONSENT)) {
      consentBanner.show();
    }
  };

  
  let acceptCookies = function () {
    localStorage.setItem(CONSENT, true);
    consentBanner.hide();
    enableAnalytics();
    window.dataLayer.push({
      event: "consent_update",
      ad_storage: "granted",
      analytics_storage: "granted",
    });
  };

  
  let denyCookies = function () {
    localStorage.setItem(CONSENT, false);
    consentBanner.hide();
    window.dataLayer.push({
      event: "consent_update",
      ad_storage: "denied",
      analytics_storage: "denied",
    });
  };

  
  let initPage = function () {
    initializeConsentMode();
    displayConsentBanner();
    enableAnalytics();
  };

  let initEvents = function () {
    jQuery(acceptCookiesButton).on('click',function (e) {
      e.preventDefault();
      acceptCookies();
    });

  

    jQuery(denyCookiesButton).on('click', function (e) {
      e.preventDefault();
      denyCookies();
    });
  };

  let init = function () {
    adjustHomeLink();
    initPage();
    initEvents();
  };

  return {
    init: init,
  };
})(jQuery);

controllerHome.init();
