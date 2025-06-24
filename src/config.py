from dotenv import load_dotenv
from os import getenv


def db_url() -> str:
    load_dotenv()
    return getenv('DB_URL')

