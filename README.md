# slack2sqlite

Backing up the slack chat to the SQLite database.

## Back up the following objects:
- user list
- channel list
- message history

## Changelog
### v0.1.0
- initial version

## Usage:

```bash
== slack_backup.py - v0.1.0  ==
Usage:
    slack_backup.py --access-token=<access_token> --output-database=<database.sqlite> --debug
```
- access_token - can be found here: https://api.slack.com/web
- database.sqlite - output SQLite database filename
