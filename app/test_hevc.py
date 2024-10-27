import gradio as gr

import ffmpeg
import pysubs2
def convert_video(video_file, srt_file):

    #read start and end time pairs from srt format file srt_file
    subs = pysubs2.SSAFile.load(srt_file)
    
    trim_code = ''
    for idx in range(len(subs)):
        #print(sub.times)
        start, end = subs[idx].start/1000, subs[idx].end/1000

        trim_code = trim_code + f"            input_video.trim(start={start}, end={end}),\n"
        break
        #print(f"start: {start}, end: {end}")
    code = f'''
input_video = ffmpeg.input("{video_file}", hwaccel="cuda")
(
    ffmpeg
    .concat(
{trim_code}
        
    )
    .output('output.mp4',  vcodec="h264_nvenc", acodec='copy')
    .run(overwrite_output=True)
)'''
#     code = f'''
# print("hello")
#     '''
    exec(code)
    print(f"code is {code}")
        # output(f"test/out/output{idx}.mp4", vcodec="h264_nvenc", acodec='copy').run(overwrite_output=True)
        # break
    # merge all output files into one video file
    # ffmpeg.concat(
    #     *[ffmpeg.input(f"test/out/output{idx}.mp4") for idx in range(len(subs))],
    #     v=1, a=1
    # ).output("output.mp4").run(overwrite_output=True)
    return "output.mp4"

demo = gr.Interface(convert_video, [gr.FileExplorer(root_dir='test', file_count='single'), gr.FileExplorer(root_dir='test', file_count='single')], gr.File(label="Output Video"))

demo.launch(server_name='0.0.0.0', server_port=7777)