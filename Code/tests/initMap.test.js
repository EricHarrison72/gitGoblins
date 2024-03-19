// initMap.test.js

// Before your tests, mock fetch globally
beforeAll(() => {
  global.fetch = jest.fn(() => Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ icon: 'error' }),
  }));
});


// Mock the global document methods used by initMap.js
document.getElementById = jest.fn().mockImplementation(id => {
  switch (id) {
      case 'yearSelect':
      case 'monthSelect':
      case 'daySelect':
          return { addEventListener: jest.fn(), value: "2020" };
      default:
          return null;
  }
});

// Mock bind popup function
const mockBindPopup = jest.fn().mockReturnThis();

// Mock the L (Leaflet) object
const mockIcon = jest.fn().mockImplementation(() => 'mockIconReturn');
const L = {
  map: jest.fn().mockReturnThis(),
  tileLayer: jest.fn().mockReturnThis(),
  addTo: jest.fn().mockReturnThis(),
  setView: jest.fn().mockReturnThis(),
  marker: jest.fn().mockImplementation(() => ({
      addTo: jest.fn().mockReturnThis(),
      bindPopup: mockBindPopup,
      options: {}
  })),
  icon: mockIcon, // Mock the icon method
};
global.L = L;




// Assuming initMap is modified to be a module or its methods are otherwise made testable
const { initMap, createMarker, generateWeatherSummaryUrl, updatePopupLinks } = require('../weatherApp/static/js/init_map');

describe('init_map.js', () => {
  beforeEach(() => {
    // Reset the mocks for functions called on the L object directly
    L.map.mockClear();
    L.tileLayer.mockClear();
    L.addTo.mockClear();
    L.setView.mockClear();

    // Reset the mocks for functions called on the object returned by L.marker()
    if (L.marker().addTo.mockClear) {
        L.marker().addTo.mockClear();
    }
    if (L.marker().bindPopup.mockClear) {
        L.marker().bindPopup.mockClear();
    }
});

  //Test function for initializing map
  test('init_map initializes the map correctly', () => {
      initMap();
      expect(L.map).toHaveBeenCalledTimes(1);
      expect(L.tileLayer).toHaveBeenCalledTimes(1);
      expect(L.setView).toHaveBeenCalledTimes(1);
  });

  test('createMarker adds a marker to the map', async () => { // Note the async keyword
    L.marker.mockClear();
    await createMarker(L.map, -27.4705, 153.0260, 'Brisbane'); // Await the async function
    expect(L.marker).toHaveBeenCalledTimes(1);
    expect(mockBindPopup).toHaveBeenCalledTimes(1);
  });

  //Test function for generating weather summary
  test('generateWeatherSummaryUrl generates the correct URL', () => {
      const url = generateWeatherSummaryUrl('Brisbane', "2017-06-24");
      expect(url).toBe('/weather_summary?city_name=Brisbane&date=2017-06-24');
  });

});

//Clear all mocks after each test
afterEach(() => {
  jest.clearAllMocks();
});

