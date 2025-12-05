import time 
from typing import Dict, Any

class RateLimiter:
    def __init__(self,max_requests = 60,period_seconds=60):
        self.max_requests = max_requests
        self.period_seconds = period_seconds
        self.tokens = max_requests
        self.last_refill = time.time()