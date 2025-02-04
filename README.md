# Pytest API Test Suite

This project contains automated API tests using `pytest` for the **barrel monitoring API** hosted at `https://to-barrel-monitor.azurewebsites.net`.

## 📌 Project Structure

- **`conftest.py`** → Contains pytest fixtures for setting up test data.
- **`test_barrels.py`** → Tests API endpoints related to barrels.
- **`test_measurements.py`** → Tests API endpoints related to measurements.

## 🛠️ Installation & Setup

### 1️⃣ Install Dependencies
Make sure you have Python installed (preferably 3.8+). Then, install required dependencies:

```sh
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install manually:
```sh
pip install pytest requests
```

### 2️⃣ Running Tests
Run all tests using:
```sh
pytest
```

Run specific test files:
```sh
pytest test_barrels.py
pytest test_measurements.py
```

Run specific test case:
```sh
pytest test_barrels.py::test_get_barrels
pytest test_measurements.py::test_get_measurements
```

## 🔹 Configuration
- The API base URL is set in `BASE_URL` inside test files (`https://to-barrel-monitor.azurewebsites.net`).
- Test data is generated dynamically using `uuid`.
- `conftest.py` contains reusable fixtures for API test setup.

## 🧪 Example Test Case
A simple test case to fetch all barrels:
```python
import requests
BASE_URL = "https://to-barrel-monitor.azurewebsites.net"

def test_get_barrels():
    response = requests.get(f"{BASE_URL}/barrels")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

Feel free to contribute or report issues! 🚀
