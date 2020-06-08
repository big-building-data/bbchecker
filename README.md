# BBDATA checker

* [Goals](#goals)
* [Install and run](#install-and-run)
* [Telegram interface](#telegram-interface)
* [Configuration](#configuration)
* [dependencies](#dependencies)

## Goals

This little python script is intended to run periodically via a cron job. It will check that:

- the flink jobs are running: quarters and hours,
- the api is reachable, and the submit endpoint up,
- the ingestion process is working.

In case one of the above test fails, a notification will be send to a telegram channel.
The script is devoid of any output (except unknown exceptions). 
Only the exit code and the telegram notification informs you of a failure.

## Install and run

Given a `config.ini` file (see [below](#Configuration)), this is a straight-forward python app:

__Install__

```bash
# clone
git clone git@github.com:big-building-data/bbchecker.git
cd bbchecker

# create and activate virtualenv
python3 -m venv venv
source venv/bin/activate

# install (use 'develop' instead of 'install' for development)
python setup.py install
```

__Run__
```bash
# from bash directly:
bbchecker -c config.ini

# using module
python -m bbchecker -c config.ini
```

__Setup cron__

Use `crontab -e` to launch a cron editor and paste (will run every 15 minutes):
```text 
*/15 * * * * /path/to/venv/bin/python -m bbchecker -c /path/to/config.ini
```

## Telegram interface

The bot api key and the chat id of the telegram channel are configured through the .ini file.
You can pause/resume the check process whenever you want by sending one of `stop`, `pause`, `start`, `resume` keyword in the chat.

## Configuration

An example configuration file is provided (see `config-sample.ini`).

__bot__ section:

- `offset`: put 0 the first time, will be updated by the script itself
- `running`: current status of the script, i.e. if it should run the tests or not (updated through telegram)
- `key`: the bot api key, as returned by the @botfather
- `chat_id`: you can find the chat id by 1) adding the bot to the chat, 2) send a message to the chat,
  3) consult the url `https://api.telegram.org/bot<bot-api-key>/getUpdates`, the bot token being `XXX:YYY`...

__bbdata__ section:

- `url`: the base url of the bbdata apis, for example https://bbdata.daplab.ch
- `bbuser` and `bbtoken`: the authentication used to connect to the output api (see `bbdata/output-api`)

__flink__ section:

- `script`: the path to the `run-hadoop.sh` shell script (see [flink-aggregations](https://github.com/big-building-data/flink-aggregations)).
If not present, the flink status test is skipped.

__input__ section:

- `object_id`: the objectId for posting new measures (must be an object with float or int value)
- `token`: the token used to send new measures (should be valid for the specified objectId)

## dependencies

- [requests](http://docs.python-requests.org/en/master/)
- [pytgbot](https://github.com/luckydonald/pytgbot)