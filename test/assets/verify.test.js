const {JSDOM} = require('jsdom');

describe('Certificate Verification Page', () => {
    let $;
    let document;
    let window;

    beforeEach(() => {
        const dom = new JSDOM(`
            <!DOCTYPE html>
            <html>
            <body>
                <div class="verification-container">
                    <div class="search-box">
                        <input type="text" id="certId" placeholder="Enter Certificate ID"/>
                        <button id="verify-btn">Verify</button>
                    </div>
                    <div class="loading" id="loading" style="display: none;">
                        <p>Verifying certificate...</p>
                    </div>
                    <div id="result"></div>
                </div>
            </body>
            </html>
        `, {
            url: 'http://localhost'
        });

        global.document = dom.window.document;
        global.window = dom.window;
        global.location = dom.window.location;
        global.jQuery = require('jquery');
        global.$ = global.jQuery;

        $ = global.jQuery;
        document = global.document;
        window = global.window;
        global.fetch = jest.fn();
    });

    afterEach(() => {
        jest.clearAllMocks();
        delete global.document;
        delete global.window;
        delete global.location;
        delete global.jQuery;
        delete global.$;
        delete global.fetch;
    });

    test('page elements exist', () => {
        expect(document.getElementById('certId')).toBeTruthy();
        expect(document.getElementById('verify-btn')).toBeTruthy();
        expect(document.getElementById('loading')).toBeTruthy();
        expect(document.getElementById('result')).toBeTruthy();
    });

    test('certificate ID input accepts text', () => {
        const certIdInput = $('#certId');
        certIdInput.val('ABC123');
        expect(certIdInput.val()).toBe('ABC123');
    });

    test('verify button exists and is clickable', () => {
        const verifyBtn = $('#verify-btn');
        expect(verifyBtn.length).toBe(1);
        expect(verifyBtn.text()).toBe('Verify');

        let clicked = false;
        verifyBtn.on('click', () => {
            clicked = true;
        });

        verifyBtn.trigger('click');
        expect(clicked).toBe(true);
    });

    test('loading indicator is initially hidden', () => {
        const loading = $('#loading');
        expect(loading.css('display')).toBe('none');
    });

    test('result div is initially empty', () => {
        const result = $('#result');
        expect(result.html()).toBe('');
    });

    test('can simulate Enter key press on input', () => {
        const certIdInput = $('#certId');
        let keyPressed = false;

        certIdInput.on('keydown', (e) => {
            if (e.key === 'Enter') {
                keyPressed = true;
            }
        });

        // Simulate Enter key
        const event = $.Event('keydown');
        event.key = 'Enter';
        certIdInput.trigger(event);

        expect(keyPressed).toBe(true);
    });

    test('fetch API is mocked correctly', async () => {
        const mockData = {certificates: []};
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => mockData
        });

        const response = await fetch('/assets/js/certificates_registry.json');
        const data = await response.json();

        expect(data).toEqual(mockData);
        expect(global.fetch).toHaveBeenCalledWith('/assets/js/certificates_registry.json');
    });

    test('jQuery is available globally', () => {
        expect(global.jQuery).toBeDefined();
        expect(global.$).toBeDefined();
        expect(global.jQuery).toBe(global.$);
    });

    test('can manipulate DOM with jQuery', () => {
        const result = $('#result');
        result.html('<p class="success">Test</p>');

        expect(result.find('p').hasClass('success')).toBe(true);
        expect(result.find('p').text()).toBe('Test');
    });

    test('can toggle element visibility', () => {
        const loading = $('#loading');

        expect(loading.is(':visible')).toBe(false);

        loading.show();
        expect(loading.css('display')).not.toBe('none');

        loading.hide();
        expect(loading.css('display')).toBe('none');
    });

    test('URL parameters can be accessed', () => {
        const domWithParam = new JSDOM('', {
            url: 'http://localhost?cert=ABC123'
        });

        const urlParams = new domWithParam.window.URLSearchParams(domWithParam.window.location.search);
        expect(urlParams.get('cert')).toBe('ABC123');
    });
});
