import config
import sqlite3,time,re, pandas as pd

class Employee:
    def __init__(self, fio, group, card):
        self.fio = fio
        self.group = group
        self.card = card
    def __str__(self):
        return f"<b>Специалист:</b>\n{self.group}\n{self.fio}\n<code>{self.card}</code>" + "\n"


def initDB():
    conn = sqlite3.connect(config.DB_NAME + '.sqlite')
    df = pd.read_excel('info.xlsx')
    df.to_sql(name='employees', con=conn, if_exists='replace')
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS admin_list (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,user_id VARCHAR UNIQUE, add_date datetime);")
    cursor.execute(f"INSERT OR IGNORE INTO admin_list (user_id,add_date)VALUES ('{str(config.MAIN_ADMIN)}','{str(time.strftime('%Y-%m-%d %H:%M:%S'))}')")
    conn.commit()
    cursor.close()
    conn.close()

def isAdmin(chat_id):
    conn = sqlite3.connect(config.DB_NAME + '.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"SELECT user_id FROM admin_list WHERE user_id = '{chat_id}'")
    user_fetched = cursor.fetchone()
    cursor.close()
    conn.close()
    user = True if user_fetched != None else False
    return user

def changeAdmin(message):
    conn = sqlite3.connect(config.DB_NAME + '.sqlite')
    cursor = conn.cursor()
    action, chat_id = message.split(":")[1:]
    res = "Неверная команда"
    if action == "добавить":
        cursor.execute(f"INSERT OR IGNORE INTO admin_list (user_id,add_date)VALUES ('{chat_id}','{str(time.strftime('%Y-%m-%d %H:%M:%S'))}')")
        res =  "Успешно добавлен новый админ"
    if action == "удалить":
        cursor.execute(f"DELETE FROM admin_list WHERE user_id ='{chat_id}';")
        res = "Успешно удален админ"
    conn.commit()
    cursor.close()
    conn.close()
    return res

def searchByParam(message):
    conn = sqlite3.connect(config.DB_NAME + '.sqlite')
    cur = conn.cursor()
    action, search_parameter  = message.split(":")[1:]

    if action == "фио":
        like_statement = ' AND `fio` LIKE '.join(f"'%{word}%'" for word in search_parameter.split(" "))
        cur.execute(f"SELECT * FROM employees WHERE `fio` LIKE {like_statement}")
    elif action == "отдел":
        like_statement = ' AND `group` LIKE '.join(f"'%{word}%'" for word in search_parameter.split(" "))
        cur.execute(f"SELECT * FROM employees WHERE `group` LIKE {like_statement}")
    elif action == "карта":
        cur.execute(f"SELECT * FROM employees WHERE `card` = '{search_parameter}'")
    res = '\n'.join(str(Employee(row[1],row[2],row[3])) for row in cur) if cur else "Неправильная команда"
    cur.close()
    conn.close()
    return res
def searchReg(message):
    conn = sqlite3.connect(config.DB_NAME + '.sqlite')
    cur = conn.cursor()

    # if message is a numeric value
    if re.match('^[0-9\,]*$', message):
        cur.execute(f"SELECT * FROM employees WHERE `card` = '{message}'")
    # if message is (word word word) or (word word)
    elif re.fullmatch('[а-яё\-]+\s+[а-яё\-]+(?:\s+[а-яё\-]+)?', message.lower()):
        like_statement = ' AND `fio` LIKE '.join(f"'%{word}%'" for word in message.split(" "))
        cur.execute(f"SELECT * FROM employees WHERE `fio` LIKE {like_statement}")
    else:
        like_statement = ' AND `group` LIKE '.join(f"'%{word}%'" for word in message.split(" "))
        cur.execute(f"SELECT * FROM employees WHERE `group` LIKE {like_statement}")

    res = '\n'.join(str(Employee(row[1],row[2],row[3])) for row in cur) if cur else "Неправильная команда"
    cur.close()
    conn.close()

    return res
