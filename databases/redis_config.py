import redis 

class RedisTools():

    def __init__(self, db: int = 0):
        try:
            client = redis.Redis(host='redis', port=6379, db=db)
            self.client = client
        except Exception as e:
            print(f"Error connecting to redis: {e}")
        
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