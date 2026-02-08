const controllerSearch = (function (jQuery) {
    const MENTOR_TYPE_BOTH = 'both';
    const HIDE_CLASS = 'd-none';
    const MENTOR_CARD_HIDDEN = '.card-mentor.d-none';
    const Filter = {
        KEYWORDS: 'keywords',
        EXPERIENCE: 'exp',
        TYPE: 'type'
    }

    const filterInputMap = new Map([
        [Filter.KEYWORDS, " input[name='mentor-data']"],
        [Filter.TYPE, " input[name='mentor-type']"],
        [Filter.EXPERIENCE, " input[name='exp']"],
    ]);

    const params = new URLSearchParams(window.location.search);
    const activeMentors = jQuery('.card-mentor').length;
    let filteredMentors = 0;

    const $keywords = jQuery('#keywords');
    const $area = jQuery('#area');
    const $experience = jQuery('#experience');
    const $focus = jQuery('#focus');
    const $type = jQuery('#type');
    const $form = jQuery('.mentor-filter');
    const $emptyMsg = jQuery('#no-mentors-msg');
    const $descriptionMsg = jQuery('.description');
    const $searchBtn = jQuery('#search');
    const $clearBtn = jQuery('#clear-btn');
    const $toggleFilterBtn = jQuery('#toggle-filters');
    const $numberOfMentorsDisplay = jQuery('#total-mentors');

    const showMentorCard = function (mentorSelector) {
        jQuery(mentorSelector).removeClass(HIDE_CLASS);

        if (!$emptyMsg.hasClass(HIDE_CLASS)) {
            applyMentorsMsg();
        }
    };

    const applyMentorsMsg = function () {
        $emptyMsg.addClass(HIDE_CLASS);
        $descriptionMsg.removeClass(HIDE_CLASS);
    };

    const hideMentorCard = function (mentorSelector) {
        jQuery(mentorSelector).addClass(HIDE_CLASS);

        if ((jQuery(MENTOR_CARD_HIDDEN).length) === activeMentors && $emptyMsg.hasClass(HIDE_CLASS)) {
            $emptyMsg.removeClass(HIDE_CLASS);
            $descriptionMsg.addClass(HIDE_CLASS);
        }
    };

    const paramToFilter = function (key, value) {
        return {
            'key': key,
            'value': value.toLowerCase()
        };
    };

    const experienceFilter = function (key, value, min, max) {
        return {
            'key': key,
            'value': value.toLowerCase(),
            'min': min,
            'max': max
        };
    };

    const applyKeywordsParam = function () {
        const keywords = params.get(Filter.KEYWORDS);

        if (keywords) {
            const filter = paramToFilter(Filter.KEYWORDS, keywords);
            $keywords.val(keywords);
            filterMentors([filter]);
        }
    };

    const trackSearchTerms = function (filters) {
        let searchTerms = filters.map(filter => `${filter.key}: ${filter.value}`).join(', ');
        if (window.gtag) {
            gtag('event', 'search', {
                'event_category': 'Mentor Search',
                'event_label': searchTerms,
                'value': filteredMentors
            });
        }
    };

    const applyFilters = function () {
        let filters = [];

        if ($keywords.val()) {
            filters.push(paramToFilter(Filter.KEYWORDS, $keywords.val()));
        }

        if ($area.val()) {
            filters.push(paramToFilter(Filter.KEYWORDS, $area.val()));
        }

        if ($focus.val()) {
            filters.push(paramToFilter(Filter.KEYWORDS, $focus.val()));
        }

        if ($type.val()) {
            filters.push(paramToFilter(Filter.TYPE, $type.val()));
        }

        if ($experience.val()) {
            const min = $experience.find(':selected').data('min');
            const max = $experience.find(':selected').data('max');
            filters.push(experienceFilter(Filter.EXPERIENCE, $experience.val(), min, max));
        }

        if (isDefined(filters)) {
            filterMentors(filters);
            toggleClearBtn(filters.length > 0);
            trackSearchTerms(filters);
        } else {
            removeFilters();
        }
    };

    const setNumberOfMentors = (val) => {
        $numberOfMentorsDisplay.text(val);
    }

    const resetFilteredMentors = () => {
        filteredMentors = 0;
    }

    const removeFilters = function () {
        jQuery(MENTOR_CARD_HIDDEN).removeClass(HIDE_CLASS);
        applyMentorsMsg();

        $keywords.val('');
        $area.val('');
        $focus.val('');
        $type.val('');
        $experience.val('');
        setNumberOfMentors(activeMentors);
        toggleClearBtn(false);
    };

    const filterMentors = function (filters) {
        if (isDefined(filters)) {
            resetFilteredMentors();
            jQuery('.card-mentor').each(function () {
                const id = jQuery(this).attr('id');
                if (id) {
                    const mentorSelector = '#' + id;
                    applyMentorFilters(mentorSelector, filters);
                }
            });
            setNumberOfMentors(filteredMentors);
        }
    }

    const applyMentorFilters = function (mentorSelector, filters) {
        const mentor = jQuery(mentorSelector);
        if (isDefined(mentor)) {
            if (hasFilters(mentorSelector, filters)) {
                filteredMentors++;
                showMentorCard(mentorSelector);
            } else {
                hideMentorCard(mentorSelector);
            }
        }
    };

    const hasFilters = function (mentorCardId, filters) {
        let hasFilter = 0;
        for (let i = 0; i < filters.length; i++) {
            const filter = filters[i];
            // input id example: #mentor-card-9 input[name='bio'] 
            const inputHiddenId = mentorCardId + filterInputMap.get(filter.key);
            const inputHidden = jQuery(inputHiddenId);

            if (filter.key === Filter.EXPERIENCE) {
                const min = Number(filter.min);
                const max = Number(filter.max);
                const val = parseInt(inputHidden.val(), 10);
                if (isDefined(inputHidden) && !isNaN(val) && val >= min && val <= max) {
                    hasFilter++;
                }

            } else if (filter.key === Filter.TYPE) {
                const typeVal = String(inputHidden.val()).toLowerCase();
                if (isDefined(inputHidden) && (typeVal === filter.value || typeVal === MENTOR_TYPE_BOTH)) {
                    hasFilter++;
                }

            } else {
                //keywords
                if (isDefined(inputHidden) && containsFilter(inputHidden, filter.value)) {
                    hasFilter++;
                }
            }

        }

        return hasFilter === filters.length;
    }

    const containsFilter = function (input, value) {
        return input.val().toLowerCase().indexOf(value) > -1
    };

    const isDefined = function (element) {
        return element.length > 0
    };

    const toggleClearBtn = function (show) {
        if (show) {
            $clearBtn.removeClass(HIDE_CLASS);
        } else {
            $clearBtn.addClass(HIDE_CLASS);
        }
    };

    const initEvents = function () {
        $keywords.change(function () {
            applyFilters();
        });

        $area.change(function () {
            applyFilters();
        });

        $focus.change(function () {
            applyFilters();
        });

        $experience.change(function () {
            applyFilters();
        });

        $type.change(function () {
            applyFilters();
        });

        $form.submit(function (e) {
            return false;
        });

        $searchBtn.click(function () {
            applyFilters();
        });

        $clearBtn.click(function () {
            removeFilters();
        });

        $toggleFilterBtn.click(function () {
            jQuery('#filters-container').toggleClass(HIDE_CLASS);
        });
    };

    const init = function () {
        setNumberOfMentors(activeMentors);
        initEvents();
        applyKeywordsParam();
        toggleClearBtn(false);
    };

    return {
        init: init
    };

}(jQuery));

controllerSearch.init();
