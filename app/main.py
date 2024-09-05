import gradio as gr
import pysubs2
import ollama
from rapidfuzz import fuzz
from datetime import datetime
import pytz
import ffmpeg
import re
import os
import shutil
from gradio_mycomponent import MyComponent

gr.set_static_paths("/home/userroot/dev/CCFClip/stream")
post_sys_prompt = '''
你是一个科技类媒体资深编辑，你的工作是把待编辑的内容中的换行符去掉，同时添加标点符号。
输出的格式为：* "编辑后的内容"
'''

post_user_prompt = '''
后面是待编辑的内容，请按要求完成工作：
'''
def save_video(video, target_path):
    """
    Saves the uploaded video to the specified target path.
    
    :param video: The uploaded video file.
    :param target_path: The directory where the video should be saved.
    :return: Path to the saved video.
    """
    # Ensure the directory exists
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    # Save the video
    shutil.move(video.name, target_path)
    return None
def load_srt_file(srt_file):
    with open(srt_file, 'r') as f:
        srt_text = f.read()
        return srt_text
def load_sys_prompt(prompt_file):
    with open(prompt_file, 'r') as f:
        prompt_text = f.read()
        return prompt_text

def load_user_prompt(prompt_file):
    with open(prompt_file, 'r') as f:
        prompt_text = f.read()
        return prompt_text
def gen_full_text(srt_file):
    subs = pysubs2.load(srt_file)
    full_txt = ''
    for line in subs:
        full_txt += line.text + '\n'
    return [full_txt, len(full_txt)]

def auto_clip(full_text, model_select, system_prompt, user_prompt,  temperature=0.1, num_ctx=30000,keep_alive=-1):
    response = ollama.chat(model=model_select, messages=[

        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt + full_text }
    ],options= {
        "num_ctx": num_ctx ,
        "temperature" : temperature
    }, keep_alive=keep_alive)

    return response['message']['content']

def post_run(full_text, model_select, system_prompt, user_prompt, temperature=0.1, num_ctx=30000, keep_alive=-1):
    response = ollama.chat(model=model_select, messages=[

        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt + full_text }
    ],options= {
        "num_ctx": num_ctx ,
        "temperature" : temperature
    }, keep_alive=keep_alive)

    return response['message']['content']
def invert_find(short_text, short_post_text, srt_text, fuzz_param):
    print(f"short_post_text is {short_post_text}")
    if short_post_text != "" :
        short_text = short_post_text
    last_cursor = 0
    subs = pysubs2.SSAFile.from_string(srt_text)
    subs_out = pysubs2.SSAFile()
    # read short_text by line
    for line in short_text.split('\n'):
        matches = re.findall(r'"(.*?)"', line)
        for match in matches:
            split_text = re.split(r'[，,、？。！…]', match)
            
            for seg in split_text:
                #print(f"seg is {seg}")
                for i in range(last_cursor, len(subs)):
                    score = (fuzz.ratio(seg, subs[i].text))
                    #print(f"score is {score}")
                    if score > fuzz_param :
                        last_cursor = 0
                        subs_out.append(subs[i])
                        break
    #print(subs_out.to_string('srt'))
    return subs_out.to_string('srt')

def get_file_list(directory):
    """获取指定目录下的所有文件名列表"""
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files
def edit_clips(srt_file, video_file):
    video_file = 'video/' + video_file
    print("merge clips")
    subs = pysubs2.SSAFile.from_string(srt_file)
#subs = pysubs2.load('cliped_srt/clip1.srt')
    
    output_file = 'stream/output.m3u8'

    clips = []
    for i in range(len(subs)):
        sub1 = subs[i]
        st = datetime.fromtimestamp(sub1.start/1000, pytz.timezone('utc'))
        ed = datetime.fromtimestamp(sub1.end/1000, pytz.timezone('utc'))
        start_time = st.strftime('%H:%M:%S.%f')[:-3] #'00:00:12.1' # Start time for trimming (HH:MM:SS)
        end_time = ed.strftime('%H:%M:%S.%f')[:-3] # End time for trimming (HH:MM:SS)
        print(start_time, end_time	)
        clips.append(ffmpeg.input(video_file,  ss=start_time, to=end_time)) #hwaccel = 'cpu'

    video_concat = ffmpeg.concat(*[stream['v'] for stream in clips], v=1, a=0).node
    audio_concat = ffmpeg.concat(*[stream['a'] for stream in clips], v=0, a=1).node
    
    output = ffmpeg.output(video_concat['v'].filter('scale', width='640', height='478'), audio_concat['a'], output_file,format='hls', start_number=0, hls_time=10, hls_list_size=0, vcodec='h264_nvenc', init_hw_device="cuda:1") #, vcodec='h264_nvenc', acodec='copy')
    output = ffmpeg.overwrite_output(output) 
    
    ffmpeg.run(output)

    #demo.load(None,None,None,js=scripts)

    return output_file
        
callback = gr.CSVLogger()
with gr.Blocks() as demo:
    with gr.Row():
        srt_file = gr.File(label="SRT File", file_types=[".srt"])
        with gr.Column(scale=2):
            video_path = gr.Textbox(value="./video", label="Target Directory")
            video_file = gr.File(label="Video File", file_types=[".mp4"])
            save_video_btn = gr.Button("upload Video")
        srt_text = gr.Textbox(label="SRT Text", scale=3, autoscroll=False)
    gen_btn = gr.Button("提取全文内容")
    with gr.Row():
        
        with gr.Column(scale=6):
            text_len = gr.Number(label="Text Length")
            full_text = gr.Textbox(label="Full Text", autoscroll=False)
        
        with gr.Column(scale=6):
            default_sys_prompt = load_sys_prompt("sys_prompts/best_prompt.txt")
            sys_prompt_text = gr.Textbox(label="System Prompt", value=default_sys_prompt)
            sys_prompt_file = gr.File(label="System Prompt File")
        with gr.Column(scale=4):
            default_usr_prompt = load_user_prompt("usr_prompts/user_prompt.txt")
            user_prompt_text = gr.Textbox(label="User Prompt", value=default_usr_prompt)
            user_prompt_file = gr.File(label="User Prompt File")
        flag_btn = gr.Button("Flag")

    # This needs to be called at some point prior to the first call to callback.flag()
    callback.setup([sys_prompt_text, user_prompt_text], "flagged_prompts")

    clip_btn = gr.Button("摘录精彩片段")
    with gr.Row():
        with gr.Column():
            model_select = gr.Dropdown(["qwen2:72b-instruct", "gemma2:27b-instruct-q4_0", "deepseek-v2:16b"], label="Model", value="qwen2:72b-instruct")
            temperature = gr.Slider(0, 1, value=0.1, step=0.1, label="Temperature")
            ctx_num = gr.Slider(1000, 40000, value=8092, step=64, label="context num")
            keep_alive = gr.Dropdown([-1, 0, 50], label="Keep Live", value=-1)
        with gr.Column(scale=4):
            
            short_text = gr.Textbox(label="Short Text",  scale=4)
            short_post_text = gr.Textbox(label="Short Post Text",  scale=4)
        with gr.Column():
            post_prompt_text = gr.Textbox(label="Post sys prompt",  scale=2, value=post_sys_prompt)
            post_user_text = gr.Textbox(label="Post user prompt",  scale=2, value=post_user_prompt)
            post_btn = gr.Button( "Post Run")
    
    
    with gr.Row():
        with gr.Column():
            fuzz_param = gr.Slider(0, 100, value=70, step=1, label="Fuzz Param")
            edit_btn = gr.Button("定位到视频时间轴")
            #model_select = gr.Dropdown(["qwen2:72b-instruct", "deepseek-v2:16b"], label="Model")
            invert_srt_text = gr.Textbox(label="精彩视频时间轴")
        with gr.Column():
            video_selected = gr.Dropdown(get_file_list("video"), label="Video List")
            clips_btn = gr.Button("合并视频")
            #video = gr.HTML("<video width='640' height='478' controls autoplay></video>")
            #video = gr.Video()
            test = MyComponent()


    save_video_btn.click(fn=save_video, inputs=[video_file, video_path], outputs=None)
    #video_file.change(fn=save_video, inputs=[video_file, video_path], outputs=None)
    flag_btn.click(lambda *args: callback.flag(list(args)), [sys_prompt_text, user_prompt_text], None, preprocess=False)

    # read srt_file 
    srt_file.upload(fn=load_srt_file, inputs=srt_file, outputs=srt_text)
    gen_btn.click(fn=gen_full_text, inputs=srt_file, outputs=[full_text, text_len])

    clip_btn.click(fn=auto_clip, inputs=[full_text, model_select, sys_prompt_text, user_prompt_text, temperature, ctx_num, keep_alive], outputs=short_text)

    sys_prompt_file.upload(fn=load_sys_prompt, inputs=sys_prompt_file, outputs=sys_prompt_text)
    user_prompt_file.upload(fn=load_user_prompt, inputs=user_prompt_file, outputs=user_prompt_text)
    
    edit_btn.click(fn=invert_find, inputs=[short_text, short_post_text, srt_text, fuzz_param], outputs=invert_srt_text)
    clips_btn.click(fn=edit_clips, inputs=[invert_srt_text, video_selected], outputs=None)

    post_btn.click(fn=post_run, inputs=[short_text, model_select, post_prompt_text, post_user_text, temperature, ctx_num,  keep_alive], outputs=short_post_text)
    #greet_btn.click(fn=greet, inputs=name, outputs=output, api_name="greet")

demo.launch()