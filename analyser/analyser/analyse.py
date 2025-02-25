import requests

url = "http://127.0.0.1:8000/api/analyze/"
data = {"filename": "data.pdf"}  # Ensure correct filename

response = requests.post(url, json=data)

print("Analyze Status:", response.status_code)
print("Response:", response.json())
