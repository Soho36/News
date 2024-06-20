import redis
r = redis.Redis(
    host='redis-17183.c281.us-east-1-2.ec2.redns.redis-cloud.com',
    port=17183,
    password='YeO79TVHe5vXcKQSOF843HQpwt9x0mDd'
)
r.set('foo', 'bar')

# print(r)

value = r.get('foo')
print(value)
