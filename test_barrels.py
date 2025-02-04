import requests
import uuid

BASE_URL = "https://to-barrel-monitor.azurewebsites.net"

# TC for getting whole list of barrels, response should be 200
def test_get_barrels():
    response = requests.get(f"{BASE_URL}/barrels")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# TC for getting specific barrel, response should be 200
def test_get_barrel(test_barrel):
    response = requests.get(f"{BASE_URL}/barrels/{test_barrel['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == test_barrel["id"]

# TC for getting nonExistent barrel, response should be 404
def test_get_barrel_nonExistent():
    barrel_id = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/barrels/{barrel_id}")
    assert response.status_code == 404

# TC for getting invalid barrel, response should be 400
def test_get_barrel_incorrect():
    barrel_id = "incorectID"
    response = requests.get(f"{BASE_URL}/barrels/{barrel_id}")
    assert response.status_code == 400

# TC for creating barrel, response should be 200 and test is checking all required fields
def test_create_barrel(test_barrel):
    assert test_barrel is not None
    assert "id" in test_barrel
    # print(f"Created barrel ID: {test_barrel['id']}")

    get_response = requests.get(f"{BASE_URL}/barrels/{test_barrel['id']}")
    assert get_response.status_code == 200

    retrieved_barrel = get_response.json()

    assert retrieved_barrel['id'] == test_barrel['id']
    assert retrieved_barrel['qr'] == test_barrel['qr']
    assert retrieved_barrel['rfid'] == test_barrel['rfid']
    assert retrieved_barrel['nfc'] == test_barrel['nfc']

# TC for creating invalid barrel, response should be 400
def test_create_barrel_incorrect():
    payload = {
        "qr": 55,                       #wrong type
        "rdif": "Wrong atribute name",  #non-existent attribute
        "additionalAttribute": "test"   #different attribute
    }
    response = requests.post(f"{BASE_URL}/barrels", json=payload)
    assert response.status_code == 400

# TC for deleting specific barrel, response of delete should be 200 and of next get should be 404
def test_delete_barrel(test_barrel_without_teardown):
    assert test_barrel_without_teardown is not None
    assert "id" in test_barrel_without_teardown
    # print(f"Created barrel ID: {test_barrel_without_teardown['id']}")

    delete_response = requests.delete(f"{BASE_URL}/barrels/{test_barrel_without_teardown['id']}")
    assert delete_response.status_code == 200

    get_response = requests.get(f"{BASE_URL}/barrels/{test_barrel_without_teardown['id']}")
    assert get_response.status_code == 404

# TC for deleting nonExisting barrel, response should be 404
def test_delete_barrel_nonExistent():
    barrel_id = str(uuid.uuid4())
    response = requests.delete(f"{BASE_URL}/barrels/{barrel_id}")
    assert response.status_code == 404

# TC for deleting incorrect barrel, response should be 400
def test_delete_barrel_incorrect():
    barrel_id = "incorectID"
    response = requests.delete(f"{BASE_URL}/barrels/{barrel_id}")
    assert response.status_code == 400