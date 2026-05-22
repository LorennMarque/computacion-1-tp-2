import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Listar todas las claves y valores que comienzan con "stats:"
def show_stats_keys_and_values():
    keys = r.keys('stats:*')
    for key in keys:
        print(key, r.get(key))

print("===========================================")
show_stats_keys_and_values()