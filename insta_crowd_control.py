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
agent = {'id':'ID', 'pw':'PW'}

class COPIEDAPI(InstagramAPI):

    def is_my_friend(self, user_id, last_id = None):
        self.getUserFollowings(user_id)
        try:
            if self.username_id in (x['pk'] for x in self.LastJson['users']):
                return True
            else: return False
        except:
            return True


timezone = timezone('EST')
now = datetime.now(timezone)
sql = './IG_crowd_control.sqlite'
#flag = Flag()
api = COPIEDAPI(agent['id'], agent['pw'])
api.login()
condition = now.hour<=9 or now.hour>21

conn = sqlite3.connect(sql)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS instagram (user_id INTEGER PRIMARY KEY NOT NULL UNIQUE, \
            request_time INTEGER NOT NULL)')

api.getSelfUsersFollowing()
print('Sorting out my followings...')
following = [user['pk'] for user in api.LastJson['users']]

for user in following:
    cur.execute('INSERT OR IGNORE INTO instagram (user_id, request_time) VALUES({}, 0)'.format(user))

conn.commit()
cur.close()
conn.close()
print('Saving user data...')



while True:

    if not condition:
        #EST 09~21 copy followers
        if now.hour % 2 == 0:
            api.login()
        print('Starting copying followers...')
        conn = sqlite3.connect(sql)
        cur = conn.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS copy_follow (username CHAR[50] PRIMARY KEY NOT NULL UNIQUE)')
        cur.execute('SELECT username FROM copy_follow')
        target_inputs = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        for target_input in target_inputs:
            api.searchUsername(target_input)
            print('Target found, target primary key {}'.format(target_input))

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
                if condition: break
                conn = sqlite3.connect(sql)
                cur = conn.cursor()
                api.follow(follower)
                print('Friend Request has been sent to {0}'.format(follower))
                cur.execute('INSERT INTO instagram (user_id, request_time) VALUES ({}, {})'.format(follower, now))
                conn.commit()
                cur.close()
                conn.close()
                time.sleep(36)

            if condition: break

    else:
        #EST 21~09 unfollow the unfriendly
        if now.hour % 2 == 0:
            api.login()
        print('Start unfollowing...')
        api.getSelfUsersFollowing()
        my_followings = api.LastJson['users']
        print('Loading my following list...')
        my_followings_id = list(map((lambda x:x['pk']), my_followings))

        conn = sqlite3.connect(sql)
        cur = conn.cursor()
        recent_second = int(time.time()) - 172800
        cur.execute('SELECT user_id FROM instagram WHERE request_time < {}'.format(recent_second))
        my_old_followings_id = cur.fetchall()
        new_comers = set(my_followings_id) - set(my_old_followings_id)
        for new_comer in list(new_comers):
            cur.execute('INSERT OR IGNORE INTO instagram (user_id, request_time) VALUES ({}, {})'.format(new_comer, int(time.time())))
        conn.commit()
        cur.close()
        conn.close()
        print('Sorting my followings...')

        my_followings_id = my_followings_id + my_old_followings_id

        for following_id in my_followings_id:
            if not condition: break
            if not api.is_my_friend(following_id):
                api.unfollow(following_id)
                print('Unfollowed {0}!'.format(following_id))
                conn = sqlite3.connect(sql)
                cur = conn.cursor()
                cur.execute('DELETE FROM instagram WHERE user_id = \'{}\''.format(following_id))
                conn.commit()
                cur.close()
                conn.close()
                time.sleep(36)
            else:
                print('{} is a good friend of yours!'.format(following_id))
                time.sleep(36)
                continue
