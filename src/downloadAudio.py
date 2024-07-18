import os
import yt_dlp as youtube_dl
import ffmpeg
import time

# Список видео
vids = ['https://www.youtube.com/watch?v=-RA7UStvSBI', 'https://www.youtube.com/watch?v=a18qTcWn-II']

# Опции для yt_dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': './outputs/%(id)s.%(ext)s',  # Измененный шаблон для имени файла
}

def split_file(input_file, output_pattern, chunk_size=25):
    """Разбивает аудиофайл на куски по заданному размеру."""
    try:
        probe = ffmpeg.probe(input_file)
        duration = float(probe['format']['duration'])
        file_size = os.path.getsize(input_file) / (1024 * 1024)  # размер в МБ

        # Определение количества кусков
        num_chunks = int(file_size // chunk_size) + 1

        for i in range(num_chunks):
            start_time = i * (duration / num_chunks)
            end_time = (i + 1) * (duration / num_chunks)
            output_file = f"{output_pattern}_part{i + 1}.mp3"

            ffmpeg.input(input_file, ss=start_time, to=end_time).output(output_file).run()
            print(f"Создан файл: {output_file}")

        os.remove(input_file)
    except ffmpeg.Error as e:
        print(f"Ошибка при разбиении файла: {e}")
        raise

def download_video(vid_url, attempts=5):
    """Скачивает видео с заданного URL с повторными попытками."""
    for attempt in range(attempts):
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(vid_url, download=True)
                video_id = info.get('id', None)
                output_file = f"./outputs/{video_id}.mp3"
                return output_file
        except Exception as e:
            print(f"Ошибка при скачивании видео: {e}")
            if attempt < attempts - 1:
                time.sleep(2)  # Задержка перед следующей попыткой
            else:
                with open("errors.txt", "a") as error_file:
                    error_file.write(f"Не удалось скачать видео: {vid_url}\n")
                return None

def process_videos(vids, attempts=5):
    """Обрабатывает все видео в списке: скачивает и разбиает при необходимости."""
    for vid in vids:
        output_file = download_video(vid)
        if output_file and os.path.getsize(output_file) > 25 * 1024 * 1024:
            for attempt in range(attempts):
                try:
                    split_file(output_file, output_file.replace('.mp3', ''))
                    break
                except Exception as e:
                    print(f"Ошибка при разбиении файла: {e}")
                    if attempt < attempts - 1:
                        time.sleep(2)  # Задержка перед следующей попыткой
                    else:
                        with open("errors.txt", "a") as error_file:
                            error_file.write(f"Не удалось разбиить файл: {output_file}\n")

process_videos(vids)
print("Завершено")
