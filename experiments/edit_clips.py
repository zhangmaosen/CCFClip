import ffmpeg
import pysubs2
from datetime import datetime
import pytz
#load srt file by pysubs2

def edit_clips(srt_file):
    print("merge clips")
    subs = pysubs2.load(srt_file)
#subs = pysubs2.load('cliped_srt/clip1.srt')
    
    output_file = 'video/output.mp4'

    clips = []
    for i in range(len(subs)):
        sub1 = subs[i]
        st = datetime.fromtimestamp(sub1.start/1000, pytz.timezone('utc'))
        ed = datetime.fromtimestamp(sub1.end/1000, pytz.timezone('utc'))
        start_time = st.strftime('%H:%M:%S.%f')[:-3] #'00:00:12.1' # Start time for trimming (HH:MM:SS)
        end_time = ed.strftime('%H:%M:%S.%f')[:-3] # End time for trimming (HH:MM:SS)
        print(start_time, end_time	)
        clips.append(ffmpeg.input("video/jinrongzichan.mp4", hwaccel = 'cuda', ss=start_time, to=end_time))

    video_concat = ffmpeg.concat(*[stream['v'] for stream in clips], v=1, a=0).node
    audio_concat = ffmpeg.concat(*[stream['a'] for stream in clips], v=0, a=1).node

    output = ffmpeg.output(video_concat['v'], audio_concat['a'], output_file, vcodec='h264_nvenc') #, vcodec='h264_nvenc', acodec='copy')
    output = ffmpeg.overwrite_output(output) 
    ffmpeg.run(output)

    return output_file