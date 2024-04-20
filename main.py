from fastapi import FastAPI
import config
import mysql.connector

app = FastAPI(
    title="A test server for discovering the fastest endpoint solve"
)

@app.get('/ping')
def ping():
    return "pong"

@app.post("/database/set")
def set_database(database: str):
    config.database = database
    return {"status": 200}


@app.post("/database/clear")
def clear_database():
    with mysql.connector.connect(
      host=config.host,
      user=config.user,
      password=config.password,
      database=config.database
    ) as conn, conn.cursor() as cursor:
        cursor.execute("truncate table user_event;")
        conn.commit()
    return {"status": 200}

