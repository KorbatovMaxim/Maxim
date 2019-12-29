import datetime as dt
from statistics import median
from typing import Optional
import statistics
from api import get_friends



def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, "bdate")
    ages = []
    for friend in friends:
        try:
            bd = friend["bdate"]
            if len(bd.split('.')) < 3:
                continue
            byear = int(bd.split('.')[2])
            nyear = int(dt.date.today().year)
            age = nyear - byear
            ages.append(age)
        except:
            pass
    return statistics.median(ages) 


if __name__ == "__main__":
    print(age_predict(383328527))