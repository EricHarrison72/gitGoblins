// -------------------------------------------------
// init_map.js
/*
Uses leaflet.js api to create a map where users can select their date and location.

Starter code sources:
- https://leafletjs.com/examples.html
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

    //Event listeners to the dropdowns to update marker icons when selections change
    document.getElementById('yearSelect').addEventListener('change', updateMarkerIcons);
    document.getElementById('monthSelect').addEventListener('change', updateMarkerIcons);
    document.getElementById('daySelect').addEventListener('change', updateMarkerIcons);

    // Create markers for each city
    createMarker(map, -36.0751, 146.9095, 'Albury');
    createMarker(map, -33.8751, 150.7634, 'Badgerys Creek');
    createMarker(map, -31.4978, 145.8363, 'Cobar');
    createMarker(map, -30.2962, 153.1139, 'Coffs Harbour');
    createMarker(map, -29.4653, 149.8416, 'Moree');
    createMarker(map, -32.9283, 151.7817, 'Newcastle');
    createMarker(map, -33.2822, 151.5669, 'Norah Head');
    createMarker(map, -29.0408, 167.9547, 'Norfolk Island');
    createMarker(map, -33.7507, 150.6877, 'Penrith');
    createMarker(map, -37.8239, 144.9983, 'Richmond');
    createMarker(map, -33.8688, 151.2093, 'Sydney');
    createMarker(map, -33.9400, 151.1754, 'Sydney Airport');
    createMarker(map, -35.1026, 147.3655, 'Wagga Wagga');
    createMarker(map, -32.8115, 151.8443, 'Williamtown');
    createMarker(map, -34.4248, 150.8931, 'Wollongong');
    createMarker(map, -35.2802, 149.1310, 'Canberra');
    createMarker(map, -35.4180, 149.0694, 'Tuggeranong');
    createMarker(map, -35.5294, 148.7723, 'Mount Ginini');
    createMarker(map, -37.5622, 143.8503, 'Ballarat');
    createMarker(map, -36.7596, 144.2786, 'Bendigo');
    createMarker(map, -38.1051, 147.0680, 'Sale');
    createMarker(map, -37.6708, 144.8430, 'Melbourne Airport');
    createMarker(map, -37.8136, 144.9631, 'Melbourne');
    createMarker(map, -34.2068, 142.1367, 'Mildura');
    createMarker(map, -36.3328, 141.6503, 'Nhil');
    createMarker(map, -38.3421, 141.6012, 'Portland');
    createMarker(map, -37.7101, 145.0828, 'Watsonia');
    createMarker(map, -37.9224, 141.2754, 'Dartmoor');
    createMarker(map, -27.4705, 153.0260, 'Brisbane');
    createMarker(map, -16.9203, 145.7710, 'Cairns');
    createMarker(map, -28.0167, 153.4000, 'Gold Coast');
    createMarker(map, -19.2590, 146.8169, 'Townsville');
    createMarker(map, -34.9285, 138.6007, 'Adelaide');
    createMarker(map, -37.8284, 140.7807, 'Mount Gambier');
    createMarker(map, -34.4730, 138.9957, 'Nuriootpa');
    createMarker(map, -31.1988, 136.8251, 'Woomera');
    createMarker(map, -35.0268, 117.8837, 'Albany');
    createMarker(map, -34.0262, 115.1002, 'Witchcliffe');
    createMarker(map, -31.6676, 116.0292, 'Pearce RAAF');
    createMarker(map, -31.9385, 115.9672, 'Perth Airport');
    createMarker(map, -31.9514, 115.8617, 'Perth');
    createMarker(map, -32.9804, 121.6456, 'Salmon Gums');
    createMarker(map, -34.9762, 116.7313, 'Walpole');
    createMarker(map, -42.8826, 147.3257, 'Hobart');
    createMarker(map, -41.4391, 147.1358, 'Launceston');
    createMarker(map, -23.6980, 133.8807, 'Alice Springs');
    createMarker(map, -12.4637, 130.8444, 'Darwin');
    createMarker(map, -14.4520, 132.2699, 'Katherine');
    createMarker(map, -25.3444, 131.0369, 'Uluru');

    
}

//Function to generate the URL for the popup link
function generateWeatherSummaryUrl(cityName, date) {
    return `/weather_summary?city_name=${encodeURIComponent(cityName)}&date=${date}`;
}

//Function to update all markers' popups with the current date
function updatePopupLinks() {
    cityMarkers.forEach(marker => {
        var cityName = marker.getPopup().getContent().match(/<b>(.*?)<\/b>/)[1];
        var year = document.getElementById('yearSelect').value;
        var month = document.getElementById('monthSelect').value;
        var day = document.getElementById('daySelect').value;
        var date = year + '-' + month.padStart(2, '0') + '-' + day.padStart(2, '0')

        var newPopupContent = `<b>${cityName}</b><br><a href="#" onclick="window.location.href='${generateWeatherSummaryUrl(cityName, date)}'">See weather details</a>`;
        marker.setPopupContent(newPopupContent);
    });
}

//Function to update all markers' icons with the current date
async function updateMarkerIcons() {
    console.log("Updating markers...");

    var year = document.getElementById('yearSelect').value;
    var month = document.getElementById('monthSelect').value;
    var day = document.getElementById('daySelect').value;
    var date = year + '-' + month.padStart(2, '0') + '-' + day.padStart(2, '0');
    
    // Loop through all markers and update their icon
    for (const marker of cityMarkers) {
        const cityName = marker.options.cityName; // Assuming cityName is stored in options
        const iconUrl = await determineMarkerIcon(cityName, date);
        const newIcon = L.icon({
            iconUrl: iconUrl,
            iconSize: [45, 40], // Size of the icon
            iconAnchor: [35, 35], // Point of the icon which will correspond to marker's location
            popupAnchor: [-10, -32], // Point from which the popup should open relative to the iconAnchor
        });
        marker.setIcon(newIcon); // This should work if `marker` is a Leaflet marker instance
    }
}


// Define createMarker at the top level, this is done so that it can be exported for testing
async function createMarker(map, lat, lng, cityName) {
    var year = document.getElementById('yearSelect').value;
    var month = document.getElementById('monthSelect').value;
    var day = document.getElementById('daySelect').value;
    var date = year + '-' + month.padStart(2, '0') + '-' + day.padStart(2, '0')

    var iconURL = await determineMarkerIcon(cityName, date);

    //Determine correct marker icon here
    const newIcon = L.icon({
        iconUrl: iconURL,
        iconSize: [45, 40], // Size of the icon
        iconAnchor: [35, 35], // Point of the icon which will correspond to marker's location
        popupAnchor: [-10, -32], // Point from which the popup should open relative to the iconAnchor
    });
    
    var marker = L.marker([lat, lng], {icon: newIcon}).addTo(map);

    marker.bindPopup(`<b>${cityName}</b><br><a href="#" onclick="event.preventDefault(); window.location.href='${generateWeatherSummaryUrl(cityName, date)}';">See weather details</a>`);
    marker.options.cityName = cityName; // Store cityName within marker options for later access
    cityMarkers.push(marker);
}

async function determineMarkerIcon(cityName, date) {
    try {
        // Encode the city name to ensure the URL is properly formatted
        const response = await fetch(`/api/weather_icon?cityName=${encodeURIComponent(cityName)}&date=${date}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        return data.icon;
    } catch (error) {
        console.error("Failed to fetch weather icon:", error);
        // Return error icon in case of error
        return "/static/img/marker_error.png";
    }
}


    // Export functions for testing purposes
    module.exports = { initMap, createMarker, generateWeatherSummaryUrl, updatePopupLinks };
