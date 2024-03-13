/*
This file is used to create a mock the DOM elements from the leaflet
environment to be used for testing purposes.
*/

function setupDOM() {    
  document.body.innerHTML = `
    <select id="yearSelect">
      <option value="2020">2020</option>
    </select>
    <select id="monthSelect">
      <option value="01">January</option>
    </select>
    <select id="daySelect">
      <option value="01">1</option>
    </select>
    <div id="map"></div>
  `;

  global.L = {
      map: jest.fn(() => ({
          setView: jest.fn().mockReturnThis(),
          tileLayer: jest.fn().mockReturnThis(),
          addTo: jest.fn().mockReturnThis(),
      })),
      tileLayer: jest.fn(() => ({
          addTo: jest.fn().mockReturnThis(),
      })),
      marker: jest.fn(() => ({
          bindPopup: jest.fn().mockReturnThis(),
          addTo: jest.fn().mockReturnThis(),
          getPopup: jest.fn().mockImplementation(() => ({
              getContent: jest.fn().mockReturnValue(`<b>MockCity</b><br>See weather details`)
          })),
          setPopupContent: jest.fn().mockReturnThis(), // Mock implementation for setPopupContent
          options: {} // Ensure options object is present for marker
      })),
  };
}
module.exports = setupDOM;
