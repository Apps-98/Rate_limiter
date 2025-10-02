import logging
from fastapi import FastAPI, Request
from token_bucket import Token_Handling

logging.basicConfig(
    level=logging.INFO,  # INFO, DEBUG, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def main_page():
    return "This is the main page"

@app.get("/unlimited")
def unlimited_endpoint():
    return "Unlimited! Let's Go!"

@app.get("/limited")
def limited_endpoint(req : Request):
    ip_addr = req.client.host
    Token_Handling(ip_addr)
    return "Limited, don't over use me!"