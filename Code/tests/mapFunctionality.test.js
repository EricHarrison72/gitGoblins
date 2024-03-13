const setupDOM = require('./mocks/domMocks.js');
setupDOM();
const { initMap, updatePopupLinks } = require('../weatherApp/static/js/init_map');

describe('Map Functionality', () => {
    beforeEach(() => {
        setupDOM(); // Assuming setupDOM() also does other necessary DOM setup
        global.cityMarkers = [];
    });
    

  test('createMarker adds marker to cityMarkers array', () => {
    expect(global.cityMarkers.length).toBe(0); // Ensure cityMarkers is empty

    // Since initMap calls createMarker for each city, we can use it to test
    initMap();

    // Adjust the expectation based on the number of markers created in initMap
    expect(global.cityMarkers.length).toBeGreaterThan(0);
  });

  test('updatePopupLinks updates popup content correctly', () => {
    initMap(); // Initialize markers
    updatePopupLinks(); // Call updatePopupLinks to update the popup content

    // Check if popup content for the first marker has been updated
    const newPopupContent = global.cityMarkers[0].getPopup().getContent();
    expect(newPopupContent).toContain('window.location.href');
  });
});
