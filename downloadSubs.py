import yt_dlp
import os
import re

def download_auto_subtitles(video_urls, lang='ru', output_dir='.'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    ydl_opts = {
        'skip_download': True, 
        'writeautomaticsub': True,
        'subtitleslangs': [lang],
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
    }

    for video_url in video_urls:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            if 'automatic_captions' in info_dict and lang in info_dict['automatic_captions']:
                ydl.download([video_url])
                subtitle_file_vtt = f"{output_dir}/{info_dict['title']}.{lang}.vtt"
                if os.path.exists(subtitle_file_vtt):
                    txt_file = f"{output_dir}/{info_dict['title']}.{lang}.txt"
                    convert_vtt_to_txt(subtitle_file_vtt, txt_file)
                    print(f"Subtitles downloaded and saved as {txt_file}")
                    os.remove(subtitle_file_vtt)
                    print(f"VTT file {subtitle_file_vtt} has been deleted.")
                else:
                    print(f"No subtitle file found in the expected format for video: {video_url}")
            else:
                print(f"No automatic subtitles found for language '{lang}' in the video: {video_url}")

def convert_vtt_to_txt(vtt_file, txt_file):
    try:
        with open(vtt_file, 'r', encoding='utf-8') as vtt, open(txt_file, 'w', encoding='utf-8') as txt:
            unique_lines = set()
            for line in vtt:
                # Remove lines with timestamps and the WEBVTT header
                if '-->' in line or line.strip() == '' or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
                    continue
                # Remove all tags using regex
                clean_line = re.sub(r'<[^>]+>', '', line).strip()
                if clean_line and clean_line not in unique_lines:
                    unique_lines.add(clean_line)
                    txt.write(clean_line + ' ')
    except Exception as e:
        print(f"Error converting {vtt_file} to {txt_file}: {e}")

video_urls = [
    'https://www.youtube.com/watch?v=pGxD08MSklA',
    'https://www.youtube.com/watch?v=k86jwgxyMWw',
    'https://www.youtube.com/watch?v=yBHwJBxSEPU'
]
download_auto_subtitles(video_urls, lang='ru', output_dir='subtitles')
