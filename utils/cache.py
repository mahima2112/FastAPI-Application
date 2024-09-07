import redis

class RedisCache:
    def __init__(self, host="localhost", port=6379, db=0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)
    
    def is_cached(self, product):
        return self.redis.get(product.name) == str(product.price)
    
    def cache_product(self, product):
        self.redis.set(product.name, str(product.price))
