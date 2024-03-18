/* 
 * Javascript package for the location_select page functionality
 *
 * Sources: https://stackoverflow.com/questions/44346094/how-to-change-button-url-through-js
 */

/* Initializes location_select.html. 
 * The button in the page grabs the values from each Select field and generates a URL with the
 * generateWeatherSummaryUrl function (from Eric in init_map.js), which updates the href
*/
function initLocationSelect() {

    document.getElementById('submitButton').onclick = function() {
        var year = document.getElementById('yearSelect');
        var month = document.getElementById('monthSelect');
        var day = document.getElementById('daySelect');

        var sel = document.getElementById('citySelect');
        var city = sel.options[sel.selectedIndex].text;

        var date = year.value + '-' + month.value.padStart(2, '0') + '-' + day.value.padStart(2, '0');

        this.href = generateWeatherSummaryUrl(city, date);
    };
}

// Function to generate the URL for the button link
function generateWeatherSummaryUrl(cityName, date) {
    return `/weather_summary?city_name=${encodeURIComponent(cityName)}&date=${date}`;
}
