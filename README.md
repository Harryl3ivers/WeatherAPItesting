### 1. Clone the repository
```bash
git clone https://github.com/yourusername/weather-dashboard.git
cd weather-dashboard
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API key
```bash
# Copy example file
 .env.example .env

# Edit .env and add your OpenWeatherMap API key
# Get  key at: https://openweathermap.org/api
WEATHER_API_KEY=your_key_here
```

---

### Run all tests
```bash
pytest -v
```

### Run with coverage report
```bash
pytest --cov=main --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_weather_client.py -v
```

### Run cache tests with time mocking
```bash
pytest tests/test_cache_manager.py -v
```

---

## Usage

### Command Line Interface
```bash
python cli.py
```

**Menu Options:**
1. Get weather by city name
2. Get weather by coordinates
3. View cache statistics
4. View weather history
5. View temperature statistics
6. Compare multiple cities
7. Exit
