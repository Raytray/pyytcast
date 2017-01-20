# pyytcast

I ran out of podcasts, but there's a ton of great content on youtube that I could listen to.
Just need need to get them in a good audio only format in a parseable feed.
This is that project.

This service runs and generates a feed each time it's ran. To keep a feed up to date, run the script multiple days a day.

It will not redownload files if retrieved once before.

# Config.conf
This project relies on a configuration file. A sample is included with the project.

```
[youtube]
channel_ids=test_id,another_test_id, test_with_strip

[paths]
mp3_folder=downloads
deploy_path=./
url=http://localhost/
```

```channel_ids``` indicates the channel ids that channels that the service will fetch. A channel id can typically be found by going to a youtube channel's home page.

```mp3_folder``` indicates where the mp3 files should be downloaded to.
```deploy_path``` indicates where the feeds would be moved to. This project expects that the mp3_folder is a subdirectory to the ```deploy_path```
```url``` is the host of the files.
