vehicle / car tracking
========

### converting video

* to convert the video for test:
  '''ffmpeg -i VID_20180402_152729.mp4 -filter:v scale=-1:480 -c:a copy -an VID_20180402_152729_small.mp4
  ffmpeg -i VID_20180402_153105.mp4 -filter:v scale=-1:480 -c:a copy -an VID_20180402_153105_small.mp4
  ffmpeg -i VID_20180402_154210.mp4 -filter:v scale=-1:480 -c:a copy -an VID_20180402_154210_small.mp4
  ffmpeg -i VID_20180402_155155.mp4 -filter:v scale=-1:480 -c:a copy -an VID_20180402_155155_small.mp4
  ffmpeg -i VID_20180402_155458.mp4 -filter:v scale=-1:480 -c:a copy -an VID_20180402_155458_small.mp4'''

### unittest
* `python ./test/test_main.py`

### logging/todo
* to merge from fix/make-texts-class
