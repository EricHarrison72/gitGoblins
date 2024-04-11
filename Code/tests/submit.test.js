// -----------------------------
//submit.test.js
/*
Unit tests for submit.js
To run these tests, you need to have node.js and Jest installed.
Terminal command is `npm test`.

Written with some help from ChatGPT 4.
*/
// -----------------------------

// imports from submit.js
const {
    getDateFromSelection,
    getCityFromSelection,
    getStatFromSelection,
    reloadPageWithArgs
} = require('../weatherApp/static/js/submit.js');

describe('getDateFromSelection', () => {
//--------------------------------------

    // Mocks
    // -----
    document.getElementById = jest.fn().mockImplementation(id => {
        switch (id) {
            case 'yearSelect':
                return { value: "2017" };
            case 'monthSelect':
                return { value: "6" };
            case 'daySelect':
                return { value: "24" };

            case 'goblin_yearSelect':
                return { value: "2015" };
            case 'goblin_monthSelect':
                return { value: "10" };
            case 'goblin_daySelect':
                return { value: "2" };
            default:
                return null;
        }
    });

    // Tests
    // -----
    test('default', () => {
        expect(getDateFromSelection()).toBe('2017-06-24');
    });

    test('with special id_prefixes', () => {
        expect(getDateFromSelection('goblin_')).toBe('2015-10-02');
    });
});


describe('getCityFromSelection', () => {
//------------------------------------

    // Mocks
    // -----
    const documentGetElementByIdMock = (selectedIndex) => {
        document.getElementById = jest.fn().mockImplementation(id => {
            switch (id) {
                case 'citySelect':
                    return {
                        options: [{ text: 'Canberra' }, { text: 'Alice Springs' }],
                        selectedIndex: selectedIndex
                    };
                default:
                    return null;
            }
        });
};
    // Tests
    // -----
    test('get a one-word city from selection', () => {
        documentGetElementByIdMock(0);
        expect(getCityFromSelection()).toBe('Canberra');
    });

     test('get a two-word city from selection', () => {
        documentGetElementByIdMock(1);
        expect(getCityFromSelection()).toBe('AliceSprings');
     });
});

describe('getStatFromSelection', () => {
//--------------------------------------
    // Mocks
    // -----
    const documentGetElementByIdMock = (selectedIndex) => {
        document.getElementById = jest.fn().mockImplementation(id => {
            switch (id) {
                case 'statSelect':
                    return {
                        options: [{ text: 'wind' }],
                        selectedIndex: selectedIndex
                    };
                default:
                    return null;
            }
        });
    };
    // Tests
    // -----
    test('get a stat (string) from the stat selection menu', () => {
        documentGetElementByIdMock(0);
        expect(getStatFromSelection()).toBe('wind');
    });
});


describe('reloadPageWithArgs', () => {
//------------------------------------

    // Mocks Setup & Teardown
    // ----------------------
    const originalLocation = global.location;

    beforeEach(() => {
        delete global.location;
        global.location = { href: 'https://example.com/page' };
    });

    afterEach(() => {
        // Restore the original location object after each test
        global.location = originalLocation;
    });

    // Tests
    // -----
    test('add new args to URL (that doesn\'t currently have args)', () => {

        const newArgs = 'param1=value1&param2=value2';
        reloadPageWithArgs(newArgs);

        expect(global.location.href).toBe('https://example.com/page?' + newArgs);
    });

    test('replace args of URL (that currently has args)', () => {

        global.location.href += '?oldParam=oldValue';
        const newArgs = 'param1=value1&param2=value2';
        reloadPageWithArgs(newArgs);

        expect(global.location.href).toBe('https://example.com/page?' + newArgs);
    });
});