import requests
import stocks_request


response = requests.get("http://127.0.0.1:5000/quarks")

# newResponse = requests.get(
# "http://127.0.0.1:5000/quarks")

# newResponse = requests.delete("http://127.0.0.1:5000/quarks/top")

print(response.text)
