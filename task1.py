import random
import time
from functools import lru_cache

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = []
    
    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest_key = self.order.pop(0)
            del self.cache[oldest_key]
        self.cache[key] = value
        self.order.append(key)
    
    def invalidate(self, index):
        keys_to_remove = [key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_remove:
            del self.cache[key]
            self.order.remove(key)

N = 100000
array = [random.randint(1, 1000) for _ in range(N)]


Q = 50000
queries = []
for _ in range(Q):
    if random.random() < 0.7:
        L, R = sorted(random.sample(range(N), 2))
        queries.append(('Range', L, R))
    else:
        index = random.randint(0, N-1)
        value = random.randint(1, 1000)
        queries.append(('Update', index, value))


def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value


cache = LRUCache(1000)

def range_sum_with_cache(array, L, R):
    cached_result = cache.get((L, R))
    if cached_result is not None:
        return cached_result
    result = sum(array[L:R+1])
    cache.put((L, R), result)
    return result

def update_with_cache(array, index, value):
    array[index] = value
    cache.invalidate(index)

start_time = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_no_cache(array, query[1], query[2])
    else:
        update_no_cache(array, query[1], query[2])
no_cache_time = time.time() - start_time


start_time = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_with_cache(array, query[1], query[2])
    else:
        update_with_cache(array, query[1], query[2])
cache_time = time.time() - start_time


print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")