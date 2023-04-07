import os
import subprocess
from pytube import YouTube, Playlist
import eyed3
import time

def download_music(video, dir_name):
    vid_down = video.streams.filter(only_audio=True).first()
    default_filename = vid_down.default_filename
    vid_down.download(dir_name)

    thumbnial = video.thumbnail_url
    subprocess.run([
        'wget',
        '-O', os.path.join(dir_name, default_filename.replace('.mp4', '.jpg')),
        thumbnial
    ])

    subprocess.run([
        'ffmpeg',
        '-i', os.path.join(dir_name, default_filename),
        os.path.join(dir_name, default_filename.replace('.mp4', '.mp3'))
    ])

    audiofile = eyed3.load(os.path.join(dir_name, default_filename.replace('.mp4', '.mp3')))

    audiofile.tag.artist = video.author
    audiofile.tag.title = video.title
    audiofile.tag.images.set(3, open(os.path.join(dir_name, default_filename.replace('.mp4', '.jpg')), 'rb').read(), 'image/jpeg')
    audiofile.tag.save()

    os.remove(os.path.join(dir_name, default_filename.replace('.mp4', '.jpg')))

    os.remove(os.path.join(dir_name, default_filename))

    print("Downloaded: " + video.title)

def playlist_download():
    playlist_url = input("Enter the playlist URL: ")
    playlist = Playlist(playlist_url)

    if(playlist == None):
        print("Invalid URL")
        return
    
    dir_name = input("Enter the directory name of the playlist: ")

    print("Downloading playlist: " + playlist.title)

    failsDownloads = []    

    i = 0
    while i < len(playlist.videos):
        try:
            video = playlist.videos[i]
            download_music(video, dir_name)
            i+=1

        except Exception as e:
            print(e)
            print("Error downloading video: " + video.title)
            failsDownloads.append(i)
            i+=1
            continue

    j = 0

    while len(failsDownloads) > 0:
        print("Retrying failed downloads...")
        while j < len(failsDownloads):
            try:
                print('Fail downloads: ' + str(len(failsDownloads)))
                print('Current index: ' + str(j))
                video = playlist.videos[failsDownloads[j]]
                download_music(video, dir_name)
                j+=1
            except Exception as e:
                print(e)
                print("Error downloading video: " + video.title)
                time.sleep(10)
                print("Retrying...")
                continue

    print("Download Complete")

print("Youtube Downloader")
#Menu
while True:
    print("Options:")
    print("Enter '1' to download a youtube music playlist")
    print("Enter 'E' to exit")

    choice = input("What would you like to do? ")

    if(choice == '1'):
        playlist_download()
        continue
    elif(choice == 'E' or choice == 'e'):
        print("Exiting...")
        break
    else:
        print("XXXX Invalid Input XXXX\n")






