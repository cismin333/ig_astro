#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ___        InstaBot V 1.2.0 by Trevor                 ___
# ___        Mengotomatiskan aktivitas Instagram Anda   ___

# ___        Copyright 2018 by Trevor            ___

# ___Perangkat lunak ini dilisensikan di bawah Apache 2___
# ___lisensi. Anda mungkin tidak menggunakan file ini  ___
# ___ kecuali sesuai dengan licensi anda               ___

from lxml import etree
from json import loads as toJSON
from random import random, choice
from time import sleep
import itertools

# === INSTAGRAM FUNCTIONS ===

def refill(user_id, data, bucket, friends, tags_to_avoid, enabled, mode):


    if mode == 'feed' and data:
        for i in data:
            bucket['codes'][i['media_id']] = i['url_code']

        if enabled['like_feed']:
            bucket['feed']['like'].extend([[i['media_id'], i['username']] for i in data 
                                            if any(n.lower() == i['username'].lower() for n in friends) 
                                            if not user_id == i['user_id']
                                            if not any(n == i['media_id'] for n in bucket['feed']['media_ids'])
                                            if not any(n[0] == i['media_id'] for n in bucket['feed']['done'])
                                            if not any(n in i['caption'] for n in tags_to_avoid)])
            bucket['feed']['media_ids'].extend([i['media_id'] for i in data])

    if mode == 'explore' and data['posts']:
        for i in data['posts']:
            bucket['codes'][i['media_id']] = i['url_code']
            bucket['user_ids'][i['user_id']] = i['username']

        tmp = [['like', 'media_id'], ['follow', 'user_id'], ['comment', 'media_id']]
        params = [param for param in tmp if enabled[param[0]]]

        for param in params:
            if param:
                bucket[mode][param[0]].update([i[param[1]] for i in data['posts'] if not user_id == i['user_id']
                                            if not any(i[param[1]] in n for n in bucket[mode]['done'][param[0]]) 
                                            if not any(n in i['caption'] for n in tags_to_avoid)])
    elif mode == 'explore' and not data['posts']:
        raise Exception('No posts found')
    return bucket

def media_by_tag(browser, tag_url, media_url, tag, media_max_likes, media_min_likes):
    result = {'posts': False, 'tag': tag}
    try:
        explore_site = browser.get(tag_url %(tag))
        tree = etree.HTML(explore_site.text)
        data = return_sharedData(tree)
        if data:
            nodes = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
            result['posts'] = [{'user_id': n['node']['owner']['id'],
                                'username': return_username(browser, media_url, n['node']['shortcode']),
                                'likes': n['node']['edge_liked_by']['count'],
                                'caption': n['node']['edge_media_to_caption']['edges'][0]['node']['text'],
                                'media_id': n['node']['id'],
                                'url_code': n['node']['shortcode']}
                               for n in nodes if media_min_likes <= n['node']['edge_liked_by']['count'] <= media_max_likes if not n['node']['comments_disabled']]
    except Exception as e:
        print '\nError in obtaining media by tag: %s' %(e)
    return result

def return_sharedData(tree):


    identifier = 'window._sharedData = '
    for a in tree.findall('.//script'):
        try:
            if a.text.startswith(identifier):
                try:
                    return toJSON(a.text.replace(identifier, '')[:-1])
                except Exception as e:
                    print '\nError returning sharedData JSON: %s' %(e)
        except Exception as e:
            continue
    return False

def return_username(browser, media_url, code):


    try:
        media_page = browser.get(media_url %(code))
        tree = etree.HTML(media_page.text)
        data = return_sharedData(tree)
        return data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username']
    except Exception as e:
        print '\nError obtaining username: %s' %(e)
    return False

def news_feed_media(browser, url, user_id):

    
    posts = False
    nodes = False
    try:
        news_feed = browser.get(url)
        tree = etree.HTML(news_feed.text)
        data = return_sharedData(tree)
        if data:
            nodes = data['entry_data']['FeedPage'][0]['graphql']['user']['edge_web_feed_timeline']['edges']
        if nodes:
            posts = []
            for n in nodes:
                try:
                    if not n['node']['owner']['id'] == user_id and not n['node']['viewer_has_liked']:
                        post = {'user_id': n['node']['owner']['id'],
                                'username': n['node']['owner']['username'],
                                'likes': n['node']['edge_media_preview_like']['count'], 
                                'caption': n['node']['edge_media_to_caption']['edges'][0]['node']['text'], 
                                'media_id': n['node']['id'],
                                'url_code': n['node']['shortcode']}
                        posts.append(post)
                except:
                    continue
    except Exception as e:
        print '\nError getting new feed data: %s.' %(e)
    return posts

def check_user(browser, url, user):
    # checks the users profile to assess if it's fake

    result = {
    'fake': False, 'active': False, 'follower': False, 'data': {
        'username': '', 'user_id': '', 'media': '', 'follows': 0, 'followers': 0
    }}
    try:
        site = browser.get(url %(user))
        tree = etree.HTML(site.text)
        data = return_sharedData(tree)
        user_data = data['entry_data']['ProfilePage'][0]['user']
        if user_data:
            if user_data['follows_viewer'] or user_data['has_requested_viewer']:
                result['follower'] = True
            if user_data['followed_by']['count'] > 0:
                try:
                    if user_data['follows']['count'] / user_data['followed_by']['count'] > 2 and user_data['followed_by'] < 10:
                        result['fake'] = True
                except ZeroDivisionError:
                    result['fake'] = True
                try:
                    if user_data['follows']['count'] / user_data['media']['count'] < 10 and user_data['followed_by']['count'] / user_data['media']['count'] < 10:
                        result['active'] = True
                except ZeroDivisionError:
                    pass
            else:
                result['fake'] = True
            result['data'] = {
                'username': user_data['username'],
                'user_id': user_data['id'],
                'media': user_data['media']['count'],
                'follows': user_data['follows']['count'],
                'followers': user_data['followed_by']['count']
            }

    except Exception as e:
        print '\nError checking user: %s.' %(e)

    sleep(5*random())
    return result
    
def generate_comment(comments_list):

    batch = list(itertools.product(*comments_list))
    return ' '.join(choice(batch))

def post_data(browser, url, identifier, comment):
    # sends post request

    result = {'response': False, 'identifier': identifier}
    try:
        if comment:
            response = browser.post(url %(identifier), data= {'comment_text': comment})
        else:
            response = browser.post(url %(identifier))
        result['response'] = response
    except:
        pass
    return result   
