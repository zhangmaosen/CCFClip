import ffmpeg
import pysubs2
import time
from datetime import datetime
import pytz
#in_file = ffmpeg.input('/home/userroot/dev/CCFClip/video/术语访谈 - AI4Science之智能新药研发+20231127.mp4')
srt_file = '''1
00:21:46,770 --> 00:21:47,010
对

2
00:21:48,070 --> 00:21:49,260
所以很快看一下这张图

3
00:21:49,260 --> 00:21:50,926
就是一个蛋白质

4
00:21:50,930 --> 00:21:53,842
它上面通常有说有它有一个靶点

5
00:21:53,850 --> 00:21:55,926
这个靶点通常具备一些功能

6
00:21:56,110 --> 00:22:01,783
那药的原理就是能够在这个蛋白质的某一个区域的靶点用一个小分子药

7
00:22:01,810 --> 00:22:03,490
比如说这就是一个小分子药

8
00:22:03,500 --> 00:22:06,326
能够跟它产生一定的binding之后

9
00:22:07,210 --> 00:22:08,386
能够中和掉它

10
00:22:08,390 --> 00:22:10,293
或者把它的功能就抑制住

11
00:22:10,470 --> 00:22:18,550
所以我们要是我们需要理解的就是比如说这个蛋白质的结构跟它的那个那个靶点的三维结构

12
00:22:18,620 --> 00:22:20,744
还有它的表表位的那些性质

13
00:22:20,750 --> 00:22:26,330
还有然后之后就要设计这样一个三维的这样一个小分子药来跟它结合

14
00:22:26,680 --> 00:22:28,539
这里面当然我们可以很快想到

15
00:22:28,540 --> 00:22:30,169
就用这种生成式AI

16
00:22:30,600 --> 00:22:35,525
例如说我们团队在2023年的ICM就发表了一篇文章

17
00:22:35,540 --> 00:22:41,399
就是怎么样去生成一个small money drive

18
00:22:41,630 --> 00:22:42,575
这就是一个过程

19
00:22:42,880 --> 00:22:47,781
大家可以看到它从原来随机的决定每一个坐标上面是什么样的原子

20
00:22:48,200 --> 00:22:49,244
这个type是什么

21
00:22:49,250 --> 00:22:50,554
然后它坐标的位置

22
00:22:50,740 --> 00:22:53,635
然后用这个生成式模型来慢慢来学

23
00:23:00,810 --> 00:23:03,438
那这个跟生成图片其实很像

24
00:23:03,610 --> 00:23:06,418
就从一个随机的一个噪声不断

25
00:23:06,420 --> 00:23:08,409
怎么样能够做defu群之后

26
00:23:08,420 --> 00:23:10,950
生成一个是有语义的图片

27
00:28:49,940 --> 00:28:51,845
另外我只是再想想这个小分子药物

28
00:28:51,850 --> 00:28:53,748
其实很多时候你设计它的时候

29
00:28:53,750 --> 00:28:56,630
不单是你这你你要它跟某个靶点结合

30
00:28:56,750 --> 00:28:59,858
你还有时候还要限制它不能跟另外哪些靶点结合

31
00:29:00,140 --> 00:29:01,496
所以他这样一个生成的任务

32
00:29:01,500 --> 00:29:03,600
有时候他会给一些目标

33
00:29:03,600 --> 00:29:06,460
但是他同时要给几个是啊constrain

34
00:29:07,050 --> 00:29:10,352
不希望你跟这些靶点有有反应

35
00:29:10,360 --> 00:29:13,640
因为这样的话就会例如说会影响他的治疗效果

36
00:29:17,230 --> 00:29:19,660
第三个问题就是说通常小分子药物

37
00:29:19,670 --> 00:29:21,639
通常AI设计都难以合成

38
00:29:22,210 --> 00:29:25,390
另外我们想做的就是说在设计小分子的过程中

39
00:29:25,820 --> 00:29:27,954
也把拟合成这样一个问题

40
00:29:28,400 --> 00:29:31,214
这个也同时作为优化的一个目标

41
00:29:31,280 --> 00:29:33,648
所以当我们设计出这个小分子的时候

42
00:29:33,660 --> 00:29:36,686
同时也就可以推荐出它和可合成的路径

43
00:29:36,840 --> 00:29:41,936
因为一般小分子医药它通常是从最小的单元开始去合成起来

44
00:29:41,940 --> 00:29:44,700
所以如果中间这个路径找不到一个稳定的结构

45
00:29:44,700 --> 00:29:46,716
或者找不到一个能够

46
00:29:46,720 --> 00:29:49,138
或者说它的合成路径非常昂贵

47
00:29:49,300 --> 00:29:50,900
那这个可能也就不合适

48
00:29:50,950 --> 00:29:55,213
所以这边这样的一个问题就导就就让这个AI生成药物小分子药物

49
00:29:55,240 --> 00:29:57,390
其实整个问题就更复杂

50
00:29:58,370 --> 00:30:00,890
但也让这个问题就更更interesting

51
00:30:03,020 --> 00:30:07,181
最后我想这张也是蓝燕老师给我的很多启发

52
00:30:07,190 --> 00:30:10,318
就说我们今天看到这个AF在这个领域

53
00:25:03,600 --> 00:25:04,632
也是一种language


'''

# srt_file = '''15
# 00:22:28,540 --> 00:22:30,169
# 就用这种生成式AI
# '''


from moviepy.editor import *
def gen_download_video(srt_file, video_file):
    video_file = 'video/' + video_file
    print("merge clips")
    subs = pysubs2.SSAFile.from_string(srt_file)

    ts = int(time.time())
    output_file = 'stream' + f'/output_{ts}.mp4'

    movie = VideoFileClip(video_file)
    clips = []
    for i in range(len(subs)):
        sub1 = subs[i]
        st = datetime.fromtimestamp(sub1.start/1000, pytz.timezone('utc'))
        ed = datetime.fromtimestamp(sub1.end/1000, pytz.timezone('utc'))
        start_time = st.strftime('%H:%M:%S.%f')[:-3] #'00:00:12.1' # Start time for trimming (HH:MM:SS)
        end_time = ed.strftime('%H:%M:%S.%f')[:-3] # End time for trimming (HH:MM:SS)
        print(start_time, end_time	)
        clips.append(movie.subclip(start_time, end_time))
        #clips.append(ffmpeg.input(video_file,  ss=start_time, to=end_time, hwaccel = 'cuda')) #hwaccel = 'cpu'
        
    short_movie = concatenate_videoclips(clips)
    short_movie.write_videofile(output_file, fps=30)
    # video_concat = ffmpeg.concat(*[stream['v'] for stream in clips], v=1, a=0).node
    # audio_concat = ffmpeg.concat(*[stream['a'] for stream in clips], v=0, a=1).node
    #ffmpeg.concat(clips[0], clips[1])
    # output = ffmpeg.output(*clips, output_file,vcodec='h264_nvenc', video_bitrate="727k",threads=4) #, vcodec='h264_nvenc', acodec='copy')
    # output = ffmpeg.overwrite_output(output) 
    
    # ffmpeg.run(output)

    return output_file
#overlay_file = ffmpeg.input('overlay.png')
video_name = "计算+行业，如何助力千行百业？+20240105.mp4"
video_name = "术语访谈 - AI4Science之智能新药研发+20231127.mp4"
#video_name = '/home/userroot/dev/CCFClip/video/术语访谈 - AI4Science之智能新药研发+20231127.mp4'
gen_download_video(srt_file,video_name)
# start_time = '00:21:46' #'00:21:46.770'
# end_time = '00:21:48' #'00:21:47.010'
# in_file = ffmpeg.input(video_name)
# #overlay_file = ffmpeg.input('overlay.png')
# (
#     ffmpeg.concat(
#         in_file.trim(start_frame=1306*30, end_frame=1307*30),
#         in_file.trim(start_frame=30, end_frame=40),
#     )

#     .output('out.mp4')
#     .run()
# )
