import asyncio
import os
import time
import subprocess
import math
import logging
import re
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from SmartEncoder.Plugins.list import *

from SmartEncoder.Tools.progress import *
from SmartEncoder.Tools.ffmpeg_progress import progress_shell
#from SmartEncoder.Database.db import myDB

def filename(ul):
    # Remove square brackets, keeping the content inside
    ul = re.sub(r'\[', '', ul)
    ul = re.sub(r'\]', '', ul)
    # Remove curly braces and their contents
    ul = re.sub(r'\{.*?\}', '', ul)
    # Remove parentheses and their contents
    ul = re.sub(r'\(.*?\)', '', ul)
    # Remove strings like "720p", "1080p", "480p"
    ul = re.sub(r'\b\d+p\b', '', ul)
    # Remove strings starting with "@"
    ul = re.sub(r'\s@[\w_]+', '', ul)
    # Replace multiple spaces with a single space
    ul = ' '.join(ul.split())
    return ul

async def en_co_de(dl, message):
    pron = dl.split("/")[-1]
    sox = pron.split(".")[-1]
    ul = pron.replace(f".{sox}",".mkv")
    ul = filename(ul)  # Clean the ul filename
    TF = time.time()
    progress = f"progress-{TF}.txt"
    
    # ffmpeg encoding code 
    if codec[0] == "libx265":
        if audio_codec[0] == "libfdk_aac":
            cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress """{progress}""" -i """{dl}""" -map 0:v? -map 0:a? -map 0:s? -c:v libx265 -x265-params no-info=1 -crf {crf[0]} -s {qualityy[0]} -b:v 420k  -preset {preset[0]} -threads 3 -pix_fmt yuv420p -c:a libfdk_aac -profile:a aac_he_v2 -ac 2 -vbr 1 -c:s copy """{ul}""" -y'''
        elif audio_codec[0] == "libopus":
            cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress """{progress}""" -i """{dl}""" -filter_complex "drawtext=fontfile=headline1.ttf:text='Anime fusion':x='w*0.95-text_w':y=10:fontcolor=white@0.4:fontsize={watermark_size[0]}:enable='between(t,0,15)':alpha='if(lt(t,14)\,1\,if(lt(t\,15)\,(1-(t-14))/1\,0))'" -map 0:v:0 -map 0:a:? -map 0:s:? -map -0:t -c:v libx265 -x265-params no-info=1 -tag:v hvc1 -b:v 1M -maxrate 1M -bufsize 2M -crf {crf[0]} -s {qualityy[0]} -preset {preset[0]} -threads 4 -pix_fmt yuv420p -c:a libopus -profile:a aac_he -ac 1 -b:a {audio_[0]} -c:s copy """{ul}""" -y'''
    else:
        if audio_codec[0] == "libopus":
            cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress """{progress}""" -i """{dl}""" -map 0:a? -map 0:s? -map 0:v? -c:v libx264 -crf {crf[0]} -pix_fmt yuv420p -s {qualityy[0]} -preset {preset[0]} -c:a libopus -profile:a aac_he -ac 2 -b:a {audio_[0]} -c:s copy """{ul}""" -y'''
        elif audio_codec[0] == "libfdk_aac":
            cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress """{progress}""" -i """{dl}""" -vf "drawtext=fontfile=headline1.ttf:fontsize=15:fontcolor=white:bordercolor=black@0.50:x=w-tw-10:y=10:box=1:boxcolor=black@0.5:boxborderw=6:text="AnimeSpectrum' -map 0:v:0 -map 0:a:? -map 0:s:? -map -0:t -c:v libx264 -b:v 400k -crf {crf[0]} -s {qualityy[0]} -preset {preset[0]} -threads 4 -pix_fmt yuv420p -c:a libopus -profile:a aac_he -ac 1 -b:a {audio_[0]} -c:s copy -metadata title="Anime fusion" """{ul}""" -y'''
    
    # bot pm info for process -_-
    await progress_shell(cmd, dl, progress, TF, message, "**ENCODING IN PROGRESS**")
    
    if os.path.lexists(ul):
        return ul
    else:
        return None
