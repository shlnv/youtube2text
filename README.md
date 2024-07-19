This program extracts text from one or multiple YouTube videos using two different methods: a paid method (using GPT) and a free method (using YouTube's automatic subtitle generation). For the paid method, you need to enter your OpenAI API key. The program has no user interface. I haven't tested the program on Unix. To run the program on Windows, you need to have Python, Poetry, ffprobe, and ffmpeg installed.

Steps to Follow:

1. Install Python: https://www.python.org/
2. Install Poetry: https://python-poetry.org/
3. Install ffprobe and ffmpeg: https://ffmpeg.org/download.html
4. Clone this repository.
5. In the root directory of the cloned repository, create a file named ".env".
6. In the ".env" file, create a variable containing your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

Replace "your_openai_api_key_here" with your actual key (if you plan to use the paid method).

7. In the console, navigate to the root directory of the project and run the command:

poetry install

8. Run the command:

poetry shell

9. Open the file app.py.

10. Add the YouTube video links to the "vids" array as shown:

vids = [
    'https://www.youtube.com/watch?v=example001',
    'https://www.youtube.com/watch?v=example002',
    'https://www.youtube.com/watch?v=example003',
]

11. Change the value of the language variable to the language used in the videos (if you plan to use subtitles).

12. Uncomment "getTextWithGPT" function by removing the "#" if you plan to use your OpenAI key. Uncomment "downloadSubs" function if you want to extract subtitle texts.

13. Save the app.py file.

14. In the Poetry Shell, run the command:

python app.py

15. The output of "getTextWithGPT" function will be saved in the "outputs" folder.

Note: You need to manually clear "outputs" folder before each run.

The output of the downloadSubs function will be saved in the "subs" folder.