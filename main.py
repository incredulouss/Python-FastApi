from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import os


app = FastAPI()
load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

mongo_uri = f"mongodb+srv://{db_username}:{db_password}@{db_host}/{db_name}"
# Try connecting to MongoDB and catch connection issues
try:
    conn = MongoClient(mongo_uri)
    conn.admin.command('ping')  # Check the connection by pinging the server
    print("MongoDB connection: Successful")
except ConnectionFailure as e:
    print(f"MongoDB connection: Failed - {e}")


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    try:
        # Access the notes collection
        docs = conn.notes.notes.find({})
        notes = [doc for doc in docs]  # Fetch all documents into a list
        print("Documents in MongoDB:", notes)
        
        return templates.TemplateResponse(
            "index.html", {"request": request, "notes": notes}
        )
    except Exception as e:
        print(f"Error while fetching data: {e}")
        return templates.TemplateResponse(
            "error.html", {"request": request, "error": str(e)}
        )
