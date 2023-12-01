from typing import Union
import logging
import os
from fastapi import FastAPI
from pydantic import BaseModel
from sql_handler import StateHandler

import asyncio
import httpx

WEBHOOK_HANDLER_URL = os.getenv("WEBHOOK_HANDLER_URL")
POSTGRES_URL = os.getenv("POSTGRES_URL") or "db"
POSTGRES_USER = os.getenv("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") or "password"
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE") or "db"

# EXPEN_STATE = False

log = logging.getLogger(
    __name__,
)
# Set logging file
logging.basicConfig(
    filename="message_handler.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI()


@app.get("/")
def read_root():
    log.info("Hello World")
    return {"Hello": "World"}


sql_handler = StateHandler(
    url=POSTGRES_URL,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    database=POSTGRES_DATABASE,
)


class State(BaseModel):
    state: bool


@app.post("/update_state")
async def state_update(data: State):
    print(f"Updating state to {data.state}")

    state = data.state
    print(f"State is now {state}")
    print(f"Sending state to db")
    await sql_handler.set_state(data.state)

    print(f"Sending state to webhook handler")
    await send_state_to_webhook_handler(state)
    return {"state": state}


class Webhook(BaseModel):
    url: str


@app.post("/add_webhook")
async def state_update(data: Webhook):
    print(f"Adding webhook {data.url}")
    await sql_handler.add_webhook(data.url)
    return {"success": True}


@app.get("/state")
async def get_state():
    state = await sql_handler.get_state()
    return {"state": state}


async def send_state_to_webhook_handler(state: bool):
    print("Sending state to webhook handler")

    url = f"http://{WEBHOOK_HANDLER_URL}/invoke_webhooks"
    print(f"Sending to {url}")
    async with httpx.AsyncClient() as client:
        result = await client.post(url, json={"state": state})

    if result.status_code != 200:
        print("Failed to send state to webhook handler")
        print(result.text)
        return False
    print("Successfully sent state to webhook handler")
