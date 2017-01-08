import configparser
import feedparser
import pprint


YOUTUBE_RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id="


def get_feeds(config_name='feeds.conf'):
    """Takes in a configuration name (defaults to feeds.conf),
    and returns a dictionary of youtube ids found in that file."""

    config = configparser.ConfigParser()
    config.read(config_name)

    result = {}
    for section in config.sections():
        result[section] = {'channel_id': config[section]['channel_id']}

    return result


def get_latest_entry(feeds):
    """Takes in a dictionary of youtube channel ids created by get_feeds,
    returns a list of youtube urls from the latest entry"""
    results = []
    for feed in feeds:
        parsed_feed = feedparser.parse(
            "{}{}".format(YOUTUBE_RSS_URL,
                          feeds[feed]['channel_id']))
        if parsed_feed and len(parsed_feed.entries) > 0:
            results.append(parsed_feed.entries[0].link)

    return results


def main():
    feeds = get_feeds()
    videos = get_latest_entry(feeds)


if __name__ == "__main__":
    main()
