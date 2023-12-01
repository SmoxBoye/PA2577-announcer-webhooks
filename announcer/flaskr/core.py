from hmac import compare_digest  # compare_digest is used to prevent timing attacks


from flask import Blueprint, render_template, request, current_app

# import socket
# import ssl
from datetime import datetime, timedelta
import requests

bp = Blueprint("core", __name__, url_prefix="/")

is_expen_open = False
latest_heartbeat = datetime(1337, 5, 11, 2, 44, 20)


def check_heartbeat(minutes=0, seconds=60):
    """check_heartbeat Check if the heartbeat is within the minutes and seconds specified

    Args:
        minutes (int, optional): Amount of minutes allowed since last heartbeat. Defaults to 5.
        seconds (int, optional): Amount of seconds allowed since last heartbeat. Defaults to 0.

    Returns:
        Bool: Returns True if the heartbeat is within the time specified, False if it is not.
    """

    global latest_heartbeat

    # If the time since the latest heartbeat is greater than the time specified, return False
    if datetime.now() - latest_heartbeat > timedelta(minutes=minutes, seconds=seconds):
        return False
    else:
        return True


@bp.route("/")
def index():
    """index The route for the index page of the website (the main page)

    Checks if the heartbeat is within the last x minutes, if it is, it will return the state of the door.
    If not it will return an error page.

    Returns:
        render_template: A render_template of the index.html page or the oops.html page
    """
    # return current_app.root_path

    # global is_expen_open

    message_url = current_app.config["MESSAGE_HANDLER_URL"]
    state = requests.get(f"http://{message_url}/state").json()["state"]
    print(state)
    # if check_heartbeat():
    #     return render_template("index.html", open=is_expen_open)
    # else:
    #     return render_template("oops.html")
    return render_template("index.html", open=state)


@bp.route("/update", methods=["POST"])
def update():
    """update Receives a POST request from the ESP32 and updates the database

    Returns "Opened" if the door is opened, "Closed" if the door is closed, "Wrong key" if the key is wrong

    Returns:
        str: A confirming string of the state of the door
    """

    data = request.get_json()
    key = data["api_key"]
    state = data["sensor"]
    print(state)

    global is_expen_open

    if compare_digest(key, current_app.config["SECRET_KEY"]) and state == "1":
        is_expen_open = True
        return "Opened"
    elif compare_digest(key, current_app.config["SECRET_KEY"]) and state == "0":
        is_expen_open = False
        return "Closed"
    else:
        return "Invalid"


@bp.route("/heartbeat", methods=["POST"])
def heartbeat():
    """heartbeat Receives a heartbeat from the ESP32 and updates the database

    Returns:
        str: A confirming string that the heartbeat was received
    """
    data = request.get_json()
    key = data["api_key"]

    global latest_heartbeat

    if compare_digest(key, current_app.config["SECRET_KEY"]):
        latest_heartbeat = datetime.now()
        return "Heartbeat received"
    else:
        return "Invalid"


@bp.route("/add_webhook", methods=["POST"])
def add_webhook():
    """add_webhook Receives a request from the user (API) and adds a webhook to the database

    Returns:
        str: A confirming string that the webhook was added
    """
    data = request.get_json()
    url = data["url"]

    message_handler = current_app.config["MESSAGE_HANDLER_URL"]

    requests.post(f"http://{message_handler}/add_webhook", json={"url": url})
    return "Webhook added"


@bp.route("/update_state", methods=["POST"])
def update_state():
    """update_state Receives a request from the backend and updates the state of the door

    Returns:
        str: A confirming string that the state was updated
    """
    data = request.get_json()
    print(data)
    state = data["state"]
    print(state)
    result = requests.post(
        f"http://{current_app.config['MESSAGE_HANDLER_URL']}/update_state",
        json={"state": state},
    )
    if result.status_code != 200:
        return f"Error: {result.status_code}"
    print(result.json())

    return f"State updated to {result.json()}"
