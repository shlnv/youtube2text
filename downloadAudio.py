import os
import yt_dlp as youtube_dl
import ffmpeg

# Список видео
vids = ['https://www.youtube.com/watch?v=-RA7UStvSBI']

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

    except ffmpeg.Error as e:
        print(f"Ошибка при разбиении файла: {e}")

# Скачивание и обработка видео
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    result = ydl.download(vids)

    # Определение идентификатора видео
    info = ydl.extract_info(vids[0], download=False)
    video_id = info.get('id', None)
    output_file = f"./outputs/{video_id}.mp3"

    # Проверка существования файла
    if not os.path.exists(output_file):
        print(f"Файл не найден: {output_file}")
    else:
        print(f"Файл найден: {output_file}")

    # Проверка размера файла и разбиение, если необходимо
    if os.path.getsize(output_file) > 25 * 1024 * 1024:
        split_file(output_file, f"./outputs/{video_id}")

print("Завершено")