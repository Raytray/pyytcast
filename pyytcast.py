import configparser
import feedparser
import os
import youtube_dl

from feedgen.feed import FeedGenerator

config = configparser.ConfigParser()
config.read('config.conf')

MP3_FOLDER = config.get('paths', 'mp3_folder')
URL = config.get('paths', 'url')
DEPLOY_PATH = config.get('paths', 'deploy_path')


def get_channel_ids():
    """Takes in a configuration name (defaults to feeds.conf),
    and returns a list of youtube ids found in that file."""
    result = config.get('youtube', 'channel_ids')
    result = [channel_id.strip() for channel_id in result.split(',')]

    return result


def generate_feed(channel_id):
    """Given a channel id, obtain the youtube rss feed.
    Download any new entries, convert to audio.
    Attach and publish a feed for it."""
    print("Generating feed for {}".format(channel_id))
    parsed_feed = feedparser.parse('{}{}'.format(
        'https://www.youtube.com/feeds/videos.xml?channel_id=', channel_id))

    if parsed_feed.status != 200:
        continue;

    generated_feed = setup_feed(channel_id, parsed_feed.feed.get('title'))

    files_to_keep = []
    for entry in parsed_feed.entries[:5]:
        download_new_entries(entry.link)

        feed_entry = generated_feed.add_entry()
        feed_entry.id(entry.yt_videoid)
        feed_entry.title(entry.title)
        feed_entry.description(entry.summary)

        feed_entry.enclosure('{}{}/{}.mp3'.format(
            URL, MP3_FOLDER, entry.yt_videoid), 0, 'audio/mpeg')
        generated_feed.add_entry(feed_entry)

        files_to_keep.append('{}.mp3'.format(entry.yt_videoid))

    feed_name = '{}.xml'.format(channel_id)
    generated_feed.rss_file('{}/{}'.format(DEPLOY_PATH, feed_name))
    files_to_keep.append(feed_name)

    return files_to_keep


def setup_feed(channel_id, title):
    """Create the feed with initial information and return it"""
    generated_feed = FeedGenerator()
    generated_feed.title(title)
    generated_feed.load_extension('podcast')
    generated_feed.link(
        href='{}{}.xml'.format(URL, channel_id), rel='self')
    generated_feed.link(
        href='https://raytray.io/', rel='alternate')
    generated_feed.description(title)
    generated_feed.rss_str(pretty=True)

    return generated_feed


def download_new_entries(link):
    """Download first 5 entries if not yet downloaded."""
    youtube_dl_options = {'format': 'bestaudio',
                          'postprocessors': [{
                              'key': 'FFmpegExtractAudio',
                              'preferredcodec': 'mp3',
                              'preferredquality': '192'
                          }],
                          'download_archive': 'downloaded-videos.log',
                          'outtmpl': '{}/{}/%(id)s.%(ext)s'.format(
                              DEPLOY_PATH, MP3_FOLDER)}
    with youtube_dl.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download([link])


def cleanup_old_files(files_to_keep):
    """Delete files matching mp3 in the MP3_FOLDER that are not found
    in files_to_keep.
    Delete files matching .xml in DEPLOY_PATH not found in files_to_keep"""
    mp3s = [mp3 for mp3 in os.listdir('{}/{}'.format(DEPLOY_PATH, MP3_FOLDER))
            if mp3.endswith(".mp3")]

    feeds = [feed for feed in os.listdir(DEPLOY_PATH) if feed.endswith('.xml')]

    to_delete = ["{}/{}".format(MP3_FOLDER, old_file) for old_file in mp3s
                 if old_file not in files_to_keep]
    to_delete.extend([old_file for old_file in feeds
                      if old_file not in files_to_keep])

    for file_name in to_delete:
        print("Removing {}".format(file_name))
        os.remove("{}/{}".format(DEPLOY_PATH, file_name))


def main():
    channel_ids = get_channel_ids()
    files_to_keep = []
    for channel_id in channel_ids:
        files_to_keep.extend(generate_feed(channel_id))

    cleanup_old_files(files_to_keep)


if __name__ == '__main__':
    main()
