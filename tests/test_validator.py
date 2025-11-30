from main.validator import validator
import pytest
class TestValidator:
    def test_valid_city(self):
        mock_result = validator.valid_city("New York")
        assert mock_result == "New York"
    
    def test_city_with_abbreviation(self):
        mock_result = validator.valid_city("LA")
        assert mock_result == "Los Angeles"
    
    def test_city_with_spaces(self):
        mock_result = validator.valid_city("  San Francisco  ")
        assert mock_result == "San Francisco"

    def test_city_with_hyphen(self):
        mock_result = validator.valid_city("Winston-Salem")
        assert mock_result == "Winston-Salem"
    
    def test_city_whitespace(self):
        mock_result = validator.valid_city(" Paris  ")
        assert mock_result == "Paris"
    
    def test_empty_city(self):
        with pytest.raises(ValueError, match="City name cannot be empty."):
            validator.valid_city("   ")
    
    def test_city_with_numbers(self):
        with pytest.raises(ValueError, match="City name contains invalid characters."):
            validator.valid_city("City123")
       
    
    def test_city_with_special_characters(self):
        with pytest.raises(ValueError, match="City name contains invalid characters."):
            validator.valid_city("New@York!")
    
    def test_valid_coordinates(self):
        lat, lon = validator.valid_coordinates("45.0", "-93.0")
        assert lat == 45.0
        assert lon == -93.0
    
    def test_coords_as_strings(self):
        lat, lon = validator.valid_coordinates("  34.05  ", " -118.25 ")
        assert lat == 34.05
        assert lon == -118.25
    
    def test_invalid_latitude(self):
        with pytest.raises(ValueError, match="Latitude must be between -90 and 90."):
            validator.valid_coordinates("100.0", "50.0")
    
    def test_invalid_longitude(self):
        with pytest.raises(ValueError, match="Longitude must be between -180 and 180."):
            validator.valid_coordinates("45.0", "-200.0")
    
    def test_non_numeric_coordinates(self):
        with pytest.raises(ValueError):
            validator.valid_coordinates("abc", "def")

    def test_valid_units_metric(self):
        units = validator.valid_units("metric")
        assert units == "metric"
    
    def test_valid_units_imperial(self):
        units = validator.valid_units("imperial")
        assert units == "imperial"

    def test_units_case_insensitivity(self):
        units = validator.valid_units("MeTrIc")
        assert units == "metric"
    
    def test_invalid_units(self):
        with pytest.raises(ValueError, match="Units must be one of \['metric', 'imperial'\]."):
            validator.valid_units("celsius")