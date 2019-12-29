import requests
import time
from random import normalvariate
from config import *


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 1
    retry = 0
    while not retry == max_retries: # отправка запроса через back off factor
        resonse = requests.get(url, timeout=timeout)
        if resonse.status_code == 200:
            break
        time.sleep(delay)
        delay = min(delay * backoff_factor, timeout)
        delay += normalvariate(delay)
        retry += 1
    return resonse


def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}" # переменная, которая создаёт адрес url
    friends = get(query).json()["response"]["items"] # через функцию get обращаемся к созданным url и берём из него список друзей
    return friends
