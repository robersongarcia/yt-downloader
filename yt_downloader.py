import os
import subprocess
from pytube import YouTube, Playlist

def playlist_download():
    playlist_url = input("Enter the playlist URL: ")
    playlist = Playlist(playlist_url)

    if(playlist == None):
        print("Invalid URL")
        return
    
    dir_name = input("Enter the directory name of the playlist: ")

    print("Downloading playlist: " + playlist.title)
    
    for video in playlist.videos:
        try:
            vid_down = video.streams.filter(only_audio=True).first()
            default_filename = vid_down.default_filename
            vid_down.download(dir_name)

            subprocess.run([
                'ffmpeg',
                '-i', os.path.join(dir_name, default_filename),
                os.path.join(dir_name, default_filename.replace('.mp4', '.mp3'))
            ])

            os.remove(os.path.join(dir_name, default_filename))
            print("Downloaded: " + video.title)

        except Exception as e:
            print(e)
            print("Error downloading video: " + video.title)
            continue

    print("Download Complete")

print("Youtube Downloader")
#Menu
while True:
    print("Options:")
    print("Enter '1' to download a video")
    print("Enter '2' to download an audio")
    print("Enter '3' to download a playlist")
    print("Enter '4' to exit")

    choice = input("What would you like to do? ")

    if choice == '1':
        print("Video")
        continue
    
    if choice == '2':
        print("Audio")
        continue

    if choice == '3':
        playlist_download()
        continue

    if choice == '4':
        print("Exiting")
        break

    else:
        print("XXXX Invalid Input XXXX\n")






