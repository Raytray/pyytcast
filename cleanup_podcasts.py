import os


def main():
    mypath = "/var/www/files"
    downloads_folder = "downloads"
    files = [f for f in os.listdir("{}/{}".format(mypath, downloads_folder))
             if f.endswith(".mp3")]

    feeds = [f for f in os.listdir(mypath) if f.endswith(".xml")]

    to_delete = files
    for feed_name in feeds:
        for file_name in files:
            if file_name in open("{}/{}".format(mypath, feed_name)).read():
                to_delete.remove(file_name)

    for file_name in to_delete:
        print("removing {}".format(file_name)
        os.remove("{}/{}/{}".format(mypath, downloads_folder, file_name))

if __name__ == "__main__":
    main()
