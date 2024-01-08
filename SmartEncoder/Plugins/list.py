# list.py>
"""
Python3 --> list
"""

from SmartEncoder.Database.db import myDB

class video:
  crf = []
  crf.append("33.5")
  codec = []
  codec.append("libx264")
  qualityy = []
  qualityy.append("846x480")
  
  
#myDB.set('crf', "29.5")
#video.codec.append("libx265")
#video.quality.append("852x480")

class audio:
  audio_codec = []
  audio_codec.append("libopus")
  audio_ = []
  audio_.append("32k")
 
class speed:
  preset = []
  preset.append("veryfast")

class watermark:
  size_one = []
  size_two = []

watermark.size_one.append('25')
watermark.size_two.append('30')
vanish = []
vanish.insert(0, "true")
#class queue:
#data = []
#queue = []
name = []
name.append("480p")

rename_queue = []
rename_task = []
rename_task.insert(0, "off")
