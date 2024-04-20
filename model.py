from pydantic import BaseModel


class Record(BaseModel):
    user: int
    event: int
    subscribe: bool