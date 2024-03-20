// ------------------------------------------------
// urls.js
/*
 * A module for functions that generate urls to webpages based off of some inputs.
 */
// -------------------------------------------------

export function generateWeatherSummaryURL(cityName, date) {
    return `/weather_summary?city_name=${encodeURIComponent(cityName)}&date=${date}`;  
}