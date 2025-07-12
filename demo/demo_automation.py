import requests
import json

# Simple POST request to update tweet status
def simple_update_request():
    url = "https://script.google.com/macros/s/AKfycbyUq7F1VD_cBMgoyB3j_oKYGPlsbgZ8j6lz6fTatw_nyRsEtugHoManapb8v6Uwnk4n/exec"
    
    payload = {
        "tweet_id": "efb81f36-9a0a-4fc9-a404-4595af30d4ba",
        "status": "done",
        "task": "update_tweet"
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    simple_update_request()