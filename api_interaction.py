import requests
import re

pattern = r"[^0-9\.]"

def calculate_calories(querystring: dict):
    url = "https://health-calculator-api.p.rapidapi.com/dcn"
    headers = {
        "x-rapidapi-key": "c6acdb7671msh3db420552315f20p1db088jsn5b9018fe205d",
        "x-rapidapi-host": "health-calculator-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    raw_response = response.json()['caloric_needs']['calories']
    str_response = re.sub(pattern, "", raw_response)
    return float(str_response)

if __name__ == '__main__':
    print(calculate_calories())