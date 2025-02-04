import pytest
import requests
import uuid

BASE_URL = "https://to-barrel-monitor.azurewebsites.net"

def generate_barrel_payload(use_own_id=True):
    payload = {
        'qr': "my_testing_QR_final",
        'rfid': "my_testing_RFID_final",
        'nfc': "my_testing_NFC_final"
    }
    
    if use_own_id:
        payload['id'] = str(uuid.uuid4())     

    return payload

@pytest.fixture
def test_barrel(use_own_id=True):
    payload = generate_barrel_payload(use_own_id)
    
    response = requests.post(f"{BASE_URL}/barrels", json=payload)
    assert response.status_code == 201
    barrel = response.json()

    yield barrel

    try:
        delete_url = f"{BASE_URL}/barrels/{barrel['id']}"
        delete_response = requests.delete(delete_url)
        delete_response.raise_for_status()
    except requests.RequestException as e:
        print(f"\nTeardown failed: DELETE {delete_url} returned {delete_response.status_code} - {delete_response.text}\nException: {e}")   

@pytest.fixture
def test_barrel_without_teardown(use_own_id=True):
    payload = generate_barrel_payload(use_own_id)
    
    response = requests.post(f"{BASE_URL}/barrels", json=payload)
    assert response.status_code == 201
    return response.json()
               

@pytest.fixture
def test_measurement(test_barrel):
    payload = {
        'barrelId': test_barrel['id'], 
        'temperature': 25.5,
        'humidity': 60
        }

    response = requests.post(f"{BASE_URL}/measurements", json=payload)
    assert response.status_code == 201
    measurement = response.json()

    yield measurement

    try:
        delete_url = f"{BASE_URL}/measurements/{measurement['id']}"
        delete_response = requests.delete(delete_url)
        delete_response.raise_for_status()
    except requests.RequestException as e:
        print(f"\nTeardown failed: DELETE {delete_url} returned {delete_response.status_code} - {delete_response.text}\nException: {e}")    
