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
import argparse
from slack_db import SlackDb
from slack_backup import *


def version():
    return 'v0.1.1'


def description():
    return 'This utility saves the message history from the '           \
           'slack.com into the database SQLite. The first time you '    \
           'are downloading the whole message history. On the next '    \
           'start only new messages are added into the database.'


def create_parser():
    parser = argparse.ArgumentParser(description=description())
    parser.add_argument('--version', action='version', version="%(prog)s " + version())
    parser.add_argument('--verbose', action='store_true', help='show debug information')
    parser.add_argument('--access-token', action='store', help='slack access token')
    parser.add_argument('--output-database', action='store', help='sqlite database file')
    return parser.parse_args()


def main():
    parser = create_parser()
    access_token = parser.access_token
    output_database = parser.output_database
    verbose = parser.verbose

    print("=== Summary ===")
    print("Access token   :", access_token)
    print("Output database:", output_database)
    print("Verbose enabled:", verbose)

    print("=== Begins the backup ===")
    print("--> create database...")
    db = SlackDb(output_database)
    db.create_tables()

    print("--> backup user list...")
    backup_users(db, access_token)
    print("Done!")

    print("--> backup channel list...")
    channel_ids, channel_names = backup_channels(db, access_token)
    print("Done!")

    print("--> backup channel history...")
    for i in range(0, len(channel_ids)):
        print("----> channel:", channel_names[i], "(%s)" % (channel_ids[i],))
        backup_channel_history(db, access_token, channel_ids[i], verbose)
    print("Done!")

    print("--| finalize...")
    db.commit()
    print("Done!")


if __name__ == '__main__':
    main()
