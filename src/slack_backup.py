#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2016, Durachenko Aleksey V. <durachenko.aleksey@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import urllib.request
import json


def get_json(request):
    response = urllib.request.urlopen(request)
    str_response = response.read().decode('utf-8')
    return json.loads(str_response)


def backup_users(db, access_token):
    request = "https://slack.com/api/users.list"    \
              "?token=%s"                           \
              "&pretty=1"                           \
              % (access_token,)
    obj = get_json(request)

    if 'ok' not in obj:
        print("Error: incorrect response")
        exit(-1)

    if obj['ok'] is False:
        print("Error: ", obj['error'])
        exit(-1)

    if 'members' not in obj:
        print("Error: incorrect response")
        exit(-1)

    ids = []
    names = []
    for user in obj['members']:
        ids.append(user['id'])
        names.append(user['name'])
        db.user_add_or_update(user)

    return ids, names


def backup_channels(db, access_token):
    request = "https://slack.com/api/channels.list" \
              "?token=%s"                           \
              "&exclude_archived=0"                 \
              "&pretty=1"                           \
              % (access_token,)
    obj = get_json(request)

    if 'ok' not in obj:
        print("Error: incorrect response")
        exit(-1)

    if obj['ok'] is False:
        print("Error: ", obj['error'])
        exit(-1)

    if 'channels' not in obj:
        print("Error: incorrect response")
        exit(-1)

    ids = []
    names = []
    for channel in obj['channels']:
        ids.append(channel['id'])
        names.append(channel['name'])
        db.channel_add_or_update(channel)

    return ids, names


def backup_channel_history(db, access_token, channel_id, verbose=False):
    latest = ""
    while True:
        request = "https://slack.com/api/channels.history"  \
                  "?token=%s"                               \
                  "&channel=%s"                             \
                  "&inclusive=0"                            \
                  "&count=1000"                             \
                  "&pretty=1"                               \
                  "&latest=%s"                              \
                  % (access_token, channel_id, latest, )
        obj = get_json(request)

        if 'ok' not in obj:
            print("Error: incorrect response")
            exit(-1)

        if obj['ok'] is False:
            print("Error: ", obj['error'])
            exit(-1)

        if 'messages' not in obj:
            print("Error: incorrect response")
            exit(-1)

        for message in obj['messages']:
            latest = message['ts']
            if db.message_add(channel_id, message) is False:
                return None
            if verbose:
                print(message['ts'], message['text'])

        if obj['has_more'] is False:
            return None
