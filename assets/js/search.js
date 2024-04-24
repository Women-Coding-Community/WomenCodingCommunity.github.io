const controllerSearch = (function(jQuery) {
    const MENTOR_TYPE_BOTH = 'both';
    const HIDE_CLASS = 'd-none';
    const MENTOR_CARD = '#mentor-card-';
    const MENTOR_CARD_HIDDEN = '.card.d-none';
    const DEACTIVATED_MENTOR = '.inactive-mentor';
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
    const totalMentors = jQuery('.card').length + jQuery(DEACTIVATED_MENTOR).length;
    const activeMentors = jQuery('.card').length;
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
    
    const showMentorCard = function(index) {
        jQuery(MENTOR_CARD+index).removeClass(HIDE_CLASS);

        if (!$emptyMsg.hasClass(HIDE_CLASS)) {
            applyMentorsMsg();
        }
    };

    const applyMentorsMsg = function() {
        $emptyMsg.addClass(HIDE_CLASS);
        $descriptionMsg.removeClass(HIDE_CLASS);
    };
    
    const hideMentorCard = function(index) {
        jQuery(MENTOR_CARD+index).addClass(HIDE_CLASS);

        if ((jQuery(MENTOR_CARD_HIDDEN).length + jQuery(DEACTIVATED_MENTOR).length) === totalMentors && $emptyMsg.hasClass(HIDE_CLASS)) {
            $emptyMsg.removeClass(HIDE_CLASS);
            $descriptionMsg.addClass(HIDE_CLASS);
        }
    };
    
    const paramToFilter = function(key, value) {
        return {
            'key': key,
            'value': value.toLowerCase()
        };
    };

    const experienceFilter = function(key, value, min, max) {
        return {
            'key': key,
            'value': value.toLowerCase(),
            'min': min,
            'max': max
        };
    };

    const applyKeywordsParam = function() {
        const keywords = params.get([Filter.KEYWORDS]);
        
        if (keywords) {
            const filter = paramToFilter(Filter.KEYWORDS, keywords);
            $keywords.val(keywords);
            filterMentors([filter]);
        }
    };

    const applyFilters = function() {
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

    const removeFilters = function(){
        jQuery(MENTOR_CARD_HIDDEN).removeClass(HIDE_CLASS);
        applyMentorsMsg();

        $keywords.val('');
        $area.val('');
        $focus.val('');
        $type.val('');
        $experience.val('');
        setNumberOfMentors(activeMentors);
    };

    const filterMentors = function(filters) {
        if (isDefined(filters)) {
            resetFilteredMentors();
            for (let index = 1; index <= totalMentors; index++) {
                applyMentorFilters(index, filters);
            }
            setNumberOfMentors(filteredMentors);      
        }
    }

    const applyMentorFilters = function(index, filters) {
        const mentorCardId = MENTOR_CARD+index;
        const mentor = jQuery(mentorCardId);
        if (isDefined(mentor)) {
            if (hasFilters(mentorCardId, filters)) {
                filteredMentors++;
                showMentorCard(index);
            } else {
                hideMentorCard(index);
            } 
        }
    };

    const hasFilters = function(mentorCardId, filters) {
        let hasFilter = 0;
        for(let i = 0; i < filters.length; i++) {
            const filter = filters[i];
            // input id example: #mentor-card-9 input[name='bio'] 
            const inputHiddenId = mentorCardId + filterInputMap.get(filter.key);
            const inputHidden = jQuery(inputHiddenId);

            if (filter.key === Filter.EXPERIENCE) {
                const min = filter.min;
                const max = filter.max;
                if (isDefined(inputHidden) &&  parseInt(inputHidden.val()) >= min && parseInt(inputHidden.val()) <= max) {
                    hasFilter++;
                }

            } else if (filter.key === Filter.TYPE) {
                if (isDefined(inputHidden) && (inputHidden.val() === filter.value || inputHidden.val() === MENTOR_TYPE_BOTH)) {
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

    const containsFilter = function(input, value){
        return input.val().indexOf(value) > -1
    };

    const isDefined = function(element) {
        return element.length > 0
    };

    const initEvents = function() {
        $keywords.change(function() {
            applyFilters();
        });

        $area.change(function() {
            applyFilters();
        });

        $focus.change(function() {
            applyFilters();
        });
        
        $experience.change(function() {
            applyFilters();
        });
        
        $type.change(function() {
            applyFilters();
        });

        $form.submit(function(e){
            return false;
        }); 

        $searchBtn.click(function() {
            applyFilters();
        }); 

        $clearBtn.click(function() {
            removeFilters();
        }); 

        $toggleFilterBtn.click(function() { 
            $clearBtn.toggleClass(HIDE_CLASS);
            jQuery('#toggle-container').toggleClass('mt-5');
            jQuery('#filters-container').toggleClass(HIDE_CLASS);
        });
    };

    const init = function() {
        setNumberOfMentors(activeMentors);
        initEvents();
        applyKeywordsParam();
    };

    return {
        init: init
    };

}(jQuery));

controllerSearch.init();
