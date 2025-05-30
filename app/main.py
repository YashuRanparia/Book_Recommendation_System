from fastapi import FastAPI
from .core.config import settings

app = FastAPI(title='Book Recommendation System')

print(f'{settings.app_name} is running.')

@app.get('/')
def root():
    return 'Server is running ...'