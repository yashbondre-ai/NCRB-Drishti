import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

print("Connecting to TiDB using PyMySQL + TLS...")

conn = pymysql.connect(
    host=os.getenv("TIDB_HOST"),
    port=int(os.getenv("TIDB_PORT", "4000")),
    user=os.getenv("TIDB_USER"),
    password=os.getenv("TIDB_PASSWORD"),
    database=os.getenv("TIDB_DATABASE"),
    ssl={
        "ca": os.getenv("TIDB_CA_PATH"),
    },
)

print("CONNECTED SUCCESSFULLY!")
print("Server:", conn.get_server_info())

conn.close()