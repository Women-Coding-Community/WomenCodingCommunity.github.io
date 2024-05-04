var ajaxController = (function(jQuery) {
    const requestData = function() {
        $.ajax({
            url: "https://api.restful-api.dev/objects/7",
            method: "GET",
            success: function(response) {
                console.log("GET request successful");
                console.log(response);
            },
            error: function(xhr, status, error) {
                console.error("Error making GET request:", status, error);
            }
        });
    };

    return {
        init: requestData
    };

}(jQuery));

ajaxController.init();
