import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './src')))

from downloadAudio import getTextWithGPT
from downloadSubs import downloadSubs

print('hello from app.py')

vids = [
    
]
language = 'en'
attempts=1

# getTextWithGPT(vids, attempts)
# downloadSubs(vids, language)