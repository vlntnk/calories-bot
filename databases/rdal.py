import redis
import datetime
from configs.validate_models import CPFC

class RedisDal:
    def __init__(self):
        self.rd = redis.Redis(host='redis', port=6379)

    def write_eaten(self, username: str, consumed: CPFC):
        today = datetime.date.today().strftime("%Y-%m-%d")
        key = f"{username}:{today}"
        self.rd.hincrbyfloat(key, "calories", consumed.calories)
        self.rd.hincrbyfloat(key, "proteins", consumed.proteins)
        self.rd.hincrbyfloat(key, "fats", consumed.fats)
        self.rd.hincrbyfloat(key, "carbohydrates", consumed.carbohydrates)
        return self.rd.hget(username, today)
    
    def show_todays(self, username):
        today = datetime.date.today().strftime("%Y-%m-%d")
        key = f"{username}:{today}"
        if not self.rd.exists(key):
            self.rd.hset(username, today, 0)
        result = CPFC(
            calories=float(self.rd.hget(key, 'calories') or 0),
            proteins=float(self.rd.hget(key, 'proteins') or 0),
            fats=float(self.rd.hget(key, 'fats') or 0),
            carbohydrates=float(self.rd.hget(key, 'carbohydrates') or 0),
        )
        return result
    
    def show_statistics(self, username: str):
        today = datetime.date.today()
        month_ago = today - datetime.timedelta(days=30)
        date_list = [
            (month_ago + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((today - month_ago).days + 1)
        ]

        results = []
        for date_str in date_list:
            key = f"{username}:{date_str}"
            if self.rd.exists(key):
                data = self.rd.hgetall(key)
                # Преобразуем байты в числа
                parsed = {k.decode(): int(v) for k, v in data.items()}
                results.append({
                    "date": date_str,
                    **parsed
                })

        return results
    
    def delete(self, username, date):
        return self.rd.hdel(username, date)
    
    def delete_user(self, username: str):
        if not self.rd.exists(username):
            return 
        return self.rd.delete(username)