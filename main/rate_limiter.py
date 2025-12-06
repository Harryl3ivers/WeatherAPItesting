import time 
from typing import Dict, Any

class RateLimiter:
    def __init__(self,max_requests = 60,period_seconds=60):
        self.max_requests = max_requests
        self.period_seconds = period_seconds
        self.tokens = max_requests
        self.last_refill = time.time()
    
    def allow_request(self) -> bool:
        if self.tokens >=1: #check if there are available tokens the request can proceed
            self.tokens -= 1 #decrement the token count
            return True #allow the request
        return False #deny the request if no tokens are available
    
    def refill_tokens(self):
        current_time = time.time() #get the current time
        elapsed = current_time - self.last_refill #calculate the time elapsed since last refill
        self.tokens += (elapsed / self.period_seconds) * self.max_requests #calculate the number of tokens to add based on elapsed time
        if self.tokens > self.max_requests: #ensure tokens do not exceed max limit
            self.tokens = self.max_requests 
        self.last_refill = current_time #update the last refill time
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "max_requests": self.max_requests,
            "period_seconds": self.period_seconds,
            "available_tokens": self.tokens,
            "last_refill": self.last_refill
        }
    
    def reset(self):
        self.tokens = self.max_requests
        self.last_refill = time.time()
        
          