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
        return { addEventListener: jest.fn(), value: "2017" };
      case 'monthSelect':
        return { addEventListener: jest.fn(), value: "06" };
      case 'daySelect':
          return { addEventListener: jest.fn(), value: "24" };
      default:
          return null;
  }
});

const mockIcon = jest.fn().mockImplementation(iconOptions => {
  if (iconOptions.iconUrl.includes("sun")) {
    return 'mockSunIcon';
  } else if (iconOptions.iconUrl.includes("rain")) {
    return 'mockRainIcon';
  } else if (iconOptions.iconUrl.includes("error")) {
    return 'mockErrorIcon';
  } else {
    return 'mockDefaultIcon'; // Fallback or default icon
  }
});
const mockSetIcon = jest.fn();


// Mock bind popup function
const mockBindPopup = jest.fn().mockReturnThis();

// Mock the L (Leaflet) object
const L = {
  map: jest.fn().mockReturnThis(),
  tileLayer: jest.fn().mockReturnThis(),
  addTo: jest.fn().mockReturnThis(),
  setView: jest.fn().mockReturnThis(),
  marker: jest.fn().mockImplementation(() => ({
      addTo: jest.fn().mockReturnThis(),
      bindPopup: mockBindPopup,
      setIcon: mockSetIcon,
      options: {}
  })),
  icon: mockIcon, // Mock the icon method
};
global.L = L;

// Import everything required for testing from init_map.js
const { initMap, createMarker, generateWeatherSummaryUrl, updatePopupLinks, updateMarkerIcons, determineMarkerIcon, cityMarkers  } = require('../weatherApp/static/js/init_map');


// Additional mock setup to simulate cityMarkers and their popups
const mockSetPopupContent = jest.fn();
const createMockMarker = (cityName) => ({
  getPopup: jest.fn().mockImplementation(() => ({
    getContent: jest.fn().mockImplementation(() => `<b>${cityName}</b>`),
    setContent: mockSetPopupContent
  })),
  setPopupContent: jest.fn(),
  options: { cityName }
});

//Tests functionality for all functions necessary to initialize the map
describe('init_map.js', () => {
  beforeEach(() => {
    // Reset the mocks for functions called on the L object directly
    L.map.mockClear();
    L.tileLayer.mockClear();
    L.addTo.mockClear();
    L.setView.mockClear();

    // Reset mockSetPopupContent for clean test starts
    mockSetPopupContent.mockClear();
    cityMarkers.length = 0; // Clear existing markers

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

  // Test for createMarker function
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


// Test for updatePopupLinks function
describe('updatePopupLinks updates the links for each popup correctly', () => {
  test('it updates popup content based on selected date', () => {
    // Setup: Define multiple cities and create a mock marker for each
    const cities = ['Brisbane', 'Sydney', 'Melbourne'];
    cities.forEach(cityName => {
      const marker = createMockMarker(cityName);
      cityMarkers.push(marker);
    });

    updatePopupLinks();

    // Assertion: Check if setPopupContent was called for each marker, and that URL is correct
    cityMarkers.forEach((marker, index) => {
      expect(marker.setPopupContent).toHaveBeenCalledTimes(1);

      const expectedDate = '2017-06-24';
      const expectedUrlPart = `/weather_summary?city_name=${cities[index]}&date=${expectedDate}`;
      expect(marker.setPopupContent).toHaveBeenCalledWith(expect.stringContaining(expectedUrlPart));
    });
  });
});

// Test for updateMarkerIcons function
describe('updateMarkerIcons updates the icons for each marker correctly', () => {
  beforeEach(() => {
    // Reset the mockSetIcon for each test
    mockSetIcon.mockClear();
  });

  test('it updates a single marker icon based on weather data', async () => {
    // Setup: Adjust fetch mock to return a single icon type
    global.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ icon: 'sun' }),
    });
  
    const cities = ['Brisbane', 'Sydney', 'Melbourne'];
    cities.forEach(cityName => {
      const marker = createMockMarker(cityName); // Original mock without setIcon
      marker.setIcon = mockSetIcon; // Explicitly adding setIcon mock
      cityMarkers.push(marker);
    });
  
    // Execute the function
    await updateMarkerIcons();
  
    // Assertions: Verify setIcon was called with the expected icon
    expect(mockSetIcon).toHaveBeenCalledWith('mockSunIcon');
  });
});

// Test for determineMarkerIcon function
describe('determineMarkerIcon functionality', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    fetch.mockClear();
  });

  test('returns correct icon for sunny weather', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ icon: 'sun' }),
    });
    
    //City and date don't matter here as above statement ensures the icon will be 'sun'
    const icon = await determineMarkerIcon('Brisbane', '2017-06-24');
    expect(icon).toEqual('mockSunIcon');
  });

  test('returns correct icon for rainy weather', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ icon: 'rain' }),
    });
    
    //City and date don't matter here as above statement ensures the icon will be 'rain'
    const icon = await determineMarkerIcon('Sydney', '2017-06-24');
    expect(icon).toEqual('mockRainIcon');
  });

  //This test intentionally throws an error which will display in the console
  test('returns error icon on fetch failure', async () => {
    fetch.mockRejectedValueOnce(new Error('API failure'));
    const icon = await determineMarkerIcon('Melbourne', '2017-06-24');
    expect(icon).toEqual('mockErrorIcon');
  });
});

//Clear all mocks after each test
afterEach(() => {
  jest.clearAllMocks();
});

