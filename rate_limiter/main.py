import logging
from fastapi import FastAPI, Request
from token_bucket import Token_Handling, Window_counter

logging.basicConfig(
    level=logging.INFO,  # INFO, DEBUG, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

WINDOW_SIZE = 60
MAX_REQUEST = 100

@app.get("/")
def main_page():
    return "This is the main page"

@app.get("/unlimited")
def unlimited_endpoint():
    return "Unlimited! Let's Go!"

@app.get("/limited")
def limited_endpoint(req : Request):
    ip_addr = req.client.host
    Window_counter(WINDOW_SIZE, req, MAX_REQUEST)
    Token_Handling(ip_addr)
    return "Limited, don't over use me!"