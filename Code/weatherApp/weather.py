# --------------------------------------
# weather.py
'''
Contains methods to retrieve weather information
'''
# ----------------------------------


def determine_icon_based_on_weather(weather_data):
    # Helper function to safely convert to int, handling 'NA', 'N/A', etc.
    def safe_int(value, default=0):
        try:
            return int(value)
        except ValueError:
            return default

    #If high and low temps are 0 it means there was no data for that day
    if (weather_data['temp_high'] == 0) & (weather_data['temp_low'] == 0):
        return 'error'
    
    if weather_data['raining'] == "Yes":
        return 'rain'

    wind_speed = safe_int(weather_data['wind_speed'])
    if wind_speed > 80:
        return 'wind'

    cloud_cover = safe_int(weather_data['cloud'])
    if cloud_cover > 4:
        return 'cloud'
    elif cloud_cover > 0:
        return 'partcloud'

    return 'sun'

