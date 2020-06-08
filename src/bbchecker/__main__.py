import argparse

from bbchecker import *


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
            # test API
            try:
                checker.is_api_reachable()
                checker.is_ingestion_working()
            except CheckerError as e:
                bot.send_message(e.telegram())

            # test flink
            try:
                checker.is_flink_running()
            except CheckerError as e:
                bot.send_message(e.telegram())
        else:
            print('bot not running')

    except Exception as e:
        if bot is not None:
            bot.send_message(pre(str(e)))
        print(e)
        exit(1)


if __name__ == '__main__':
    main()
