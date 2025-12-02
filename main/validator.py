import re
class validator:
    city_abbrviations = {
        "NYC": "New York",
        "LA": "Los Angeles",
        "SF": "San Francisco",
        "DC": "Washington",
        "UK": "United Kingdom",
        "RUS": "Russia"
    }

    @staticmethod
    def valid_city(city):
        city = city.strip()
        if not city.strip():
            raise ValueError("City name cannot be empty.")
        upper_city = city.upper()
        if upper_city in validator.city_abbrviations:
            city = validator.city_abbrviations[upper_city]
        if not re.match(r"^[a-zA-Z\s-]+$", city):
            raise ValueError("City name contains invalid characters.")
        return city
    
    @staticmethod
    def valid_coordinates(lat, lon):
        lat = float(lat)
        lon = float(lon)
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        return lat, lon
    
    @staticmethod
    def valid_units(units):
        valid_units = ["metric", "imperial"]
        units = units.lower().strip()
        if units not in valid_units:
            raise ValueError(f"Units must be one of {valid_units}.")
        return units