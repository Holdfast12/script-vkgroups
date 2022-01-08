import config
import sqlite3
import requests
import time
import vk
import time
import math
from collections import Counter

con = sqlite3.connect("hardbase.db")
cur = con.cursor()
#cur.execute("DROP TABLE IF EXISTS groups")
cur.execute("""CREATE TABLE IF NOT EXISTS groups (
keyword TEXT,
groupsforkey TEXT
)""")
con.close()

con = sqlite3.connect("base.db")
cur = con.cursor()
#cur.execute("DROP TABLE IF EXISTS groups")
cur.execute("""CREATE TABLE IF NOT EXISTS groups (
group_id TEXT PRIMARY KEY,
members_count INTEGER,
can_post INTEGER,
activity TEXT,
status TEXT,
verified INTEGER,
is_closed INTEGER,
type TEXT,
can_create_topic INTEGER,
can_message INTEGER,
can_upload_doc INTEGER,
can_upload_video INTEGER,
has_photo INTEGER,
wall INTEGER
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
    con = sqlite3.connect("hardbase.db")
    cur = con.cursor()
    cur.executemany("INSERT INTO groups (keyword, groupsforkey) VALUES (?, ?)", (zip(word, groupsforkey)))
    con.commit()
    con.close()

def dbselectunical():
    con = sqlite3.connect("base.db")
    cur = con.cursor()
    cur.execute("SELECT group_id FROM groups")
    groups.extend(cur.fetchall())
    con.close()

def dbselecalready():
    con = sqlite3.connect("base.db")
    cur = con.cursor()
    cur.execute("SELECT group_id FROM groups WHERE from_yaroslavl NOT NULL AND banned_count NOT NULL")
    groupsalready.extend(cur.fetchall())
    con.close()

def dbinsertunical(idgroups):
    con = sqlite3.connect("base.db")
    cur = con.cursor()
    cur.executemany("INSERT INTO groups (group_id) VALUES (?)", (idgroups))
    con.commit()
    con.close()


def get_members(groupid):
    first = vk_api.groups.getMembers(group_id=groupid, fields='city', v=5.92)  # Первое выполнение метода
    data = first["items"]  # Присваиваем переменной первую тысячу id'шников
    count = first["count"] // 1000  # Присваиваем переменной количество тысяч участников
    # С каждым проходом цикла смещение offset увеличивается на тысячу
    # и еще тысяча id'шников добавляется к нашему списку.
    for i in range(1, count+1):
        data = data + vk_api.groups.getMembers(group_id=groupid, v=5.92, fields='city', offset=i*1000)["items"]
        time.sleep(0.4)
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

#возвращает группы, найденные по ключевому слову word
def grabgroups(word):
    return [x['screen_name'] for x in (vk_api.groups.search(city_id = 169, q = word, sort = 6, type = 'group', deactivated = None, count = 1000)['items'])]

def getaboutgroups(allgroups):
    tgroups = []
    tallgoups = allgroups
    print(len(tallgoups))
    for i in range(math.ceil((len(allgroups) / 500))):
        #for k in range((i+1)*500 - 500 : (i+1)*500):
        range1 = ((i+1)*500 - 500)
        range2 = ((i+1)*500)
        tgroups.append(tallgoups[range1:range2])
    return tgroups


def dbinputaboutgroups(word, groupsforkey):
    con = sqlite3.connect("base.db")
    cur = con.cursor()
    cur.executemany("INSERT INTO groups (keyword, groupsforkey) VALUES (?, ?)", (zip(word, groupsforkey)))
    con.commit()
    con.close()

def trashchecking(groupforcheckingtrash, groupname):
    trashcounter = 0
    yaroslavlcounter = 0
    for i in range(len(groupforcheckingtrash)):
        try:
            if groupforcheckingtrash[i]['deactivated'] == 'banned':
                trashcounter += 1
        except:
            pass
        try:
            if groupforcheckingtrash[i]['city']['title'] == 'Ярославль':
                yaroslavlcounter += 1
        except:
            pass
    return trashcounter, yaroslavlcounter, groupname


alphabet = '123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz'
endict = enter_en_dict()
rudict = enter_ru_dict()

if __name__ == "__main__":
    token = config.TEMPTOKEN
    session = vk.Session(access_token=token)
    vk_api = vk.API(session, v=5.92)
    #bobfilm = get_members("overheard_in_yaroslavl")
    #hdkinomania = get_members("yar_live")
    #get_intersection(bobfilm, hdkinomania)
    #union = union_members(bobfilm, hdkinomania)
    #save_data(union)
    #(vk_api.users.get(user_id=295872229))

    groups = []
    groupsalready = []
    vkusers = []
    groupswithouttuples = []
    groupsalreadywithouttuples = []

    dbselectunical()
    dbselecalready()
    groupswithouttuples = [x[0] for x in groups]
    groupsalreadywithouttuples = [x[0] for x in groupsalready]
    groupswithouttuples = list(filter(lambda x: x not in groupsalreadywithouttuples, groupswithouttuples))
    #dividedlists = getaboutgroups(groupswithouttuples)
    #membersofgroup = get_members('whitehousewot')
    for i in range(len(groupswithouttuples)):
        time.sleep(0.5)
        try:
            con = sqlite3.connect("base.db")
            cur = con.cursor()
            cur.execute("UPDATE groups SET banned_count = (?), from_yaroslavl = (?) WHERE group_id = (?)", (trashchecking(get_members(groupswithouttuples[i]), groupswithouttuples[i])))
            con.commit()
            con.close()
        except Exception as e:
            if str(e).find('Access') == -1 and str(e).find('Invalid') == -1:
                while True:
                    try:
                        time.sleep(0.5)
                        con = sqlite3.connect("base.db")
                        cur = con.cursor()
                        cur.execute("UPDATE groups SET banned_count = (?), from_yaroslavl = (?) WHERE group_id = (?)",(trashchecking(get_members(groupswithouttuples[i]), groupswithouttuples[i])))
                        con.commit()
                        con.close()
                    except Exception as r:
                        print(r)
                        time.sleep(10)
                    else:
                        break
            else:
                if str(e).find('Access') != -1:
                    time.sleep(0.5)
                    con = sqlite3.connect("base.db")
                    cur = con.cursor()
                    cur.execute("UPDATE groups SET banned_count = 0, from_yaroslavl = 0 WHERE group_id = (?)",(groupswithouttuples[i],))
                    con.commit()
                    con.close()
                if str(e).find('Invalid group id') != -1:
                    try:
                        time.sleep(0.5)
                        con = sqlite3.connect("base.db")
                        cur = con.cursor()
                        cur.execute("UPDATE groups SET banned_count = (?), from_yaroslavl = (?) WHERE group_id = (?)",(trashchecking(get_members(groupswithouttuples[i][4:]), groupswithouttuples[i])))
                        con.commit()
                        con.close()
                    except:
                        time.sleep(0.5)
                        con = sqlite3.connect("base.db")
                        cur = con.cursor()
                        cur.execute("UPDATE groups SET banned_count = -1, from_yaroslavl = -1 WHERE group_id = (?)",(groupswithouttuples[i],))
                        con.commit()
                        con.close()
                print(e)


'''
    for i in range(len(dividedlists)):
        dividedlists[i] = vk_api.groups.getById(group_ids=",".join(dividedlists[i]), v=5.131, fields="members_count,can_post,activity,status,verified,can_create_topic,can_message,can_upload_doc,can_upload_video,has_photo,wall")
        time.sleep(0.3)
        for k in range(len(dividedlists[i])):
            try:
                con = sqlite3.connect("base.db")
                cur = con.cursor()
                cur.execute("UPDATE groups SET can_create_topic = (?) WHERE group_id = (?)", (dividedlists[i][k]['can_create_topic'],dividedlists[i][k]['screen_name']))
                con.commit()
                con.close()
            except:
                print('нет количества участников '+ dividedlists[i][k]['screen_name'])
    print(len(trashcounter))

    for i in alphabet:
        try:
            time.sleep(0.3)
            tempgroups = grabgroups(i)
        except:
            while True:
                try:
                    time.sleep(0.3)
                    tempgroups = grabgroups(i)
                except Exception as e:
                    print('Была ошибка на слове ' + i + 'по причине: '+ str(e))
                    time.sleep(10)
                else:
                    break
        finally:
            groups = groups + tempgroups
            words = list([i]) * len(tempgroups)
            dbinput(words, tempgroups)
'''