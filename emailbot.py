import httplib2
import re
import sqlite3

def sql_on():
    conn = sqlite3.connect(sql)
    cur = conn.cursor()

def sql_off():
    conn.commit()
    cur.close()
    conn.close()

sql = './email_harvest.sqlite'

sql_on()
cur.execute('CREATE TABLE IF NOT EXISTS email_harvest(id INTEGER NOT NULL UNIQUE PRIMARY KEY, source CHAR(200) NOT NULL, email CHAR(50))')
cur.execute('CREATE TABLE IF NOT EXISTS webpages(id INTEGER NOT NULL UNIQUE PRIMARY KEY, links CHAR(200) NOT NULL)')
cur.execute('SELECT * FROM email_harvest ORDER BY id DESC LIMIT 1')
previous = cur.fetchall()[0]
cur.execute(f'SELECT id FROM webpages WHERE links=\'{previous[1]}\'')
previous_cursor = cur.fetchall()[0][0]
cur.execute(f'SELECT links FROM webpages WHERE id > {previous_cursor}')
source = [x[0] for x in cur.fetchall()]
cursor = 0
if not source:
    source = input('Enter an url for me to start crawl around from: ')
