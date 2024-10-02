var controllerMentors = (function (jQuery) {
    var skillsButton = jQuery('.skills');
    var presentationButton = jQuery('.presentation');
    var menteesButton = jQuery('.mentees');
    let reviewsButton = jQuery('.reviews');
    let resourcesButton = jQuery('.mentor-resources');
    var tooltip = jQuery('[data-toggle="tooltip"]');
    var toggleContent = jQuery('.toggle-content');
    var copyLink = jQuery('.copy-link');


    const CLASS_ACTIVE = 'active';
    const CLASS_HIDDEN = 'd-none';
    const TOGGLE_CONTENT = 'content-overflow';
    const CONTENT = {
        'SHOW_MORE': 'Show more',
        'SHOW_LESS': 'Show less'
    }

    const trackMentorEvents = function (index, eventName) {
        const mentorName = index + ": " + jQuery("#mentor-card-" + index + " input[name='mentor-name']").val();
        if (window.gtag) {
            gtag('event', 'view', {
                'event_category': 'MentorView',
                'event_label': eventName,
                'value': mentorName
            });
        }
    };

    var showPresentation = function (index) {
        jQuery("#bt-p-" + index).addClass(CLASS_ACTIVE);
        jQuery("#bt-s-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-m-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-v-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-r-" + index).removeClass(CLASS_ACTIVE);

        jQuery("#presentation-" + index).removeClass(CLASS_HIDDEN);
        jQuery("#skills-" + index).addClass(CLASS_HIDDEN);
        jQuery("#mentees-" + index).addClass(CLASS_HIDDEN);
        jQuery("#reviews-" + index).addClass(CLASS_HIDDEN);
        jQuery("#mentor-resources-" + index).addClass(CLASS_HIDDEN);

        jQuery('.card-presentation').each(function () {
            let mentorIndex = '#card-text-' + jQuery(this).data('index');
            let btnShowMoreId = '#btn-show-more-' + jQuery(this).data('index');

            let cardHeight = jQuery(mentorIndex).prop('scrollHeight');
            let clientHeight = jQuery(mentorIndex).prop('clientHeight');

            if (cardHeight <= clientHeight) {
                jQuery(btnShowMoreId).addClass(CLASS_HIDDEN);
            }
        }
        );
    }

    var showSkills = function (index) {
        jQuery("#bt-s-" + index).addClass(CLASS_ACTIVE);
        jQuery("#bt-p-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-m-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-v-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-r-" + index).removeClass(CLASS_ACTIVE);

        jQuery("#presentation-" + index).addClass(CLASS_HIDDEN);
        jQuery("#mentees-" + index).addClass(CLASS_HIDDEN);
        jQuery("#skills-" + index).removeClass(CLASS_HIDDEN);
        jQuery("#reviews-" + index).addClass(CLASS_HIDDEN);
        jQuery("#mentor-resources-" + index).addClass(CLASS_HIDDEN);
    }

    var showMenteesData = function (index) {
        jQuery("#bt-m-" + index).addClass(CLASS_ACTIVE);
        jQuery("#bt-p-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-s-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-v-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-r-" + index).removeClass(CLASS_ACTIVE);

        jQuery("#mentees-" + index).removeClass(CLASS_HIDDEN);
        jQuery("#presentation-" + index).addClass(CLASS_HIDDEN);
        jQuery("#skills-" + index).addClass(CLASS_HIDDEN);
        jQuery("#reviews-" + index).addClass(CLASS_HIDDEN);
        jQuery("#mentor-resources-" + index).addClass(CLASS_HIDDEN);
    }

    var showReviewsData = function (index) {
        jQuery("#bt-m-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-p-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-s-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-v-" + index).addClass(CLASS_ACTIVE);
        jQuery("#bt-r-" + index).removeClass(CLASS_ACTIVE);

        jQuery("#mentees-" + index).addClass(CLASS_HIDDEN);
        jQuery("#presentation-" + index).addClass(CLASS_HIDDEN);
        jQuery("#skills-" + index).addClass(CLASS_HIDDEN);
        jQuery("#reviews-" + index).removeClass(CLASS_HIDDEN);
        jQuery("#mentor-resources-" + index).addClass(CLASS_HIDDEN);
    }

    var showResourcesData = function (index) {
        jQuery("#bt-m-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-p-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-s-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-v-" + index).removeClass(CLASS_ACTIVE);
        jQuery("#bt-r-" + index).addClass(CLASS_ACTIVE);

        jQuery("#mentees-" + index).addClass(CLASS_HIDDEN);
        jQuery("#presentation-" + index).addClass(CLASS_HIDDEN);
        jQuery("#skills-" + index).addClass(CLASS_HIDDEN);
        jQuery("#reviews-" + index).addClass(CLASS_HIDDEN);
        jQuery("#mentor-resources-" + index).removeClass(CLASS_HIDDEN);
    }

    var init = function () {
        initEvents();
        showPresentation();
        tooltip.tooltip();
    };

    var initEvents = function () {
        jQuery(skillsButton).on('click', function (e) {
            const index = jQuery(this).data('index');
            trackMentorEvents(index, 'showSkills');
            showSkills(index);
        });

        jQuery(presentationButton).on('click', function (e) {
            const index = jQuery(this).data('index');
            trackMentorEvents(index, 'showPresentation');
            showPresentation(index);
        });

        jQuery(menteesButton).on('click', function (e) {
            const index = jQuery(this).data('index');
            trackMentorEvents(index, 'showMentee');
            showMenteesData(index);
        });

        jQuery(reviewsButton).on('click', function (e) {
            const index = jQuery(this).data('index');
            trackMentorEvents(index, 'showReviews');
            showReviewsData(index);
        });

        jQuery(resourcesButton).on('click', function (e) {
            const index = jQuery(this).data('index');
            trackMentorEvents(index, 'showResources');
            showResourcesData(index);
        });

        jQuery(toggleContent).on('click', function (e) {
            jQuery(this).prev().toggleClass(TOGGLE_CONTENT);

            const index = jQuery(this).data('index');

            if (jQuery(this).text() === CONTENT.SHOW_MORE) {
                trackMentorEvents(index, 'showLess');
                jQuery(this).text(CONTENT.SHOW_LESS);
            } else {
                trackMentorEvents(index, 'showMore');
                jQuery(this).text(CONTENT.SHOW_MORE);
            }
        });

        jQuery(copyLink).on('click', function (e) {
            var text = jQuery(this).data("url");
            var tempInput = jQuery("<input>");
            jQuery("body").append(tempInput);
            tempInput.val(text).select();
            document.execCommand("copy");
            tempInput.remove();

            var mentorContainer = jQuery(this).closest('.mentor-container');
            var linkCopiedAlert = mentorContainer.find('.link-copied-alert')

            linkCopiedAlert.removeClass(CLASS_HIDDEN);
            setTimeout(function () {
                linkCopiedAlert.addClass(CLASS_HIDDEN);
            }, 1000);
        });
    };

    return {
        init: init
    };

}(jQuery));

controllerMentors.init();
