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
import sqlite3
import json


class SlackDb:
    """This class used for access the database. The database structure:

--------------------------------------------------------------------|
| TUser                                                             |
--------------------------------------------------------------------|
| id                | string   | unique       | user id             |
| name              | string   |              | user name           |
| color             | string   |              | user color          |
| json              | string   |              | raw json            |
--------------------------------------------------------------------|

--------------------------------------------------------------------|
| TChannel                                                          |
--------------------------------------------------------------------|
| id                | string   | unique       | channel id          |
| name              | string   |              | channel name        |
| archived          | string   |              | channel is archived |
| json              | string   |              | raw json            |
--------------------------------------------------------------------|

--------------------------------------------------------------------|
| TMessage                                                          |
--------------------------------------------------------------------|
| TChannelId        | string   | unique       | message type        |
| type              | string   |              | message type        |
| subtype           | string   |              | message subtype     |
| user              | string   |              | user id             |
| ts                | string   | unique       | message timestamp   |
| text              | string   |              | message text        |
| json              | string   |              | raw json            |
--------------------------------------------------------------------|
    """
    __conn = None

    def __init__(self, path_to_database):
        self.__conn = sqlite3.connect(path_to_database)
        self.__conn.text_factory = str
        self.__conn.commit()

    def create_tables(self):
        cursor = self.__conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TUser(
                id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                color TEXT NOT NULL,
                json TEXT NOT NULL);""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TChannel(
                id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                archived TEXT NOT NULL,
                json TEXT NOT NULL);""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TMessage(
                TChannelId TEXT NOT NULL,
                type TEXT NOT NULL,
                subtype TEXT NOT NULL,
                user TEXT NOT NULL,
                ts TEXT NOT NULL,
                text TEXT NOT NULL,
                json TEXT NOT NULL,
                UNIQUE(TChannelId, ts));""")
        self.__conn.commit()

    def commit(self):
        self.__conn.commit()

    def user_add_or_update(self, user, commit=False):
        user_id = user['id']
        user_name = user['name']
        user_color = user.get('color', '000000')

        cursor = self.__conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO TUser"
                       " (id, name, color, json)"
                       " VALUES(?, ?, ?, ?)",
                       (user_id, user_name, user_color, json.dumps(user),))
        if commit:
            self.__conn.commit()

    def channel_add_or_update(self, channel, commit=False):
        channel_id = channel['id']
        channel_name = channel['name']
        channel_archived = channel['is_archived']

        cursor = self.__conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO TChannel"
                       " (id, name, archived, json)"
                       " VALUES(?, ?, ?, ?)",
                       (channel_id, channel_name, channel_archived,
                        json.dumps(channel),))
        if commit:
            self.__conn.commit()

    def message_add(self, channel_id, message, commit=False):
        try:
            message_type = message['type']
            message_ts = message['ts']

            message_subtype = ""
            if 'subtype' in message:
                message_subtype = message['subtype']

            message_user = ""
            if 'user' in message:
                message_user = message['user']

            message_text = ""
            if 'text' in message:
                message_text = message['text']

            cursor = self.__conn.cursor()
            cursor.execute("INSERT INTO TMessage"
                           " (TChannelId, type, subtype, user, ts, text, json)"
                           " VALUES(?, ?, ?, ?, ?, ?, ?)",
                           (channel_id, message_type, message_subtype,
                            message_user, message_ts, message_text,
                            json.dumps(message),))
            if commit:
                self.__conn.commit()
        except sqlite3.IntegrityError:
            return False
        else:
            return True


if __name__ == "__main__":
    pass
