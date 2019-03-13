import time
from InstagramAPI import InstagramAPI
import sqlite3
from datetime import datetime
from pytz import timezone
import threading
from random import shuffle
'''
3rd party api has been used
download this repositary https://github.com/LevPasha/Instagram-API-python.git
'''

'''
From when till when do you want to copy followers?
Rest of the time, this script will unfollow your non-mutual followings.
'''
start_time = 11
end_time = 17

'''
Put in your IG id and password down below.
'''
agent = {'id':'', 'pw':''}

class COPIEDAPI(InstagramAPI):

    def is_my_friend(self, user_id, last_id = None):
        self.getUserFollowings(user_id)
        try:
            if self.username_id in (x['pk'] for x in self.LastJson['users']):
                return True
            else: return False
        except:
            return True

def time_now():
    est_timezone = timezone('EST')
    return datetime.now(est_timezone)

def condition():
    now = time_now()
    return now.hour <= start_time or now.hour > end_time
    #Condition in which this script unfollows the non-mutual-followings

sql = './IG_crowd_control.sqlite'
api = COPIEDAPI(agent['id'], agent['pw'])
while True:
    api.login()

    conn = sqlite3.connect(sql)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS instagram (user_id INTEGER PRIMARY KEY NOT NULL UNIQUE, \
                request_time INTEGER NOT NULL, is_friend INTEGER NOT NULL)')

    '''
    is_friend = 0 means none friend, is_friend = 1 means friend
    '''

    cur.execute('SELECT user_id FROM instagram WHERE is_friend = 1')
    previous_followers = [x[0] for x in cur.fetchall()]

    api.getSelfUsersFollowing()
    print('Sorting out my followings...')
    following = [user['pk'] for user in api.LastJson['users']]

    for user in following:
        cur.execute('INSERT OR IGNORE INTO instagram (user_id, request_time, is_friend) VALUES({}, 0, 0)'.format(user))

    conn.commit()
    cur.close()
    conn.close()
    print('Saving user data...')

    print('Checking if there has been some friends request received')
    api.getSelfUserFollowers()
    my_followers = [user['pk'] for user in api.LastJson['users']]

    previous_followers = set(previous_followers)
    my_followers = set(my_followers)
    my_followers = list(my_followers - previous_followers)

    for my_follower in my_followers:
        api.follow(my_follower)
        print('Mutual friend request has been sent to {}, cheers!'.format(my_follower))
        conn = sqlite3.connect(sql)
        cur = conn.cursor()
        cur.execute('INSERT OR IGNORE INTO instagram (user_id, request_time, is_friend) VALUES({}, {}, 1)'.format(my_follower, int(time.time())))
        cur.execute('UPDATE instagram SET is_friend = 1 WHERE user_id = {}'.format(my_follower))
        conn.commit()
        cur.close()
        conn.close()
        time.sleep(36)

    if not condition():
        #EST 09~21 copy followers
        if time_now().hour % 2 == 0:
            api.login()
        print('Starting copying followers...')
        conn = sqlite3.connect(sql)
        cur = conn.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS copy_follow (username TEXT[50] PRIMARY KEY NOT NULL UNIQUE)')
        cur.execute('SELECT username FROM copy_follow')
        target_inputs = [copy[0] for copy in cur.fetchall()]
        conn.commit()
        cur.close()
        conn.close()

        if not target_inputs:
            target_inputs.append('unboxtherapy')
# if there's no copy targets, you'll copy the youtuber, unboxtherapy. Why? Because this channel happened
# to be on when I was writing this piece of code. The channel's pretty good, actually.
        for target_input in target_inputs:
            if condition(): break
            api.searchUsername(target_input)
            print('Target found, target ID {}'.format(target_input))

            target_user_id = api.LastJson['user']['pk']
            api.getUserFollowers(target_user_id)
            print('Examining the target...')

            target_followers = [user['pk'] for user in api.LastJson['users']]
            print('Extracting followers...')

            api.getSelfUsersFollowing()
            for user in api.LastJson['users']:
                if user in target_followers: target_followers.remove(user)

            conn = sqlite3.connect(sql)
            cur = conn.cursor()
            cur.execute('SELECT user_id FROM instagram')
            existing = cur.fetchall()
            if not existing:
                existing = [x[0] for x in existing[0]]
                for minus_id in existing:
                    target_followers.remove(minus_id)
            cur.close()
            conn.close()

            print('Comparing your followings with the followers...')

            for follower in target_followers:
                if condition(): break
                conn = sqlite3.connect(sql)
                cur = conn.cursor()
                api.follow(follower)
                print('Friend Request has been sent to {0}'.format(follower))
                cur.execute('INSERT OR IGNORE INTO instagram (user_id, request_time, is_friend) VALUES ({}, {}, 0)'.format(follower, int(time.time())))
                conn.commit()
                cur.close()
                conn.close()
                time.sleep(36)
                if follower == target_followers[-1]:
                    conn = sqlite3.connect(sql)
                    cur = conn.cursor()
                    cur.execute('DELETE FROM copy_follow WHERE username = \'{}\''.format(target_input))
                    conn.commit()
                    cur.close()
                    conn.close()

    else:
        #EST 21~09 unfollow the unfriendly
        if time_now().hour % 2 == 0:
            api.login()
        print('Start unfollowing...')
        print('Loading my following list...')
#I'm giving 2 weeks of grace period, meaning you will keep non-mutual followers for two weeks at least.
        conn = sqlite3.connect(sql)
        cur = conn.cursor()
        recent_second = int(time.time()) - 1209600
        cur.execute('SELECT user_id FROM instagram WHERE request_time < {} AND is_friend = 0'.format(recent_second))
        my_followings_id = [x[0] for x in cur.fetchall()]
        conn.commit()
        cur.close()
        conn.close()
        print('Sorting my followings...')

        shuffle(my_followings_id)

        for following_id in my_followings_id:
            if not condition(): break
            try:
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
                    conn = sqlite3.connect(sql)
                    cur = conn.cursor()
                    cur.execute('UPDATE instagram SET is_friend = 1 WHERE user_id = \'{}\''.format(following_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    time.sleep(36)
                    continue
            except:
                continue
