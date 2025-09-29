import sqlite3
import datetime

class GenericDAO:
    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection

    def datetime_to_str(dt: datetime.datetime) -> str:
        if dt is None:
            return None
        else:
            return dt.isoformat()
    
    def str_to_datetime(s: str) -> datetime.datetime:
        if s is None:
            return None
        else:
            return datetime.datetime.fromisoformat(s)
