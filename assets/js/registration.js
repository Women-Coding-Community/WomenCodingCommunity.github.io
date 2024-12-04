const registrationController = (function(jQuery) {
    const CLASS_HIDDEN = 'd-none';
    const MENTORSHIP_OPEN_MONTH = 3; //March
    const MENTORSHIP_CLOSE_MONTH = 11; //November

    const checkAdHocSessions = function() {
        jQuery('.card-mentor').each(function() {
            const mentorIndex = jQuery(this).data('index');
            const mentorInfo = jQuery(`#mentor-info-${mentorIndex}`);
            
            if (mentorInfo) {
                const mentorAvailability = mentorInfo.data('availability').toString().split(',');
                const mentorType = mentorInfo.data('type');
                const daysOpen = parseInt(mentorInfo.data('days-open'));
    
                const currentDate = new Date();
                const currentDay = currentDate.getDate();
                const currentMonth = currentDate.getMonth() + 1;

                const isMentorshipCycle = (
                    currentMonth >= MENTORSHIP_OPEN_MONTH && 
                    currentMonth <= MENTORSHIP_CLOSE_MONTH
                );
                
                if (currentDay <= daysOpen && isMentorshipCycle) {
                    if (mentorType !== 'long-term') {
                        if (mentorAvailability.includes(currentMonth.toString())) {
                            jQuery(`#registration-link-${mentorIndex}`).removeClass(CLASS_HIDDEN);
                        } else {
                            jQuery(`#adhoc-unavailable-${mentorIndex}`).removeClass(CLASS_HIDDEN);
                        }
                    } else {
                        jQuery(`#long-term-only-${mentorIndex}`).removeClass(CLASS_HIDDEN);
                    }
                }
            }
        });
    }

    const init = function() {
        checkAdHocSessions();
    };

    return {
        init: init
    };

}(jQuery));

registrationController.init();
