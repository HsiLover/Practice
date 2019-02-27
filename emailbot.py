import requests
import re
import sqlite3
import time
import random
from bs4 import BeautifulSoup

sql = './email_harvest.sqlite'
email_re = r'[a-zA-Z0-9.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]*[a-zA-Z]+'
url_re = r'@(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?$@iS'

while True:
    print('Loading data from DB...')
    conn = sqlite3.connect(sql)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS email_harvest(id INTEGER NOT NULL UNIQUE PRIMARY KEY, source CHAR(200) NOT NULL, email CHAR(50) NOT NULL UNIQUE)')
    cur.execute('CREATE TABLE IF NOT EXISTS webpages(id INTEGER NOT NULL UNIQUE PRIMARY KEY, links CHAR(200) NOT NULL UNIQUE)')
    cur.execute('SELECT * FROM email_harvest ORDER BY id DESC LIMIT 1')
    previous = cur.fetchall()
    source = ''
    if previous:
        previous = previous[0]
        cur.execute('SELECT id FROM webpages WHERE links=\'{}\''.format(previous[1]))
        previous_cursor = cur.fetchall()[0][0]
        cur.execute('SELECT links FROM webpages ORDER BY id ASC LIMIT 1 WHERE id > {}'.format(previous_cursor))
        source = cur.fetchall()[0][0]
    cur.close()
    conn.close()
    if not source:
        source = input('Enter an url for me to start crawl around from: ')
    if not source.startswith('https://'):
        source = 'https://' + source
    try:
        print('Connecting to the page...')
        page = requests.get(source)
        content = page.content
        print(content[:50])
    except:
        print('Somehting went wrong...')
        continue
    print('Looking at the webpage...')
    if isinstance(content, bytes):
        content = content.decode()
    print('Sorting out emails and links...')
    soup = BeautifulSoup(content, 'html.parser')
    links = set([x['href'] for x in soup.find_all('a') if x['href'].startswith('https://')])
    emails = re.findall(email_re, content)
    count_email = 0
    count_link = len(links)

    for email in emails:
        conn = sqlite3.connect(sql)
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO email_harvest(source, email) VALUES(\'{}\', \'{}\')".format(source[:200], email.lower()))
        conn.commit()
        cur.close()
        conn.close()
        count_email += 1
    print('{} emails have been collected...'.format(count_email))

    for link in links:
        conn = sqlite3.connect(sql)
        cur = conn.cursor()
        print('='*20)
        print(link)
        print('='*20)
        cur.execute("INSERT OR IGNORE INTO webpages(links) VALUES(\'{}\')".format(link))
        conn.commit()
        cur.close()
        conn.close()

    print('{} links have been collected...'.format(count_link))
    rand = random.randrange(10, 20)
    time.sleep(rand)
