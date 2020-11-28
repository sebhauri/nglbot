import requests
import json

URL = "https://api.telegram.org/bot1432985981:AAHxLzTlnqVH8uo20PPuhDFSqbWqp6hBlJw/"

def query(action, params={}, method="GET"):
    r = None
    if method == "GET":
        r = requests.get(URL + action, params=params)
    elif method == "POST":
        r = requests.post(URL + action, params=params)
    else:
        print("Wrong method name")

    if r.status_code == 200:
        print(json.dumps(json.loads(r.text), indent=2))
    else:
        print("something went wrong :(")
        print(r.text)

def get_updates():
    query("getUpdates")

def set_webhook(url):
    query("setWebhook", {"url" : url})

def get_info():
    query("getMe")

def send(message, user):
    query("sendMessage", {"text" : message, "chat_id": user}, "POST")

def sendPic(user):
    pass


def main():
    send("Yolo", "476757080") # @username does not seem to work, why ?
    #get_info()
    #get_updates()

main()