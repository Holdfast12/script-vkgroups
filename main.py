import config
import sqlite3
import requests
import time
import vk
import time
from collections import Counter

con = sqlite3.connect("base.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS groups")
cur.execute("""CREATE TABLE IF NOT EXISTS groups (
keyword TEXT,
groupsforkey TEXT
)""")
con.close()

'''
def dbinput(keyword, groupsforkey):
    con = sqlite3.connect("base.db")
    cur = con.cursor()
    cur.executemany("INSERT INTO groups (keyword, groupsforkey) VALUES (?, ?)", zip(keyword, groupsforkey))
    con.commit()
    con.close()
'''

def dbinput(word, groupsforkey):
    con = sqlite3.connect("base.db")
    cur = con.cursor()
    cur.executemany("INSERT INTO groups (keyword, groupsforkey) VALUES (?, ?)", (zip(word, groupsforkey)))
    con.commit()
    con.close()


def get_members(groupid):
    first = vk_api.groups.getMembers(group_id=groupid, v=5.92)  # Первое выполнение метода
    data = first["items"]  # Присваиваем переменной первую тысячу id'шников
    count = first["count"] // 1000  # Присваиваем переменной количество тысяч участников
    # С каждым проходом цикла смещение offset увеличивается на тысячу
    # и еще тысяча id'шников добавляется к нашему списку.
    for i in range(1, count+1):
        data = data + vk_api.groups.getMembers(group_id=groupid, v=5.92, offset=i*1000)["items"]
        time.sleep(0.3)
    return data


def save_groups(data, filename="groups.txt"):  # Функция сохранения базы в txt файле
    with open(filename, "w") as file:  # Открываем файл на запись
        # Записываем каждый id'шник в новой строке,
        # добавляя в начало "vk.com/id", а в конец перенос строки.
        for item in data:
            file.write(str(item) + "\n")


def enter_data(filename="data.txt"):  # Функция ввода базы из txt файла
    with open(filename) as file:  # Открываем файл на чтение
        b = []
        # Записываем каждую строчку файла в список,
        # убирая "vk.com/id" и "\n" с помощью среза.
        for line in file:
            b.append(line[9:len(line) - 1])
    return b


def get_intersection(group1, group2):
    group1 = set(group1)
    group2 = set(group2)
    intersection = group1.intersection(group2)  # Находим пересечение двух множеств
    all_members = len(group1) + len(group2) - len(intersection)
    result = len(intersection)/all_members * 100  # Высчитываем пересечение в процентах
    print("Пересечение аудиторий: ", round(result,2), "%", sep="")
    return list(intersection)


def union_members(group1, group2):
    group1 = set(group1)
    group2 = set(group2)
    union = group1.union(group2)  # Объединяем два множества
    return list(union)
'''
def grabgroups(word):
    data = [x['screen_name'] for x in (vk_api.groups.search(city_id = 169, q = word, offset=20)["items"])]  # Первое выполнение метода
    count = first["count"] // 20  # Присваиваем переменной количество тысяч участников
    # С каждым проходом цикла смещение offset увеличивается на тысячу
    # и еще тысяча id'шников добавляется к нашему списку.
    for i in range(1, count+1):
        data = data + vk_api.groups.getMembers(group_id=groupid, v=5.92, offset=i*20)["items"]
        time.sleep(0.3)
        print(data)
    return data
'''

def enter_ru_dict(filename="russian.txt"):  # Функция ввода базы из txt файла
    with open(filename) as file:  # Открываем файл на чтение
        b = []
        # Записываем каждую строчку файла в список,
        # убирая "vk.com/id" и "\n" с помощью среза.
        for line in file:
            b.append(line[:len(line) - 1])
    return b

def enter_en_dict(filename="english.txt"):  # Функция ввода базы из txt файла
    with open(filename) as file:  # Открываем файл на чтение
        b = []
        # Записываем каждую строчку файла в список,
        # убирая "vk.com/id" и "\n" с помощью среза.
        for line in file:
            b.append(line[:len(line) - 1])
    return b

def grabgroups(word):
    return [x['screen_name'] for x in (vk_api.groups.search(city_id = 169, q = word, sort = 6, count = 1000)['items'])]

alphabet = '123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz'
endict = enter_en_dict()
rudict = enter_ru_dict()


if __name__ == "__main__":
    token = config.TEMPTOKEN
    session = vk.Session(access_token=token)
    vk_api = vk.API(session, v = 5.92)
    #bobfilm = get_members("overheard_in_yaroslavl")
    #hdkinomania = get_members("yar_live")
    #get_intersection(bobfilm, hdkinomania)
    #union = union_members(bobfilm, hdkinomania)
    #save_data(union)
    #(vk_api.users.get(user_id=295872229))

    groups = []
    vkusers = []


    for i in endict:
        try:
            tempgroups = grabgroups(i)
            groups = groups + tempgroups
            time.sleep(0.3)
            words = list([i])*len(tempgroups)
            dbinput(words, tempgroups)
        except:
            while True:
                try:
                    grabgroups(i)
                    time.sleep(10)
                except:
                    print('Была ошибка на слове ' + i)
                else:
                    break
            continue
