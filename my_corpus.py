import os
import sqlite3
import re

def corpus(file_path):
    # it parses a single document
    dir = file_path.split(os.path.sep)[0] + os.path.sep
    file = file_path.split(os.path.sep)[1]
    dir_file = file_path.split('.')[0]

    if file + '_RosettaStone.sqlite' in os.listdir(dir):
        print(file + ' has already been parsed!')
        return False

    f = open(file_path, 'r', encoding='utf-8')
        # This programme will read text files made on Windows(cp949). Later, os confirmation part needed here
    text = f.read().lower()
    text = ''.join(re.findall(r'[a-zA-Z0-9 ]', text))


    conn = sqlite3.connect(dir_file + '_RosettaStone.sqlite')
    cur = conn.cursor()

    words = text.split()
    corpus = dict()

    for word in words:
        try:
            if corpus[word]: corpus[word] += 1
        except:
            corpus[word] = 1

    cur.execute('''
        CREATE TABLE IF NOT EXISTS corpus_analysis (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                                    word TEXT NOT NULL UNIQUE,
                                                    count INTEGER NOT NULL)''')

    for word in corpus:
        cur.execute('''INSERT INTO corpus_analysis (word, count) VALUES (?, ?)''', (word, corpus[word]))

    print('A document {0} words, {1} distinct words long has been parsed.'.format(len(words), len(corpus.keys())))

    f.close()
    conn.commit()
    cur.close()

dir_name = input('What is the name of the directory? ')
tmp_list = os.listdir(dir_name)
file_list = list()
for file in tmp_list:
    if not file.startswith('.'): file_list.append(os.path.join(dir_name, file))

for file in file_list:
    corpus(file)
