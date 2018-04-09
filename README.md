### topics: vehicle / car tracking

### preparing the test data
### to convert the video for test:

`ffmpeg -i <raw video>.mp4 -filter:v scale=-1:480 -c:a copy -an <re-sampled video.mp4>`


### to run the python unittest
`python ./test/test_main.py`
