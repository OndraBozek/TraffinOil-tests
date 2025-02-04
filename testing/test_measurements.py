import requests
import uuid

BASE_URL = "https://to-barrel-monitor.azurewebsites.net"

# TC for getting whole list of measurements, response should be 200
def test_get_measurements():
    response = requests.get(f"{BASE_URL}/measurements")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# TC for getting specific measurement, response should be 200
def test_get_measurement(test_measurement):
    response = requests.get(f"{BASE_URL}/measurements/{test_measurement['id']}")
    assert response.status_code == 200
    assert response.json()['id'] == test_measurement['id']

# TC for getting nonExistent measurement, response should be 404
def test_get_measurement_nonExistent():
    measure_id = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/measurements/{measure_id}")
    assert response.status_code == 404

# TC for getting invalid measurement, response should be 400
def test_get_measurement_incorrect():
    measure_id = "incorectID"
    response = requests.get(f"{BASE_URL}/measurements/{measure_id}")
    assert response.status_code == 400

# TC for creating measurement, response should be 200 and test is checking all required fields
def test_create_measurement(test_measurement):
    assert test_measurement is not None
    assert 'id' in test_measurement
    # print(f"Created measurement ID: {test_measurement['id']}")

    get_response = requests.get(f"{BASE_URL}/measurements/{test_measurement['id']}")
    assert get_response.status_code == 200

    retrieved_measurement = get_response.json()

    assert retrieved_measurement['id'] == test_measurement['id']
    assert retrieved_measurement['barrelId'] == test_measurement['barrelId']
    assert retrieved_measurement['temperature'] == test_measurement['temperature']
    assert retrieved_measurement['humidity'] == test_measurement['humidity']

# TC for creating invalid measurements, response should be 400
def test_create_measurement_invalid():
    payload = {
        'barrelId': str(uuid.uuid4()),  #random UUID
        'temperature': "20.5",          #string instead of double
        'humidity': 60,
        'addedAttribute': 44            #added attribute
    }

    response = requests.post(f"{BASE_URL}/measurements", json=payload)
    assert response.status_code == 400
