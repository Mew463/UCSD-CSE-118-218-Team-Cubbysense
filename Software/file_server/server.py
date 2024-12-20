from fastapi import FastAPI
import logging
from db.db_utils import create_db_and_tables, seed_leds
from api.routes import router

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Create the FastAPI app
app = FastAPI()

# Include the routes from routes.py
app.include_router(router)

# Create tables at startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_leds()
