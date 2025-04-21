from dotenv import load_dotenv
import os


def load_DBconfig():
    load_dotenv()
    config = {
        'database': os.getenv('DATABASE'),
        'user': os.getenv('USER'),
        'password': os.getenv('PASSWORD')
    }

    return config


db_config = load_DBconfig()
