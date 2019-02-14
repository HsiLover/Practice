import time
from InstagramAPI import InstagramAPI
import sqlite3
from datetime import datetime
from pytz import timezone
import threading

'''
3rd party api has been used
download this repositary https://github.com/LevPasha/Instagram-API-python.git
'''

'''
From when till when do you want to copy followers?
Rest of the time, this script will unfollow your non-mutual followings.
'''
start_time = 9
end_time = 21

'''
Put in your IG id and password down below.
'''
agent = {'id':'cloudeight.io', 'pw':'hoit8cloud'}

class COPIEDAPI(InstagramAPI):

    def is_my_friend(self, user_id, last_id = None):
        self.getUserFollowings(user_id)
        if self.username_id in (x['pk'] for x in self.LastJson['users']):
            return True
        else: return False

class Flag():
    signal = True
    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            if now.hour >= start_time and now.hour < end_time:
                self.signal = False
            else: self.signal = True
            time.sleep(5)


timezone = timezone('EST')
now = datetime.now(timezone)
sql = './IG_crowd_control.sqlite3'
flag = Flag()
api = COPIEDAPI(agent['id'], agent['pw'])
api.login()

conn = sqlite3.connect(sql)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS instagram (user_id INTEGER PRIMARY KEY NOT NULL UNIQUE,
            request_time INTEGER NOT NULL)')

api.getSelfUsersFollowing()
following = [user['pk'] for user in api.LastJson['users']]

for user in following:
    cur.execute('''
    INSERT OR IGNORE INTO instagram (user_id, request_time) VALUES({}, 0)'''.format(user))

cur.execute('SELECT * FROM instagram')
raw_data = cur.fetchall()

cur.close()
conn.close()

database = list()
entry = dict()

for user in raw_data:
    entry['id'] = user[0]
    entry['time'] = user[1]
    database.append(entry)

while True:

    if not flag.signal:
        #EST 09~21 copy followers

        conn = sqlite3.connect(sql)
        cur = conn.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS copy_follow (username CHAR[50] PRIMARY KEY NOT NULL UNIQUE)')
        cur.execute('SELECT * FROM copy_follow')
        target_inputs = cur.fetchall()
        cur.close()
        conn.close()

        for target_input in target_inputs:
            api.searchUsername(target_input)
            print('Target found...')

            target_user_id = api.LastJson['user']['pk']
            api.getUserFollowers(target_user_id)
            print('Examining the target...')


            target_followers = [user['pk'] for user in api.LastJson['users']]
            print('Extracting followers...')

            api.getSelfUsersFollowing()
            for user in api.LastJson['users']:
                if user in target_followers: target_followers.remove(user)
            print('Comparing your followings with the followers...')

            for follower in target_followers:
                if flag.signal: break
                conn = sqlite3.connect(sql)
                cur = conn.cursor()
                api.follow(follower)
                print('Friend Request has been sent to {0}'.format(follower))
                cur.execute('INSERT INTO instagram (user_id, request_time) VALUES ({}, {})'.format(follower, now))
                cur.close()
                conn.close()
                time.sleep(36)

            if flag.signal: break

    else:
        #EST 21~09 unfollow the unfriendly

        api.getSelfUsersFollowing()
        my_followings = api.LastJson['users']
        print('Loading my following list...')

        conn = sqlite3.connect(sql)
        cur = conn.cursor()
        cur.execute('SELECT user_id FROM instagram WHERE request_time < {}'.format(int(time.time()) - 172800))
        my_followings_id = cur.fetchall()
        cur.close()
        conn.close()
        print('Sorting my followings...')

        for my_following_id in my_followings_id:
            if not flag.signal: break
            if not api.is_my_friend(my_following_id):
                api.unfollow(my_following_id)
                print('Unfollowed {0}!'.format(my_following_id))
                conn.connect(sql)
                cur = conn.cursor()
                cur.execute('DELETE FROM instagram WHERE user_id = {}'.format(my_following_id))
                cur.close()
                conn.close()
                time.sleep(36)
            else:
                print('{} is a good friend of yours!'.format(my_following_id))
                continue
