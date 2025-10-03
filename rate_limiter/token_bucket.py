from dataclasses import dataclass
import time
from fastapi import HTTPException, Request
import logging


logger = logging.getLogger(__name__)

@dataclass
class TokenBucket:
    """Token bucket 
Capacity - N tokens
Per IP address 
Rate of token 
"""
    bucket_capacity : int = 90000
    tokens : int = 0
    ip_address : str = "no ip"
    token_rate : int = 1000000
    last_refill_time : time = time.time()

    def add_token(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_refill_time
        new_token = elapsed_time*self.token_rate
        self.tokens = min(self.bucket_capacity, new_token + self.tokens)
        self.last_refill_time = current_time

    def request_handling(self):
        self.add_token()
        if self.tokens > 1:
            self.tokens=self.tokens-1
        else:
           raise HTTPException(status_code = 429, detail = "Too Many Requests" )
        

 
def Token_Handling(ip_addr : str):
    refill_time = time.time()
    bucket_cap = 90000
    default_tokens = 0
    token_rate = 1000000
    token_bucket = TokenBucket(bucket_cap, default_tokens, ip_addr, token_rate, refill_time)
    token_bucket.request_handling()
        


def Window_counter(window_size : int, req : Request, max_limit : int):

    request_counter = {}

    current_time = int(time.time())
    current_window = current_time // window_size
    window_start = current_window*window_size
    ip_addr = req.client.host
    prev_counter, count = request_counter.get(ip_addr,(None, 0))

    if prev_counter!= window_start:
        request_counter[ip_addr] = (window_start,1)
    else:
        if count>= max_limit:
           raise HTTPException(429, detail="Too many Requests")
        else:
            request_counter[ip_addr] = (window_start,count+1)
        

