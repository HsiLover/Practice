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

api = InstagramAPI('id', 'password')

api.login()

while True:
    input = input('What is the name of the target user?')

    api.searchUsername(input)
    print('Target found...')

    target_user = api.LastJson
    target_user_id = target_user['user']['pk']
    api.getUserFollowers(target_user_id)
    print('Examining the target...')

    target_followers = []
    for user in api.LastJson['users']:
        target_followers.append(user['pk'])
    print('Extracting followers...')

    api.getSelfUsersFollowing()
    for user in api.LastJson['users']:
        if user in target_followers: target_followers.remove(user)
    print('Comparing your followings with the followers...')

    for follower in target_followers:
        api.follow(follower)
        print('Friend Request has been sent to {0}'.format(follower))
        time.sleep(36)


    print('Job done!')
