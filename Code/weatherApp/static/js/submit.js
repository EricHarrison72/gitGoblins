// -----------------------------------
// submit.js
/*
Script containing the functions neccessary for 
the submit buttons in selection tables on feature pages.
Based off of code Josh and Eric wrote.
*/
// --------------------------------------

function getDateFromSelection(id_prefix='') {
    var year = document.getElementById(id_prefix + 'yearSelect');
    var month = document.getElementById(id_prefix + 'monthSelect');
    var day = document.getElementById(id_prefix + 'daySelect');

    var date = `${ year.value }-${ month.value.padStart(2, '0')}-${ day.value.padStart(2, '0')}`;
    return date;
}

function getCityFromSelection() {
    var sel = document.getElementById('citySelect');
    var cityName = sel.options[sel.selectedIndex].text;
    cityName = cityName.replace(/\s+/g, '');

    return cityName;
}

function getCitiesFromSelection() {
    //TODO - Eric
}

function reloadPageWithArgs(urlArgs){
    currentUrl = location.href;

    urlArray = currentUrl.split('?');
    newUrl = urlArray[0] + '?' + urlArgs;

    location.href = newUrl;
}

// export for testing purposes
module.exports = {
    getDateFromSelection,
    getCityFromSelection,
    getCitiesFromSelection,
    reloadPageWithArgs
}