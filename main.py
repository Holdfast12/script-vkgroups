import config
import sqlite3
import requests
import time
import vk
import time

con = sqlite3.connect("base.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS clients")
cur.execute("""CREATE TABLE IF NOT EXISTS clients (
vkid INTEGER PRIMARY KEY,
inyaroslavl INTEGER,
ingroup INTEGER,
infriends INTEGER,
inmessages INTEGER
)""")
con.close()

def dbinput(userid):
    con = sqlite3.connect("base.db")
    cur = con.cursor()
    cur.executemany("INSERT INTO clients (vkid) VALUES (?)", zip(userid))
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
        print(data)
        time.sleep(0.15)
    dbinput(data)


def save_data(data, filename="data.txt"):  # Функция сохранения базы в txt файле
    with open(filename, "w") as file:  # Открываем файл на запись
        # Записываем каждый id'шник в новой строке,
        # добавляя в начало "vk.com/id", а в конец перенос строки.
        for item in data:
            file.write("vk.com/id" + str(item) + "\n")


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


if __name__ == "__main__":
    token = config.TOKEN
    session = vk.Session(access_token=token)
    vk_api = vk.API(session, v = 5.81)
    #bobfilm = get_members("overheard_in_yaroslavl")
    #hdkinomania = get_members("massage_malinina")
    #get_intersection(bobfilm, hdkinomania)
    #union = union_members(bobfilm, hdkinomania)
    #save_data(union)
    print(vk_api.users.get(user_id=295872229))