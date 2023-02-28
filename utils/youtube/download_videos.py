from pytube import Playlist
import pdb

DOWNLOAD_FOLDER = r"D:\00. 개인\01. 강의\01. 운영체제(널널한 개발자)"

pl = Playlist('https://www.youtube.com/watch?v=ZrNp9Be83qQ&list=PLXvgR_grOs1DGFOeD792kHlRml0PhCe9l')
total = len(pl)
for i, video in enumerate(pl.videos, 1):
    if i<26: continue
    print("Progress => [%s/%s]" % (i, total))
    try:
        high_res_video = video.streams.get_highest_resolution()
    except Exception as e:
        print("Error msg: {e}".format(e=e))
        continue

    print("mimetype: " + high_res_video.mime_type)
    print("Start downloading...")
    high_res_video.download(DOWNLOAD_FOLDER)
    print("Download is completed.")