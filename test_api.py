import requests


def calculate_calories(querystring: dict):
    url = "https://health-calculator-api.p.rapidapi.com/dcn"
    # querystring = {"age":"30","weight":"60","height":"170","gender":"male","activity_level":"sedentary","goal":"maintenance","equation":"mifflin"}
    headers = {
        "x-rapidapi-key": "c6acdb7671msh3db420552315f20p1db088jsn5b9018fe205d",
        "x-rapidapi-host": "health-calculator-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    return response.json()['caloric_needs']['calories']

if __name__ == '__main__':
    print(calculate_calories())