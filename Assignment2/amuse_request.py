import requests
import json


def send_request(text):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = [ {"text":text, "lang":"FA"} ]

    json_data = json.dumps(data)

    response = requests.post('http://127.0.0.1/api/model', headers=headers, data=json_data)

    response_dict = json.loads(response.text)

    return response_dict[0]['tokens']


# print(send_request("قیمت اجناس افزایش پیدا کرده است."))
