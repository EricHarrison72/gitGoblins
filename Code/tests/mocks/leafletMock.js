/*
This file is used to create a mock leaflet environment to be used for testing purposes.
*/
const L = {
    map: jest.fn().mockReturnThis(),
    tileLayer: jest.fn().mockReturnThis(),
    addTo: jest.fn().mockReturnThis(),
    marker: jest.fn().mockImplementation(() => ({
      bindPopup: jest.fn().mockReturnThis(),
      addTo: jest.fn().mockReturnThis(),
      getPopup: jest.fn().mockImplementation(() => ({
        getContent: jest.fn().mockReturnValue(`<b>MockCity</b><br>See weather details`)
      })),
      options: { cityName: 'MockCity' }
    }))
  };
  
  module.exports = L;
  