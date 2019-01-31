#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password
import time
import json
from InstagramAPI import InstagramAPI

''' 3rd party api has been used
    download this repositary https://github.com/LevPasha/Instagram-API-python.git
'''

class COPIEDAPI(InstagramAPI):

    def is_my_friend(self, user_id):
        super().getUserFollowings(user_id)
        if self.username_id in (x['pk'] for x in self.LastJson['users']):
            return True
        else: return False

api = COPIEDAPI('ID', 'PASSWORD')

api.login()

while True:

    api.getSelfUsersFollowing()
    my_followings = api.LastJson['users']
    print('Loading my following list...')

    my_followings_id = map((lambda x:x['pk']), my_followings)
    print('Sorting my followings...')

    for my_following_id in my_followings_id:
        if not api.is_my_friend(my_following_id):
            api.unfollow(my_following_id)
            print('Unfollowed {0}!'.format(my_following_id))
            time.sleep(36)
        else: continue

    print('Job done!')
