import redis 

class RedisTools():

    def __init__(self, db: int = 0):
        client = redis.Redis(host='localhost', port=6379, db=db)
        self.client = client
        
    def set(self, key, value):
        return self.client.set(name=key, value=value)

    def get(self, key):
        return self.client.get(key)

    def close(self):
        self.client.close()

if __name__ == '__main__':
    rd = RedisTools()
    rd.set('hi', 'hello')
    print(rd.get('hi'))