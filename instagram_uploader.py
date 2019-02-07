import time
from datetime import datetime
import InstagramAPI as IG
import sqlite3
import threading
from pytz import timezone

Login_details = {'id':'cloudeight.io', 'pw':'hoit8cloud'}

#threading

while True:
    conn = sqlite3.connect('IG_auto_upload.sqlite')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS instagram(post_time CHAR(50) PRIMARY KEY NOT NULL, photo CHAR(300) NOT NULL, caption CHAR(500) NOT NULL)')

    api = IG.InstagramAPI(Login_details['id'], Login_details['pw'])
    api.login()

    cur.execute('SELECT post_time, photo, caption FROM instagram ORDER BY post_time ASC')

    data = cur.fetchall()
    post_entry = dict()
    post_list = list()

    for (post_time, photo, caption) in data:
        day, month, hour = map(int, post_time.split('/'))
        post_entry['post_day'] = day
        post_entry['post_month'] = month
        post_entry['post_hour'] = hour
        post_entry['photo'] = photo
        post_entry['caption'] = caption
        post_list.append(post_entry)

    timezone = timezone('EST')
    est_time = datetime.now(timezone)

    for post in post_list:
        if post['post_hour'] == est_time.hour and post['post_day'] == est_time.day and int(int(post['month']) == est_time.month:
            post_time_reformat = str(post['post_day']) + '/' + str(post['post_month']) + '/' + str(post['post_hour'])
            api.uploadPhoto(post['photo'], post['caption'])
            cur.execute('DELETE FROM instagram WHERE post_time = {0} AND photo = {1} AND caption = {2}'.format(post_time_reformat, post['photo'], post['caption']))
        else: break

    conn.commit()
    cur.close()
    conn.close()

    time.sleep(1800)
