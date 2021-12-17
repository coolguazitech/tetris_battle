import sqlite3 as lite
import time


def create_table():
    conn = lite.connect('.\Tetris_Battle.db')
    cur = conn.cursor()

    try:
        cur.execute(
            '''
            CREATE TABLE PLAYER
            (
                ID             INT PRIMARY KEY,
                BADGE          CHAR(2),
                SCORE          INT,
                VERSION        TEXT,
                DATE           CHAR(30)
            )
            '''
        )

        cur.execute(
            '''
            INSERT INTO PLAYER 
            VALUES (?, ?, ?, ?, ?)
            ''',
            (1, 'D0', 0, "1.0.0", time.ctime())
        )

        conn.commit()

    except Exception as e:
        print(e)
    finally:
        conn.close()

def fetch(id):
    conn = lite.connect('.\Tetris_Battle.db')
    cur = conn.cursor()

    data = cur.execute(
        '''
        SELECT BADGE, SCORE, VERSION, DATE FROM PLAYER WHERE ID = ?
        ''',
        (id, )
    )

    data = list(data)
    conn.close()

    dict_info = {
        "BADGE": data[0][0],
        "SCORE": data[0][1],
        "VERSION": data[0][2],
        "DATE": data[0][3],
    }

    return dict_info

def update(id, dict_info):
    dict_old_info = fetch(1)
    dict_old_info.update(dict_info)
    conn = lite.connect('.\Tetris_Battle.db')
    cur = conn.cursor()
    cur.execute(
        '''
        UPDATE PLAYER
        SET BADGE = ?, SCORE = ?, VERSION = ?, DATE = ?
        WHERE ID = ?
        ''',
        (
            dict_old_info["BADGE"],
            dict_old_info["SCORE"],
            dict_old_info["VERSION"],
            dict_old_info["DATE"],
            id
        )
    )
    conn.commit()
    conn.close()

def drop_table():
    conn = lite.connect('.\Tetris_Battle.db')
    cur = conn.cursor()

    try:
        cur.execute(
            '''
            DROP TABLE PLAYER
            '''
        )
        conn.commit()
    except Exception as e:
        print(e)
    conn.close()



