from dotenv import load_dotenv
from os import getenv


load_dotenv()

def db_url() -> str:
    return getenv('DB_URL')

def bot_token() -> str: 
    return getenv('BOT_TOKEN')
