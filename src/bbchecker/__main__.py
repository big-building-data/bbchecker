import argparse

from pytgbot.exceptions import TgApiServerException

from bbchecker import *

# suppress InsecureRequestWarning: Unverified HTTPS request is being made [...] when verify=False
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True, help='path the the config.ini file')
    args = parser.parse_args()

    bot = None
    try:
        # create objects
        config = Config(args.config)
        bot = BBBot(config)
        checker = Checker(config)

        if bot.running:
            messages = []
            # test API
            try:
                checker.is_api_reachable()
                checker.is_ingestion_working()
            except CheckerError as e:
                messages.append(e.telegram())

            # test flink
            try:
                checker.is_flink_running()
            except CheckerError as e:
                messages.append(e.telegram())

            if len(messages):
                bot.send_message('\n\n'.join(messages))
        else:
            print('bot not running')

    except TgApiServerException as e:
        print(f'Telegram error')
        if hasattr(e, 'request'):
            print(f'While fetching {e.request.url}.\nIs it the proper API key ? And chat id ?')
        print('Details:', e)
        exit(1)

    except KeyboardInterrupt:
        pass

    except BaseException as e:
        if bot is not None:
            bot.send_message('Unknown error\n' + pre(str(e)))
        print('Error:', e)
        exit(1)


if __name__ == '__main__':
    main()
