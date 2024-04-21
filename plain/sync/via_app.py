from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.requests import Request

from model import Record
import mysql.connector
import config

def connection():
    return mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.create_connection = connection
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/add")
def add_record(request: Request, data: Record):
    with request.app.state.create_connection() as conn, conn.cursor() as cur:
        cur.execute(
            f"replace into user_event(user, event, status) "
            f"value ({data.user}, {data.event}, '{'accepted' if data.subscribe else 'rejected'}')"
        )
        conn.commit()
    return {"status": 200}

