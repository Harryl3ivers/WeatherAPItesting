import time 

class CacheManager:
    def __init__(self):
        self.cache = {} #create an empty dictionary to store cache items
        self.expiration_time = 300  # Cache expiration time in seconds (5 minutes)
        self.hits = 0 #number of cache hits - items found in cache
        self.misses = 0 #number of cache misses - items not found in cache
    
    def get(self, key): #retrieve item from cache
        if key not in self.cache: #check if key exists in cache
            self.misses += 1 #if not, increment misses counter
            return None #return None if key not found
        item = self.cache[key] #get the cached item

        if time.time() >item["expires"]: #check if item has expired
            del self.cache[key] #remove expired item from cache
            self.misses +=1 #increment misses counter
            return None
        
        self.hits += 1  #increment hits counter
        return item["value"] #return the cached value
    
    def set(self, key, value):
        self.cache[key] = { #store the value along with its expiration time
            "value": value,
            "expires": time.time() + self.expiration_time
        }
    
    def delete(self, key):
        if key in self.cache: #check if key exists in cache
            del self.cache[key] #remove the item from cache
    
    def clear(self):
        self.cache.clear() #clear the entire cache
    
    def get_stats(self): #return cache statistics
        return {
            "hits": self.hits, 
            "misses": self.misses,
            "size": len(self.cache)
        }
