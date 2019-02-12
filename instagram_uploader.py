import time
from datetime import datetime
import InstagramAPI as IG
import sqlite3
import threading
from pytz import timezone

Login_details = {'id':'ID', 'pw':'PW'}
print('Starting the script...')

while True:
    try:
        timezone = timezone('EST')
        break
    except:
        print('Timezone module is being crappy again...')
est_time = datetime.now(timezone)

while True:
    conn = sqlite3.connect('IG_auto_upload.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS instagram(post_time CHAR(50) PRIMARY KEY NOT NULL, photo CHAR(300) NOT NULL, caption CHAR(500) NOT NULL)')
    print('Looking at the queue database...')

    print('EST now is {}/{}/{}...'.format(est_time.day, est_time.month, est_time.hour))

    api = IG.InstagramAPI(Login_details['id'], Login_details['pw'])
    api.login()

    cur.execute('SELECT post_time, photo, caption FROM instagram ORDER BY post_time ASC')
    print('Loading the queue...')

    data = cur.fetchall()
    if len(data) == 0:
        print('There is no post to be scheduled...')
        time.sleep(7200)
        continue

    post_list = list()

    for entry in data:
        post_entry = dict()
        tmp = entry[0]
        tmp = tmp.split('/')

        post_entry['post_day'] = tmp[0]
        post_entry['post_month'] = tmp[1]
        post_entry['post_hour'] = tmp[2]
        post_entry['photo'] = entry[1]
        post_entry['caption'] = entry[2]
        post_list.append(post_entry)

    print('Parsing the queue...')

    print('Looking at the queue')

    for post in post_list:

        print('{}/{}/{} is being viewed...'.format(post['post_day'], post['post_month'], post['post_hour']))
        if (int(post['post_hour']) <= est_time.hour and int(post['post_day']) <= est_time.day and int(post['post_month']) <= est_time.month):
            post_time_reformat = '\'' + post['post_day'] + '/' + post['post_month'] + '/' + post['post_hour'] + '\''
            print('Posting...')
            api.uploadPhoto(post['photo'], post['caption'])
            time.sleep(10)
            print('{} uploaded...'.format([post['photo'], post['caption'][:25]]))
            sql_command = "DELETE FROM instagram WHERE post_time = {} AND photo = {}".format(post_time_reformat, '\'' + post['photo'] + '\'')
            cur.execute(sql_command)
            print('Deleting the uploaded post from the queue...')

    conn.commit()
    cur.close()
    conn.close()
    print('Hibernate for 20 minutes...')
    time.sleep(1200)
