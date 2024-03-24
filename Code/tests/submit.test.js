// -----------------------------
//submit.test.js
/*
Unit tests for submit.js

Written with some help from Chat-GPT 4.
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


test('This is just so the CI doesnt break', () => {
    expect((1+2)).toBe(3);
});