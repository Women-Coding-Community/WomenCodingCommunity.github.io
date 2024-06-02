const eventsScript = (function(jQuery) {
    const pastEventsTab = jQuery('#tab-past-events');
    const upcomingEventsTab = jQuery('#tab-upcoming-events');

    const CLASS_ACTIVE = 'active';
    const CLASS_HIDDEN = 'd-none';

    const showUpcomingEvents = function() {
        jQuery('#tab-past-events').removeClass(CLASS_ACTIVE);
        jQuery('#tab-upcoming-events').addClass(CLASS_ACTIVE);

        jQuery('#past-events').addClass(CLASS_HIDDEN);
        jQuery('#upcoming-events').removeClass(CLASS_HIDDEN);
    }

    const showPastEvents = function() {
        jQuery('#tab-past-events').addClass(CLASS_ACTIVE);
        jQuery('#tab-upcoming-events').removeClass(CLASS_ACTIVE);

        jQuery('#past-events').removeClass(CLASS_HIDDEN);
        jQuery('#upcoming-events').addClass(CLASS_HIDDEN);
    }

    const init = function() {
        initEvents();
        showUpcomingEvents();
    };

    const initEvents = function() {
        pastEventsTab.click(function() {
            showPastEvents(jQuery(this));
        });

        upcomingEventsTab.click(function() {
            showUpcomingEvents(jQuery(this));
        });  
    };

    return {
        init: init
    };

}(jQuery));

eventsScript.init();
