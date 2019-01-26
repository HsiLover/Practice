import oauth2 as oauth
import urllib
import time
import json

def oauth_request(argv, cons_k, cons_s, tok_k, tok_s, http_method='POST', post_body = None, http_headers = None):

    consumer = oauth.Consumer(key = consumer_key, secret = consumer_secret)
    access_token = oauth.Token(key = token_key, secret = token_secret)
    client = oauth.Client(consumer, access_token)

    friend_request_api = 'https://api.twitter.com/1.1/friendships/create.json?user_id=' + str(argv)

    results = client.request(
    friend_request_api,
    method = http_method,
    body = urllib.parse.urlencode({'status' : post_body}),
    headers = http_headers,)

    return results

# put in your keys and tokens

consumer_key = ''
consumer_secret = ''
token_key = ''
token_secret = ''

#making an oauth key
consumer = oauth.Consumer(key = consumer_key, secret = consumer_secret)
access_token = oauth.Token(key = token_key, secret = token_secret)
client = oauth.Client(consumer, access_token)

#api endpoints
friends_api = 'https://api.twitter.com/1.1/friends/ids.json?'
followers_api = 'https://api.twitter.com/1.1/followers/ids.json?screen_name='

my_friends_list = list()

friend_headers, friend_data = client.request(friends_api)
friend_data = json.loads(friend_data.decode())

while True:
    #friend list retrieving

    print('Friends list retrieving ' + friend_headers['x-rate-limit-remaining'] + ' times left!')

    for id in friend_data['ids']:
        my_friends_list.append(id)

    if friend_data['next_cursor'] != 0:
        friend_headers, friend_data = client.request(friends_api + 'cursor=' + friend_data['next_cursor_str'])
        friend_data = json.loads(friend_data.decode())
        continue

    while True:
        #follower list retrieving

        name = input('What is the ID of the target user?')

        follower_headers, follower_data = client.request(followers_api + name)
        follower_data = json.loads(follower_data.decode())

        while True:
            #friend request sending

            print('Follower list retrieving ' + follower_headers['x-rate-limit-remaining'] + ' times left!')

            for id in follower_data['ids']:
                if my_friends_list.count(id) == 0:
                    oauth_request(id, consumer_key, consumer_secret, token_key, token_secret)
                    print('Sent friend request to ' + str(id))
                    my_friends_list.append(id)
                    time.sleep(240)

            if follower_data['next_cursor'] == 0:
                print('Friend requests have been sent to all the followers of the target user.')
                break
            else:
                follower_headers, follower_data = client.request(followers_api + name + '?cursor=' + follower_headers['next_cursor_str'])
                follower_data = json.loads(follower_data.decode())


'''
How to run this script:
1. Enter the target account's name.
2. This script will automatically send a friend request to all the followers of the target, who are not your friendsself.
'''
