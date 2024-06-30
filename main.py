import requests
import key
import datetime as dt

PIXELA_ENDPOINT = "https://pixe.la/v1/users"

global formatted_date

params = {
    "token": key.PIXELA_TOKEN,
    "username": key.PIXELA_USNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

headers = {
    "X-USER-TOKEN": key.PIXELA_TOKEN,
}

try:
    with open("resp_user.json") as fc:
        data_file = fc.readline()
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

if "graph ok" not in data_file:

    graph_params = {
        "id": key.PIXELA_GRAPHID,
        "name": "Python Study",
        "unit": "hour",
        "type": "int",
        "color": "sora",
    }
    graph_endpoint = f"{PIXELA_ENDPOINT}/{key.PIXELA_USNAME}/graphs"
    response = requests.post(url=graph_endpoint, json=graph_params, headers=headers)

    data = response.json()

    if data["message"] == "Success.":

        with open("resp_user", "w") as fc:
            fc.write('{"Success":  "graph ok"}')

else:

    date = dt.datetime.now()
    formatted_date = date.strftime("%Y%m%d")

    list_pixels_endpoint = f"{PIXELA_ENDPOINT}/{key.PIXELA_USNAME}/graphs/{key.PIXELA_GRAPHID}/pixels"
    response = requests.get(url=list_pixels_endpoint, headers=headers)
    print(response.text)

    dates = response.json()["pixels"]

    if formatted_date not in dates:

        valid = False
        quantity = None

        while not valid:
            quantity = input("Quantidade de horas de estudo: ")
            if quantity.isdigit():
                valid = True

        quantity = str(quantity)

        pixel_params = {
            "date": formatted_date,
            "quantity": quantity,
        }

        pixel_endpoint = f"{PIXELA_ENDPOINT}/{key.PIXELA_USNAME}/graphs/{key.PIXELA_GRAPHID}"
        response = requests.post(url=pixel_endpoint, headers=headers, json=pixel_params)
        print(response.json()["message"])

    else:

        answer = None

        while answer != "y" and answer != "n":
            answer = input("Update today? [y/n]").lower()

        if answer == "y":
            invalid = True
            quantity = None

            while invalid:
                quantity = input("Atualizar quantidade de horas de estudo: ")
                if quantity.isdigit():
                    invalid = False

            quantity = str(quantity)

            pixel_update_params = {
                "quantity": quantity
            }

            pixel_update_endpoint = f"{PIXELA_ENDPOINT}/{key.PIXELA_USNAME}/graphs/{key.PIXELA_GRAPHID}/{formatted_date}"
            response = requests.put(url=pixel_update_endpoint, headers=headers, json=pixel_update_params)
            print(response.json()["message"])

        else:

            print("Bye!")

# TODO delete pixel
