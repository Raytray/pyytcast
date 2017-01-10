import configparser
import feedparser
import youtube_dl

from feedgen.feed import FeedGenerator


def get_channel_ids(config_name='config.conf'):
    """Takes in a configuration name (defaults to feeds.conf),
    and returns a list of youtube ids found in that file."""
    config = configparser.ConfigParser()
    config.read(config_name)

    result = config.get('youtube', 'channel_ids')
    result = [channel_id.strip() for channel_id in result.split(",")]

    return result


def generate_feed(channel_id):
    """Given a channel id, obtain the youtube rss feed.
    Download any new entries, convert to audio.
    Attach and publish a feed for it.

    Do any clean up as necessary."""
    parsed_feed = feedparser.parse("{}{}".format(
        "https://www.youtube.com/feeds/videos.xml?channel_id=", channel_id))

    generated_feed = FeedGenerator()
    generated_feed.title(parsed_feed.feed.title)
    generated_feed.load_extension('podcast')
    generated_feed.link(
        href='https://files.raytray.io/{}.xml'.format(channel_id), rel='self')
    generated_feed.link(
        href='https://raytray.io/', rel='alternate')
    generated_feed.description(parsed_feed.feed.title)

    for entry in parsed_feed.entries[:5]:
        download_new_entries(entry.link)
        feed_entry = generated_feed.add_entry()
        feed_entry.id(entry.yt_videoid)
        feed_entry.title(entry.title)
        feed_entry.description(entry.summary)
        feed_entry.enclosure('downloads/{}.mp3'.format(entry.yt_videoid),
                             0, 'audio/mpeg')

        generated_feed.add_entry(feed_entry)

    generated_feed.rss_str(pretty=True)
    generated_feed.rss_file('{}.xml'.format(channel_id))

    # TODO: Clean up old files


def download_new_entries(link):
    """Download first 5 entries if not yet downloaded."""
    youtube_dl_options = {'format': 'bestaudio',
                          'postprocessors': [{
                              'key': 'FFmpegExtractAudio',
                              'preferredcodec': 'mp3',
                              'preferredquality': '192'
                          }],
                          'download_archive': 'downloaded-videos.log',
                          'outtmpl': './downloads/%(id)s.%(ext)s'}
    with youtube_dl.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download([link])


def main():
    channel_ids = get_channel_ids()
    for channel_id in channel_ids:
        generate_feed(channel_id)


if __name__ == "__main__":
    main()
