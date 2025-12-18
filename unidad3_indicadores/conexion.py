import oracledb
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Database:
    def __init__(self):
        self.user = os.getenv("ORACLE_USER")
        self.password = os.getenv("ORACLE_PASSWORD")
        self.dsn = os.getenv("ORACLE_DSN")

    def get_connection(self):
        return oracledb.connect(user=self.user, password=self.password, dsn=self.dsn)

    def query(self, sql: str, params: Optional[dict] = None):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                result = cur.execute(sql, params or {})
                rows = result.fetchall() if sql.strip().upper().startswith("SELECT") else None
            conn.commit()
        return rows
