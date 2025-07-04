import os

from dotenv import load_dotenv

def load_env():
    """Loads environment variables from a .env file"""

    dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
    load_dotenv(dotenv_path)