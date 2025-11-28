import re
class validator:
    @staticmethod
    def valid_city(city):
        if not city:
            raise ValueError("City name cannot be empty.")
        if not re.match("^[a-zA-Z\s-]+$", city):
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