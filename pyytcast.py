import configparser
import feedparser
import os
import youtube_dl

from feedgen.feed import FeedGenerator

config = configparser.ConfigParser()
config.read('config.conf')


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
    parsed_feed = feedparser.parse('{}{}'.format(
        'https://www.youtube.com/feeds/videos.xml?channel_id=', channel_id))

    url = config.get('paths', 'url')
    generated_feed = setup_feed(channel_id, parsed_feed.feed.title, url)

    files_to_keep = []
    mp3_folder = config.get('paths', 'mp3_folder')
    for entry in parsed_feed.entries[:5]:
        download_new_entries(entry.link)

        feed_entry = generated_feed.add_entry()
        feed_entry.id(entry.yt_videoid)
        feed_entry.title(entry.title)
        feed_entry.description(entry.summary)

        feed_entry.enclosure('{}{}/{}.mp3'.format(
            url, mp3_folder, entry.yt_videoid), 0, 'audio/mpeg')
        generated_feed.add_entry(feed_entry)

        files_to_keep.append('{}.mp3'.format(entry.yt_videoid))

    feed_name = '{}.xml'.format(channel_id)
    generated_feed.rss_file(feed_name)
    files_to_keep.append(feed_name)

    return files_to_keep


def setup_feed(channel_id, title, url):
    """Create the feed with initial information and return it"""
    generated_feed = FeedGenerator()
    generated_feed.title(title)
    generated_feed.load_extension('podcast')
    generated_feed.link(
        href='{}{}.xml'.format(url, channel_id), rel='self')
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
                          'outtmpl': './downloads/%(id)s.%(ext)s'}
    with youtube_dl.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download([link])


def cleanup_old_files(files_to_keep):
    """Delete files matching mp3 in the mp3_folder that are not found
    in files_to_keep.
    Delete files matching .xml in deploy_path not found in files_to_keep"""
    deploy_path = config.get('paths', 'deploy_path')
    mp3_folder = config.get('paths', 'mp3_folder')
    mp3s = [mp3 for mp3 in os.listdir('{}/{}'.format(deploy_path, mp3_folder))
            if mp3.endswith(".mp3")]

    feeds = [feed for feed in os.listdir(deploy_path) if feed.endswith('.xml')]

    to_delete = ["{}/{}".format(mp3_folder, old_file) for old_file in mp3s
                 if old_file not in files_to_keep]
    to_delete.extend([old_file for old_file in feeds
                      if old_file not in files_to_keep])

    for file_name in to_delete:
        print("Removing {}".format(file_name))
        os.remove("{}/{}".format(deploy_path, file_name))


def main():
    channel_ids = get_channel_ids()
    files_to_keep = []
    for channel_id in channel_ids:
        files_to_keep.extend(generate_feed(channel_id))

    cleanup_old_files(files_to_keep)




if __name__ == '__main__':
    main()
