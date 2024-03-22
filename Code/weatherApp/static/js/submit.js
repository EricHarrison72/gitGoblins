
function reloadWithArgs_WeatherSummary() {
    var year = document.getElementById('yearSelect');
    var month = document.getElementById('monthSelect');
    var day = document.getElementById('daySelect');
    var date = year.value + '-' + month.value.padStart(2, '0') + '-' + day.value.padStart(2, '0');

    var sel = document.getElementById('citySelect');
    var cityName = sel.options[sel.selectedIndex].text;
    cityName = cityName.replace(/\s+/g, '');

    location.href = `/weather_summary?city_name=${ cityName }&date=${ date }`;
}