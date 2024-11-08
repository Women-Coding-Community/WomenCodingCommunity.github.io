var controllerHome = (function (jQuery) {
  const CONSENT = 'consentGiven';
  const GTAG_ID = 'G-3V6VPT445S';
  const DENIED = 'denied';
  const GRANTED = 'granted';
  const CONSENT_UPDATE = 'consent_update';

  const $consentBanner = jQuery('#consent-banner');
  const $acceptCookiesButton = jQuery('#accept-cookies');
  const $denyCookiesButton = jQuery('#deny-cookies');
  
  const adjustHomeLink = function () {
    if (document.location.hostname === 'localhost') {
      jQuery('.navbar-brand').attr('href', '/');
      jQuery('#nav-0').attr('href', '/');
    }
  };

  const initializeConsentMode = function () {
    window.dataLayer = window.dataLayer || [];
    const gtag = function() {
      window.dataLayer.push(arguments);
    }
    gtag(CONSENT, 'default', {
      ad_storage: DENIED,
      analytics_storage: DENIED,
    });
  };

  // Function to enable Google Analytics
  const enableAnalytics = function () {
    if (localStorage.getItem(CONSENT)) {
      window.dataLayer = window.dataLayer || [];
      function gtag() {
        window.dataLayer.push(arguments);
      }
      gtag('js', new Date());
      gtag('config', GTAG_ID);
    }
  };

   const displayConsentBanner = function () {
    if (!localStorage.getItem(CONSENT)) {
      $consentBanner.show();
    }
  };

  const acceptCookies = function () {
    localStorage.setItem(CONSENT, true);
    $consentBanner.hide();
    enableAnalytics();
    window.dataLayer.push({
      event: CONSENT_UPDATE,
      ad_storage: GRANTED,
      analytics_storage: GRANTED,
    });
  };

  const denyCookies = function () {
    localStorage.setItem(CONSENT, false);
    $consentBanner.hide();
    window.dataLayer.push({
      event: CONSENT_UPDATE,
      ad_storage: DENIED,
      analytics_storage: DENIED,
    });
  };

  const initPage = function () {
    initializeConsentMode();
    displayConsentBanner();
    enableAnalytics();
  };

  const initEvents = function () {
    jQuery($acceptCookiesButton).on('click', function (e) {
      e.preventDefault();
      acceptCookies();
    });

    jQuery($denyCookiesButton).on('click', function (e) {
      e.preventDefault();
      denyCookies();
    });
  };

  const init = function () {
    adjustHomeLink();
    initPage();
    initEvents();
  };

  return {
    init: init,
  };
})(jQuery);

controllerHome.init();
