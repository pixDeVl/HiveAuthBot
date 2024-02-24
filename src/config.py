from dotenv import load_dotenv
import os


load_dotenv('./.env')
class Configuration:
    # Dev stuffs
    GUILD_ID = os.getenv('DEV_GUILD_ID')
    # Bot stuffs
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')

    # OAuth2 stuffs
    CONSUMER_KEY: str = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET: str = os.getenv('CONSUMER_SECRET')

    # Database stuff
    DB_URI: str = os.getenv('DB_URI')
    DB_ECHO: bool = bool(os.getenv('DB_ECHO'))