from typing import Literal
from webhooks import default_webhook, discord_webhook
from urllib.parse import urlparse
import pika
import json
import os

WEBHOOK_QUEUE_URL = os.getenv("WEBHOOK_QUEUE_URL")


webhook_options = {"default": default_webhook, "discord.com": discord_webhook}


def callback(ch, method, properties, body):
    # Get the url and state from the message
    print(body.decode("utf-8"))
    message = json.loads(body.decode("utf-8"))
    url: str = message["url"]
    state: bool = message["state"]

    # Parse the url to get the domain
    domain = urlparse(url).netloc

    print(f" [x] Received {domain}")

    # If the domain is in the webhook_options dictionary, use that function
    # Otherwise, use the default function
    if domain in webhook_options:
        result = webhook_options[domain](
            url,
            state,
        )
    else:
        result = webhook_options["default"](
            url,
            state,
        )

    # If the webhook was successful, send an acknowledgement
    if result:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        print(" [x] Failed to deliver webhook, requeuing")
        ch.basic_nack(delivery_tag=method.delivery_tag)


print(f" [*] Connecting to {WEBHOOK_QUEUE_URL}")
connection = pika.BlockingConnection(pika.ConnectionParameters(WEBHOOK_QUEUE_URL, 5672))
print(" [*] Connected")

print(" [*] Creating channel")
channel = connection.channel()

print(" [*] Creating queue")
channel.queue_declare(queue="webhook_queue")
print(" [*] Queue created")
channel.basic_qos(prefetch_count=1)
print(" [*] Setting prefetch count")
channel.basic_consume(
    queue="webhook_queue", auto_ack=False, on_message_callback=callback
)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
