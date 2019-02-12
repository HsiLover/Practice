#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password
import time
import json
import platform
from InstagramAPI import InstagramAPI

''' 3rd party api has been used
    download this repositary https://github.com/LevPasha/Instagram-API-python.git
'''

class COPIEDAPI(InstagramAPI):

    def is_my_friend(self, user_id, last_id = None):
        super().getUserFollowings(user_id)
        if self.username_id in (x['pk'] for x in self.LastJson['users']):
            return True
        else: return False

if platform.system() == 'Windows':
    space_character = '\r\n'
else:
    space_character = '\n'

api = COPIEDAPI('ID', 'PW')

api.login()

api.getSelfUsersFollowing()
my_followings = api.LastJson['users']
print('Loading my following list...')

my_followings_id = list(map((lambda x:x['pk']), my_followings))
print('Sorting my followings...')

target_cursor = 0

while True:

    f = open('./instagram_auto_unfollow_.txt', 'r')
    last_id = f.read().split(space_character)[1]
    f.close()
    if not last_id == '':
        target_cursor = my_followings_id.index(int(last_id))

    for my_following_id in my_followings_id[target_cursor:]:
        f = open('./instagram_auto_unfollow_.txt', 'w')
        f.write(str(my_following_id) + space_character)
        f.close()
        if not api.is_my_friend(my_following_id):
            api.unfollow(my_following_id)
            print('Unfollowed {0}!'.format(my_following_id))
            time.sleep(36)
        else:
            print('{} is a good friend of yours!'.format(my_following_id))
            continue

    print('Job done! Going for another run!')
