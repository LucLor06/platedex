import os
from dotenv import load_dotenv
from pathlib import Path

path = Path(__file__).resolve().parent / '.env'

load_dotenv(path)

DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
PUBLIC_FACING_ADDRESS = os.getenv('PUBLIC_FACING_ADDRESS')
DJANGO_DEBUG = True if os.getenv('DJANGO_DEBUG') == 'True' else False
DJANGO_EMAIL_USER = os.getenv('DJANGO_EMAIL_USER')
DJANGO_EMAIL_PASSWORD = os.getenv('DJANGO_EMAIL_PASSWORD')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')