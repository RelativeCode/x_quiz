import requests

parameters = {
    "amount": 10,
    "type": "boolean",
}

response = requests.get("https://opentdb.com/api.php", params=parameters)
response.raise_for_status()  # Ensure we raise an error for bad responses
data = response.json()
question_data = data["results"]