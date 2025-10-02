from dataclasses import dataclass
import time
from fastapi import HTTPException
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
        print("in add token")
        print(self.tokens)
        self.last_refill_time = current_time

    def request_handling(self):
        self.add_token()
        print("before check")
        print(self.tokens)
        if self.tokens > 1:
            self.tokens=self.tokens-1
        else:
           raise HTTPException(status_code = 429, detail = "Too Many Requests" )
        

 
def Token_Handling(ip_addr : str):
    refill_time = time.time()
    bucket_cap = 90000
    default_tokens = 0
    token_rate = 100000
    token_bucket = TokenBucket(bucket_cap, default_tokens, ip_addr, token_rate, refill_time)
    token_bucket.request_handling()
        


