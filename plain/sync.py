from fastapi import FastAPI

from model import Record
import mysql.connector
import config


app = FastAPI()


def connection():
    return mysql.connector.connect(
      host=config.host,
      user=config.user,
      password=config.password,
      database=config.database
    )


@app.post("/add")
def add_record(data: Record):
    with connection() as conn, conn.cursor() as cur:
        cur.execute(
            f"replace into user_event(user, event, status) "
            f"value ({data.user}, {data.event}, '{'accepted' if data.subscribe else 'rejected'}')"
        )
        conn.commit()
    return {"status": 200}

