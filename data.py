import requests

def fetch_new_questions():
    parameters = {
        "amount": 20,
        "type": "boolean",
    }
    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()
    data = response.json()
    return data["results"]
