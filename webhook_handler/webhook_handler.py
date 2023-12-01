import pika
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from sqlmodel import Field, SQLModel, create_engine, Session, select
from pydantic import BaseModel
from typing import Literal, Optional, Sequence
from datetime import datetime
import logging
import os
import json
from urllib.parse import quote_plus

WEBHOOK_QUEUE_URL = os.getenv("WEBHOOK_QUEUE_URL")
POSTGRES_URL = os.getenv("POSTGRES_URL") or "db"
POSTGRES_USER = os.getenv("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") or "password"
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE") or "db"

# Set logging file
logging.basicConfig(
    filename="message_handler.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

log = logging.getLogger(__name__)


class Webhook(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(default=False, unique=True)
    time: datetime
    timeouts: int = Field(default=0)


def create_db_and_tables():
    try:
        db_url = f"postgresql://{POSTGRES_USER}:{quote_plus(POSTGRES_PASSWORD)}@{POSTGRES_URL}/{POSTGRES_DATABASE}"  # this is cursed
        engine = create_engine(db_url, echo=True)
        SQLModel.metadata.create_all(engine)
        log.info("Database and tables created")
    except Exception as e:
        print("Failed to create database and tables")
        print(e)
        engine = None

    if not engine:
        print("Failed to create engine")
        raise Exception("Failed to create engine")

    return engine


async def get_webhooks() -> Sequence[Webhook]:
    try:
        with Session(engine) as session:
            statement = session.exec(select(Webhook)).all()
            print("Webhooks retrieved from database")
            print(statement)
            result = statement
            return result
    except Exception as e:
        print("Failed to retrieve webhooks from database")
        print(e)
        return []


app = FastAPI()
engine = create_db_and_tables()


@app.post("/")
async def index():
    return {"status": "success"}


class State(BaseModel):
    state: bool


@app.post("/invoke_webhooks")
async def invoke_webhook(data: State):
    print(f"Invoking webhooks with state {data.state}")
    hooks: Sequence[Webhook] = await get_webhooks()
    if not hooks:
        print("No webhooks found")
        return {"status": "No webhooks found"}
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            WEBHOOK_QUEUE_URL, heartbeat=600, blocked_connection_timeout=300
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue="webhook_queue")
    log.info(f"Sending {len(hooks)} webhooks to queue")
    for hook in hooks:
        url: str = hook.url
        payload = {"url": url, "state": data.state}
        # Establish a connection with RabbitMQ server

        print(f"Sending {payload} to queue")
        channel.basic_publish(
            exchange="", routing_key="webhook_queue", body=json.dumps(payload)
        )
        log.info(f"Sent {url} to queue")
    channel.close()
    return {"status": "success"}
