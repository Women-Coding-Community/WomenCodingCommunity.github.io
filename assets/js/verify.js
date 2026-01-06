let controllerVerify = (function (jQuery) {
    const certIdInput = jQuery('#certId');
    const loading = jQuery('#loading');
    const result = jQuery('#result');
    const verifyBtn = jQuery('#verify-btn');

    /**
     * Parse URL parameters
     * @param {string} name - Parameter name to retrieve
     * @returns {string} - Parameter value or empty string
     */
    let getUrlParameter = function (name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        const results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    };

    /**
     * Display loading state
     */
    let showLoading = function () {
        loading.show();
        result.html('');
    };

    /**
     * Hide loading state
     */
    let hideLoading = function () {
        loading.hide();
    };

    /**
     * Display valid certificate information
     * @param {object} certificate - Certificate data object
     */
    let displayValidCertificate = function (certificate) {
        const certType = certificate.type.charAt(0).toUpperCase() + certificate.type.slice(1);

        result.html(`
            <div class="success-icon">✓</div>
            <div class="certificate-info">
                <h3>Valid Certificate</h3>
                <div class="info-row">
                    <span class="info-label">Certificate ID:</span>
                    <span class="info-value">${certificate.id}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Recipient Name:</span>
                    <span class="info-value">${certificate.name}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Certificate Type:</span>
                    <span class="info-value">${certType}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Issue Date:</span>
                    <span class="info-value">${certificate.issue_date}</span>
                </div>
            </div>
        `);
    };

    /**
     * Display invalid certificate message
     * @param {string} certId - Certificate ID that was searched
     */
    let displayInvalidCertificate = function (certId) {
        result.html(`
            <div class="error-icon">✗</div>
            <div class="certificate-info invalid">
                <h3>Invalid Certificate</h3>
                <p>No certificate found with ID: <strong>${certId}</strong></p>
                <p>This certificate may be fraudulent or the ID was entered incorrectly.</p>
            </div>
        `);
    };

    /**
     * Display error message
     * @param {string} errorMessage - Error message to display
     */
    let displayError = function (errorMessage) {
        result.html(`
            <p class="error-message">Error verifying certificate: ${errorMessage}</p>
            <p>Please try again later or contact support.</p>
        `);
    };

    /**
     * Verify certificate by ID
     */
    let verifyCertificate = async function () {
        const certId = certIdInput.val().trim().toUpperCase();

        if (!certId) {
            result.html('<p class="error-message">Please enter a certificate ID</p>');
            return;
        }

        showLoading();

        try {
            const response = await fetch('/assets/js/certificates_registry.json');

            if (!response.ok) {
                throw new Error('Unable to load certificate registry');
            }

            const registry = await response.json();
            const certificate = registry.certificates.find(cert => cert.id === certId);

            hideLoading();

            if (certificate) {
                displayValidCertificate(certificate);
            } else {
                displayInvalidCertificate(certId);
            }
        } catch (error) {
            hideLoading();
            displayError(error.message);
        }
    };

    /**
     * Auto-verify if cert ID is in URL
     */
    let autoVerifyFromUrl = function () {
        const certId = getUrlParameter('cert');
        if (certId) {
            certIdInput.val(certId);
            verifyCertificate();
        }
    };

    /**
     * Initialize event handlers
     */
    let initEvents = function () {
        // Verify button click
        verifyBtn.click(function (e) {
            e.preventDefault();
            verifyCertificate();
        });

        // Allow Enter key to trigger verification
        certIdInput.keypress(function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                verifyCertificate();
            }
        });
    };

    /**
     * Initialize the controller
     */
    let init = function () {
        // Only initialize if we're on the verify page
        if (certIdInput.length === 0) {
            return;
        }

        initEvents();
        autoVerifyFromUrl();
    };

    return {
        init: init
    };
}(jQuery));

controllerVerify.init();
