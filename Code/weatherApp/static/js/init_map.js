// -------------------------------------------------
// init_map.js
/*
Uses leaflet.js api to create a map where users can select their date and location.

TODO:
- add visual markers representing city weather (if we have time)

Starter code sources:
- ???
*/
// -------------------------------------------------
var cityMarkers = [];

function initMap() {
    var map = L.map('map').setView([-27.07, 132.08], 4); // Latitude, Longitude, Zoom level when map first opens

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map); // Import and display map
    

    //Event listeners to the dropdowns to update the popups when selections change
    document.getElementById('yearSelect').addEventListener('change', updatePopupLinks);
    document.getElementById('monthSelect').addEventListener('change', updatePopupLinks);
    document.getElementById('daySelect').addEventListener('change', updatePopupLinks);

    //Function that creates a marker at a specific latitude, longitude for a specific city
    function createMarker(lat, lng, cityName) {
        var marker = L.marker([lat, lng]).addTo(map);
        marker.bindPopup(`<b>${cityName}</b><br><a href="#" onclick="event.preventDefault(); window.location.href='${generateWeatherSummaryUrl(cityName)}';">See weather details</a>`);
        marker.options.cityName = cityName; // Store cityName within marker options for later access
        cityMarkers.push(marker);
    }

    // Create markers for each city
    createMarker(-36.0751, 146.9095, 'Albury');
    createMarker(-33.8751, 150.7634, 'Badgerys Creek');
    createMarker(-31.4978, 145.8363, 'Cobar');
    createMarker(-30.2962, 153.1139, 'Coffs Harbour');
    createMarker(-29.4653, 149.8416, 'Moree');
    createMarker(-32.9283, 151.7817, 'Newcastle');
    createMarker(-33.2822, 151.5669, 'Norah Head');
    createMarker(-29.0408, 167.9547, 'Norfolk Island');
    createMarker(-33.7507, 150.6877, 'Penrith');
    createMarker(-37.8239, 144.9983, 'Richmond');
    createMarker(-33.8688, 151.2093, 'Sydney');
    createMarker(-33.9400, 151.1754, 'Sydney Airport');
    createMarker(-35.1026, 147.3655, 'Wagga Wagga');
    createMarker(-32.8115, 151.8443, 'Williamtown');
    createMarker(-34.4248, 150.8931, 'Wollongong');
    createMarker(-35.2802, 149.1310, 'Canberra');
    createMarker(-35.4180, 149.0694, 'Tuggeranong');
    createMarker(-35.5294, 148.7723, 'Mount Ginini');
    createMarker(-37.5622, 143.8503, 'Ballarat');
    createMarker(-36.7596, 144.2786, 'Bendigo');
    createMarker(-38.1051, 147.0680, 'Sale');
    createMarker(-37.6708, 144.8430, 'Melbourne Airport');
    createMarker(-37.8136, 144.9631, 'Melbourne');
    createMarker(-34.2068, 142.1367, 'Mildura');
    createMarker(-36.3328, 141.6503, 'Nhil');
    createMarker(-38.3421, 141.6012, 'Portland');
    createMarker(-37.7101, 145.0828, 'Watsonia');
    createMarker(-37.9224, 141.2754, 'Dartmoor');
    createMarker(-27.4705, 153.0260, 'Brisbane');
    createMarker(-16.9203, 145.7710, 'Cairns');
    createMarker(-28.0167, 153.4000, 'Gold Coast');
    createMarker(-19.2590, 146.8169, 'Townsville');
    createMarker(-34.9285, 138.6007, 'Adelaide');
    createMarker(-37.8284, 140.7807, 'Mount Gambier');
    createMarker(-34.4730, 138.9957, 'Nuriootpa');
    createMarker(-31.1988, 136.8251, 'Woomera');
    createMarker(-35.0268, 117.8837, 'Albany');
    createMarker(-34.0262, 115.1002, 'Witchcliffe');
    createMarker(-31.6676, 116.0292, 'Pearce RAAF');
    createMarker(-31.9385, 115.9672, 'Perth Airport');
    createMarker(-31.9514, 115.8617, 'Perth');
    createMarker(-32.9804, 121.6456, 'Salmon Gums');
    createMarker(-34.9762, 116.7313, 'Walpole');
    createMarker(-42.8826, 147.3257, 'Hobart');
    createMarker(-41.4391, 147.1358, 'Launceston');
    createMarker(-23.6980, 133.8807, 'Alice Springs');
    createMarker(-12.4637, 130.8444, 'Darwin');
    createMarker(-14.4520, 132.2699, 'Katherine');
    createMarker(-25.3444, 131.0369, 'Uluru');

    
}

//Function to generate the URL for the popup link
function generateWeatherSummaryUrl(cityName) {
    var year = document.getElementById('yearSelect').value;
    var month = document.getElementById('monthSelect').value;
    var day = document.getElementById('daySelect').value;
    var date = year + '-' + month.padStart(2, '0') + '-' + day.padStart(2, '0');
    
    //Adjust the URL path according to your application's routing
    return `/weather_summary?city_name=${encodeURIComponent(cityName)}&date=${date}`;
}

//Function to update all markers' popups with the current date
function updatePopupLinks() {
    cityMarkers.forEach(marker => {
        var cityName = marker.getPopup().getContent().match(/<b>(.*?)<\/b>/)[1];
        var newPopupContent = `<b>${cityName}</b><br><a href="#" onclick="window.location.href='${generateWeatherSummaryUrl(cityName)}'">See weather details</a>`;
        marker.setPopupContent(newPopupContent);
    });
}

  initMap();
