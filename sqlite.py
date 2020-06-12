import sqlite3
from datetime import datetime
import pytz

__connection = None


def get_connection():
    global __connection
    try:

        if __connection is None:
            __connection = sqlite3.connect("base.db",check_same_thread=False)
        return __connection
    except:
        return None

def unit_db(force: bool = False):
    try:
        conn = get_connection()
        c = conn.cursor()
        if force:
            c.execute('DROP TABLE IF EXISTS users')
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id             INTEGER PRIMARY KEY,
        user_id            INTEGER NOT NULL UNIQUE ,
        link               TEXT NOT NULL,
        start_time         INTEGER NOT NULL,
        end_time           INTEGER NOT NULL,
        last_pars          TIMESTAMP,
        vk                 INTEGER NOT NULL
       )
        ''')
        conn.commit()
        return True
    except:
        return False

def add_users_user(user_id:int,link:str,start_time:int,end_time:int,last_pars):
    try:

        conn = get_connection()
        c = conn.cursor()
        c.execute('INSERT INTO users (user_id,link,start_time,end_time,last_pars,vk) VALUES (?,?,?,?,?,?)',(user_id,link,start_time,end_time,last_pars,0))
        conn.commit()
        return True
    except:
        return False

def select_users_check_user_time(user_id:int):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT start_time FROM users WHERE user_id=?', (user_id,))
        conn.commit()
        res = c.fetchone()
        if int(res[0])>-1:
            return True
    except:
        return False

def update_user_link(user_id,link,tstap):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(f"UPDATE users SET link='{link}', last_pars={tstap} WHERE user_id={user_id}")
        conn.commit()
        return True

    except:
        return False

def set_user_link(user_id,link):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute('UPDATE users SET link=(?),start_time=0,end_time=24,last_pars=1000, vk=0 WHERE user_id=(?)',(link,user_id))
        conn.commit()
        return True

    except:
        return False

def update_user_time(user_id,start_time,end_time):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(f'UPDATE users SET start_time={start_time},end_time={end_time}  WHERE user_id={user_id}')
        conn.commit()
        return True

    except:
        return False

def select_users_user_all(user_id:int):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        conn.commit()
        res = c.fetchone()
        return res
    except:
        return None

def update_vk(user_id,vk=0):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(f'UPDATE users SET vk={vk}  WHERE user_id={user_id}')
        conn.commit()
        return True

    except:
        return False

def update_last_pars(user_id,last_pars=0):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(f'UPDATE users SET last_pars={last_pars}  WHERE user_id={user_id}')
        conn.commit()
        return True

    except:
        return False



def select_users_for_pars():
    try:
        moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
        hour=int(moscow_time.hour)
        print('time '+str(hour))
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE vk=1 and {}>=start_time and {}<end_time'.format(hour,hour))
        conn.commit()
        res = c.fetchall()
        if len(res)>0:
            return res
        else:
            return None
    except:
        return None

