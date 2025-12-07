import requests
import time

def test_all_services_up():
    time.sleep(5)  # attend que tout démarre
    services = [
        "http://localhost:8080/health",
        "http://localhost:8001/health",
        "http://localhost:8002/health",
        "http://localhost:8003/health",
        "http://localhost:8004/health",
        "http://localhost:8005/health",
    ]
    for url in services:
        try:
            r = requests.get(url, timeout=5)
            assert r.status_code == 200
        except:
            print(f"Failed: {url}")
            raise
    print("Tous les services sont UP !")