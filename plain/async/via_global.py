from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from fastapi import FastAPI

from model import Record

import config
import mysql.connector


app = FastAPI(prefix="/plain/sync")


def connection() -> PooledMySQLConnection | MySQLConnectionAbstract:
    return mysql.connector.connect(
      host=config.host,
      user=config.user,
      password=config.password,
      database=config.database
    )


@app.post("/add")
def add_record(data: Record):
    with connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            f"replace into user_event(user, event, status) "
            f"value ({data.user}, {data.event}, '{'accepted' if data.subscribe else 'rejected'}')"
        )
        conn.commit()
    return {"status": 200}

