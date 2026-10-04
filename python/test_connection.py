
from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, URL

# Load .env from the project root
project_folder = Path(__file__).resolve().parent.parent
load_dotenv(project_folder / ".env")

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

if not all([host, port, database, username, password]):
    raise ValueError(
        "Missing database settings. Check your .env file."
    )

connection_url = URL.create(
    "mysql+pymysql",
    username=username,
    password=password,
    host=host,
    port=int(port),
    database=database,
)

engine = create_engine(connection_url)

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DATABASE(), VERSION()")
        )
        db_name, version = result.fetchone()

        print("Connection successful!")
        print("Database:", db_name)
        print("MySQL version:", version)

except Exception as error:
    print("Connection failed.")
    print("Error:", error)

finally:
    engine.dispose()
