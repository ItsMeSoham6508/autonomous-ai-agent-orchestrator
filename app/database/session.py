import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

database_url = URL.create(
    drivername="postgresql+psycopg2",
    database=os.environ["DB_NAME"],
    username=os.environ["DB_USER"],
    port=int(os.environ["DB_PORT"]),
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
)

engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
