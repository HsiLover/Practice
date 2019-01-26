import sqlite3
import re

conn = sqlite3.connect('email_list.sqlite')
cur = conn.cursor()

while True:
    question = input('Do you want to parse a list: [y]es or [n]o: ')
    if question == 'n': break
    elif question == 'y': pass

    file_name = input('What is the name of the file you want to parse? ')
    file_type = input('What type of emails does this file have? k for kickstarter, n for nonkickstarter: ')

    f = open(file_name, 'r')
    input_data = f.read()

    emails = input_data.split('\n')
    #emails = re.findall(r'[a-zA-Z0-9.-]+@[a-zA-Z0-9-]\.[a-zA-Z0-9.-]+', input_data)

    for number, email in enumerate(emails):
        emails[number] = email.lower()
        if email[-1] == '.': emails[number] = email[:-1]

    print(emails)

    cur.execute('CREATE TABLE IF NOT EXISTS kickstarter_database (email TEXT UNIQUE)')
    cur.execute('CREATE TABLE IF NOT EXISTS nonkickstarter_database (email TEXT UNIQUE)')

    if file_type == 'k':
        for email_entry in emails:
            cur.execute('INSERT OR IGNORE INTO kickstarter_database (email) VALUES(?)', (email_entry,))

    else:
        for email in emails:
            cur.execute('INSERT OR IGNORE INTO nonkickstarter_database (email) VALUES(?)', (email_entry,))

conn.commit()
cur.close()
