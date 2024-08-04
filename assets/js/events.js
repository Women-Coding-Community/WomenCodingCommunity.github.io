const eventsScript = (function(jQuery) {
    const pastEventsTab = jQuery('#tab-past-events');
    const upcomingEventsTab = jQuery('#tab-upcoming-events');

    const CLASS_ACTIVE = 'active';
    const CLASS_HIDDEN = 'd-none';

    const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');

    const showFeaturedEvents = function() {
        const sortedEventsAscending = jQuery('#featured-events .event-card');

        sortedEventsAscending.sort(function(a, b) {
            return jQuery(a).data('expiration') - jQuery(b).data('expiration');
        });

        let validEventCount = 0;
        sortedEventsAscending.each(function() {
            const expiration = jQuery(this).data('expiration');
            if (expiration >= today) {
                if (validEventCount < 2) {
                    jQuery(this).addClass(CLASS_ACTIVE);
                    validEventCount++;
                } else {
                    jQuery(this).addClass(CLASS_HIDDEN);
                }
            } else {
                jQuery(this).addClass(CLASS_HIDDEN);
            }
        });

    }

    const showUpcomingEvents = function() {
        const sortedEventsAscending = jQuery('#upcoming-events .event-card').sort(function(a, b) {
            return jQuery(a).data('expiration') - jQuery(b).data('expiration');
        });

        sortedEventsAscending.each(function() {
            const expiration = jQuery(this).data('expiration');
            if (expiration < today) {
                jQuery(this).addClass(CLASS_HIDDEN);
            }
        });

        jQuery('#tab-past-events').removeClass(CLASS_ACTIVE);
        jQuery('#tab-upcoming-events').addClass(CLASS_ACTIVE);

        jQuery('#past-events').addClass(CLASS_HIDDEN);
        jQuery('#upcoming-events').removeClass(CLASS_HIDDEN);
    }

    const showPastEvents = function() {
        const sortedEventsDescending = jQuery('#past-events .event-card').sort(function(a, b) {
            return jQuery(b).data('expiration') - jQuery(a).data('expiration');
        });

        sortedEventsDescending.each(function() {
            const expiration = jQuery(this).data('expiration');
            if (expiration >= today) {
                jQuery(this).addClass(CLASS_HIDDEN);
            }
        });

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
        showFeaturedEvents();

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
