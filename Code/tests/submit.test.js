// -----------------------------
//submit.test.js
/*
Unit tests for submit.js

Written with some help from ChatGPT 4.
*/
// -----------------------------
// imports from submit.js
const {
    getDateFromSelection,
    getCityFromSelection,
    getCitiesFromSelection,
    reloadPageWithArgs
} = require('../weatherApp/static/js/submit.js');

//test getDateFromSelection
/*
- required mocks: date selection menu
- expected value --- date:str in the form 'yyyy-mm-dd' extracted from selection menus
1. no parameter
2. passed paramter id_prefix
*/

//test getCityFromSelection
/*
- required mocks: city selection menu
expected value --- city:str extracted from selection menu
1. no space city
2. city name with space
*/

//test reloadPageWithArgs
/* 
- required mocks: page with url
expected value --- url after call should match url/args
1. url has no args
2. url has args
*/

describe('reloadPageWithArgs', () => {

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

    // Add more tests here if needed to cover other scenarios
});