import requests

url = "http://localhost:8001/rules/"
payload = {
    "rule_id": "1",
    "name": "Unused class in html",       # <-- required
    "language": "html",
    "slang": "html_rule",             # <-- required
    "tags": [],
    "parameters": [
        {
            "name": "",
            "type": "",         # <-- required
            "default": ""   # <-- required (renamed from default_value)
        }
    ]
}

response = requests.post(url, json=payload)
print("Status:", response.status_code)
print("Response:", response.text)
