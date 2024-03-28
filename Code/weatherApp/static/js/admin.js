/*
This is just starter code for admin updates on the db it's not meant to work yet 
and the resouces are listed below
https://luciana-lab.medium.com/creating-and-updating-user-database-javascript-frontend-rails-backend-178a6656b76d
https://stackoverflow.com/questions/712566/updating-database-using-javascript
*/
document.getElementById("highTempForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission
    // Collect form data
    var formData = new FormData(this);
    // Submit form data via fetch API to the admin endpoint
    fetch('/admin', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Show success message
        alert(data.message);
        // Fetch cityId based on cityName
        fetch(`/get_city_id?city_name=${formData.get('city_name')}`)
        .then(response => response.json())
        .then(cityData => {
            const cityId = cityData.city_id;
            const date = formData.get('date');
            // Redirect to weather_summary page with updated date and location
            window.location.href = `/weather_summary?city_id=${cityId}&date=${date}`;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching city data. Please try again.');
        });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.'); // Show error message
    });
});