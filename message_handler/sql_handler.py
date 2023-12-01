from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select
from urllib.parse import quote_plus


class State(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    state: bool = Field(default=False)
    time: datetime


class Webhook(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    url: str = Field(default=False, unique=True)
    time: datetime
    timeouts: Optional[int] = Field(default=0)


def create_db_and_tables(url):
    engine = create_engine(url, echo=True)
    SQLModel.metadata.create_all(engine)
    return engine


class StateHandler:
    def __init__(self, url, user, password, database):
        db_url = f"postgresql://{user}:{quote_plus(password)}@{url}/{database}"  # this is cursed
        self.engine = create_db_and_tables(db_url)

    async def get_state(self):
        with Session(self.engine) as session:
            statement = session.exec(
                select(State).order_by(State.time.desc()).limit(1)
            ).first()
            if not statement:
                return False
            print(f"RETURNING STATEMENT {statement}")
            return statement.state

    async def set_state(self, state: bool):
        with Session(self.engine) as session:
            expen_state = State(state=state, time=datetime.now())
            print(f"SETTING STATEMENT{expen_state}")
            session.add(expen_state)
            session.commit()
            return expen_state

    async def add_webhook(self, webhook: str):
        print(f"Adding webhook {webhook}")
        with Session(self.engine) as session:
            hook = Webhook(url=webhook, time=datetime.now())
            print(f"SETTING STATEMENT{hook}")
            session.add(hook)
            session.commit()
            return True
