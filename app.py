import yt_dlp as youtube_dl

vids = ['https://www.youtube.com/watch?v=Iq7G8bOneGY']

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': './outputs/%(title)s.mp3',
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(vids)