console.log("init_map.js is run");
function initMap() {
    var map = L.map('map').setView([-27.07, 132.08], 4); // Latitude, Longitude, Zoom level

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    var marker = L.marker([-36.0751, 146.9095]).addTo(map);
    marker.bindPopup("<b>Albury</b><br>See wather details").openPopup();
  }
  
  initMap();
