import requests


def default_webhook(url: str, open: bool):
    if open:
        msg = "open"
    else:
        msg = "closed"

    data = {"state": msg}
    result = requests.post(url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        success = False
    else:
        print("Webhook delivered successfully, code {}.".format(result.status_code))
        success = True

    return success


def discord_webhook(url: str, open: bool):
    if open:
        msg = "Expen is open!"
    else:
        msg = "Expen is closed!"

    data = {"content": msg}
    result = requests.post(url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        success = False
    else:
        print("Webhook delivered successfully, code {}.".format(result.status_code))
        success = True

    return success


if __name__ == "__main__":
    discord_webhook(
        "https://discord.com/api/webhooks/1177985099325784114/kpbL9FuafM3OJ5zP_OAfUJfuuByll_2dQiwYb2NeyORisxe1SoPN5QAhK6slDBYMmsPP",
        False,
    )
