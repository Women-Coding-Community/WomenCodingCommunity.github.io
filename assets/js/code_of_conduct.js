let controllerCodeOfConduct = (function(jQuery) {
    const menteeConduct = jQuery('#mentee-conduct');
    const mentorConduct = jQuery('#mentor-conduct');

    const btnMenteeLearnMore = jQuery('#btn-mentee-learn-more');
    const btnMentorLearnMore = jQuery('#btn-mentor-learn-more');
    const btnHideMenteesShowLess = jQuery('#btn-mentee-show-less');
    const btnHideMentorShowLess = jQuery('#btn-mentor-show-less');

    const menteeHeading = jQuery('#mentee-section');
    const mentorHeading = jQuery('#mentor-section');

    const classHide = 'd-none';

    let menteeCodeConduct = function() {
        menteeConduct.removeClass(classHide);
        btnHideMenteesShowLess.removeClass(classHide);
        btnMenteeLearnMore.addClass(classHide);
    }

    let mentorCodeConduct = function() {
        mentorConduct.removeClass(classHide);
        btnHideMentorShowLess.removeClass(classHide);
        btnMentorLearnMore.addClass(classHide);
    }

    let initPage = function() {
        btnHideMenteesShowLess.addClass(classHide);
        btnHideMentorShowLess.addClass(classHide);
        btnMenteeLearnMore.removeClass(classHide);
        btnMentorLearnMore.removeClass(classHide);

        mentorConduct.addClass(classHide);
        menteeConduct.addClass(classHide);
    };

    let init = function() {
        initEvents();
        initPage();
    };

    let scrollToTarget = function(target) {
        jQuery('html, body').animate({
            scrollTop: target.offset().top
        }, 1000);
    };

    let initEvents = function() {
        btnMenteeLearnMore.click(function(e) {
            e.preventDefault();
            menteeCodeConduct();
            scrollToTarget(menteeConduct);
        });

        btnMentorLearnMore.click(function(e) {
            e.preventDefault();
            mentorCodeConduct();
            scrollToTarget(mentorConduct);
        });

        btnHideMenteesShowLess.click(function(e) {
            e.preventDefault();
            initPage();
            scrollToTarget(menteeHeading);
        });

        btnHideMentorShowLess.click(function(e) {
            e.preventDefault();
            initPage();
            scrollToTarget(mentorHeading);
        });
    };

    return {
        init: init
    };
}(jQuery));

controllerCodeOfConduct.init();
