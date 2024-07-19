import os
import yt_dlp as youtube_dl
import ffmpeg
import time
from openai import OpenAI
from dotenv import load_dotenv

def getTextWithGPT(vids, attempts=5):
    load_dotenv()

    openAIkey = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=openAIkey)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': './outputs/%(id)s.%(ext)s',
    }

    def split_file(input_file, output_pattern, chunk_size=25):
        try:
            probe = ffmpeg.probe(input_file)
            duration = float(probe['format']['duration'])
            file_size = os.path.getsize(input_file) / (1024 * 1024)  # size in mb

            # how many parts
            num_chunks = int(file_size // chunk_size) + 1

            for i in range(num_chunks):
                start_time = i * (duration / num_chunks)
                end_time = (i + 1) * (duration / num_chunks)
                output_file = f"{output_pattern}_part{i + 1}.mp3"

                ffmpeg.input(input_file, ss=start_time, to=end_time).output(output_file).run()
                print(f"File created: {output_file}")

            os.remove(input_file)
        except ffmpeg.Error as e:
            print(f"File split error: {e}")
            raise

    def download_video(vid_url, attempts=5):
        for attempt in range(attempts):
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(vid_url, download=True)
                    video_id = info.get('id', None)
                    output_file = f"./outputs/{video_id}.mp3"
                    return output_file
            except Exception as e:
                print(f"Download video error: {e}")
                if attempt < attempts - 1:
                    time.sleep(2)
                else:
                    with open("errors.txt", "a") as error_file:
                        error_file.write(f"Couldn't download video: {vid_url}\n")
                    return None

    def transcribe_audio_files():
        for filename in os.listdir('./outputs'):
            if filename.endswith(".mp3"):
                audio_file_path = os.path.join('./outputs', filename)
                transcript_file_path = audio_file_path.replace(".mp3", ".txt")

                with open(audio_file_path, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        file=audio_file,
                        model="whisper-1",
                        response_format="text"
                    )

                with open(transcript_file_path, "w", encoding="utf-8") as text_file:
                    text_file.write(transcript)
                print(f"Transcript file created: {transcript_file_path}")

    for vid in vids:
        output_file = download_video(vid, attempts)
        if output_file and os.path.getsize(output_file) > 25 * 1024 * 1024:
            for attempt in range(attempts):
                try:
                    split_file(output_file, output_file.replace('.mp3', ''))
                    break
                except Exception as e:
                    print(f"Split file error: {e}")
                    if attempt < attempts - 1:
                        time.sleep(2)
                    else:
                        with open("errors.txt", "a") as error_file:
                            error_file.write(f"Couldn't split file: {output_file}\n")
        transcribe_audio_files()

    print("Finished")