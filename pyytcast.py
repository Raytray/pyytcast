import configparser
import feedparser
import pprint


def get_feeds(config_name='feeds.conf'):
    config = configparser.ConfigParser()
    config.read(config_name)

    result = {}
    for section in config.sections():
        result[section] = {'channel_id': config[section]['channel_id']}

    return result


def get_latest_entry(feeds):
    for feed in feeds:
        pass


def main():
    feeds = get_feeds()


if __name__ == "__main__":
    main()
