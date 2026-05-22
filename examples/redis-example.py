import redis

r = redis.Redis(host='localhost', port=6379, db=0)
#print(r.get('foo'))

# Crear

# ex = expiracy time sec

r.set('foo', 'bar')
r.set('foo2', 'bar2')
r.set('foo3', 'bar3')
r.set('foo4', 'bar4')
r.set('foo5', 'bar5')

# Eliminar
r.delete('foo')

# Listar todas las claves y valores
def show_all_keys_and_values():
    keys = r.keys('*')
    for key in keys:
        print(key, r.get(key))


print("===========================================")
show_all_keys_and_values()
