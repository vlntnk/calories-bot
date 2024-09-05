import redis
import datetime

class RedisDal:
    def __init__(self):
        self.rd = redis.Redis(host='localhost', port=6379)

    def write_eaten(self, username: str, calories: int):
        today = datetime.date.today().strftime("%Y-%m-%d")
        if not self.rd.hexists(username, today) or not self.rd.exists(username):
            self.rd.hset(username, today, calories)
        else:
            self.rd.hincrbyfloat(username, today, calories)
        return self.rd.hget(username, today)
    
    def show_todays(self, username):
        today = datetime.date.today().strftime("%Y-%m-%d")
        if not self.rd.exists(username):
            self.rd.hset(username)
        result = self.rd.hget(username, today)
        return result
    
    def show_statistics(self, username: str):
        if not self.rd.exists(username):
            self.rd.hset(username)
        result = self.rd.hgetall(username)
        return result