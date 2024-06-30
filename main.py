import requests
import key

PIXELA_ENDPOINT = "https://pixe.la/v1/users"

params = {
    "token": key.PIXELA_TOKEN,
    "username": key.PIXELA_USNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}
try:
    with open("resp_user.json") as fc:
        fc.readline()
except FileNotFoundError:
    with open("resp_user.json", "w") as fc:
        # request post to create a user
        response = requests.post(url=PIXELA_ENDPOINT, json=params)
        data = response.json()
        if data["isSuccess"]:
            fc.write("Success")
            print("User created with success!")
        else:
            print(f"Error creating: {data["message"]}")

graph_params = {
    "id": "pythonstudyhour1",
    "name": "Python Study",
    "unit": "hour",
    "type": "int",
    "color": "sora",
}
graph_endpoint = f"{PIXELA_ENDPOINT}/{key.PIXELA_USNAME}/graphs"

headers = {
    "X-USER-TOKEN": key.PIXELA_TOKEN,
}

response = requests.post(url=graph_endpoint, json=graph_params, headers=headers)
data = response.json()
print(data["message"])
