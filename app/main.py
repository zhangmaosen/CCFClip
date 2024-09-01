import gradio as gr
import pysubs2
import ollama
from rapidfuzz import fuzz
from datetime import datetime
import pytz
import ffmpeg
import re
import os
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
        full_txt += line.text + ','
    return [full_txt, len(full_txt)]

def auto_clip(full_text, model_select, system_prompt, user_prompt,  temperature=0.1, num_ctx=30000,):
    response = ollama.chat(model=model_select, messages=[

        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt + full_text }
    ],options= {
        "num_ctx": num_ctx ,
        "temperature" : temperature
    }, keep_alive=-1)

    return response['message']['content']

def invert_find(short_text, srt_text):
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
                    if score > 70 :
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
    
    output_file = 'video/output.mp4'

    clips = []
    for i in range(len(subs)):
        sub1 = subs[i]
        st = datetime.fromtimestamp(sub1.start/1000, pytz.timezone('utc'))
        ed = datetime.fromtimestamp(sub1.end/1000, pytz.timezone('utc'))
        start_time = st.strftime('%H:%M:%S.%f')[:-3] #'00:00:12.1' # Start time for trimming (HH:MM:SS)
        end_time = ed.strftime('%H:%M:%S.%f')[:-3] # End time for trimming (HH:MM:SS)
        print(start_time, end_time	)
        clips.append(ffmpeg.input(video_file, hwaccel='cuda', ss=start_time, to=end_time)) #hwaccel = 'cpu'

    video_concat = ffmpeg.concat(*[stream['v'] for stream in clips], v=1, a=0).node
    audio_concat = ffmpeg.concat(*[stream['a'] for stream in clips], v=0, a=1).node

    output = ffmpeg.output(video_concat['v'], audio_concat['a'], output_file, vcodec='h264_nvenc', init_hw_device="cuda:1") #, vcodec='h264_nvenc', acodec='copy')
    output = ffmpeg.overwrite_output(output) 
    ffmpeg.run(output)

    return output_file
        
with gr.Blocks() as demo:
    with gr.Row():
        srt_file = gr.File(label="SRT File")
        srt_text = gr.Textbox(label="SRT Text", scale=3, autoscroll=False)
    gen_btn = gr.Button("提取全文内容")
    with gr.Row():
        with gr.Column():
            text_len = gr.Number(label="Text Length")
            full_text = gr.Textbox(label="Full Text", autoscroll=False)
        
        with gr.Column():
            default_sys_prompt = load_sys_prompt("sys_prompts/best_prompt.txt")
            sys_prompt_text = gr.Textbox(label="System Prompt", value=default_sys_prompt)
            sys_prompt_file = gr.File(label="System Prompt File")
        with gr.Column():
            default_usr_prompt = load_user_prompt("usr_prompts/user_prompt.txt")
            user_prompt_text = gr.Textbox(label="User Prompt", value=default_usr_prompt)
            user_prompt_file = gr.File(label="User Prompt File")

    clip_btn = gr.Button("摘录精彩片段")
    with gr.Row():
        with gr.Column():
            model_select = gr.Dropdown(["qwen2:72b-instruct", "gemma2:27b-instruct-q4_0", "deepseek-v2:16b"], label="Model", value="gemma2:27b-instruct-q4_0")
            temperature = gr.Slider(0, 1, value=0.1, step=0.1, label="Temperature")
            ctx_num = gr.Slider(1000, 40000, value=8092, step=64, label="context num")
        short_text = gr.Textbox(label="Short Text",  scale=4)
    
    edit_btn = gr.Button("定位到视频时间轴")
    with gr.Row():
        #model_select = gr.Dropdown(["qwen2:72b-instruct", "deepseek-v2:16b"], label="Model")
        invert_srt_text = gr.Textbox(label="精彩视频时间轴")
        with gr.Column():
            video_selected = gr.Dropdown(get_file_list("video"), label="Video List")
            clips_btn = gr.Button("合并视频")
            video = gr.Video()



    # read srt_file 
    srt_file.upload(fn=load_srt_file, inputs=srt_file, outputs=srt_text)
    gen_btn.click(fn=gen_full_text, inputs=srt_file, outputs=[full_text, text_len])

    clip_btn.click(fn=auto_clip, inputs=[full_text, model_select, sys_prompt_text, user_prompt_text, temperature, ctx_num], outputs=short_text)

    sys_prompt_file.upload(fn=load_sys_prompt, inputs=sys_prompt_file, outputs=sys_prompt_text)
    user_prompt_file.upload(fn=load_user_prompt, inputs=user_prompt_file, outputs=user_prompt_text)
    
    edit_btn.click(fn=invert_find, inputs=[short_text, srt_text], outputs=invert_srt_text)
    clips_btn.click(fn=edit_clips, inputs=[invert_srt_text, video_selected], outputs=video)
    #greet_btn.click(fn=greet, inputs=name, outputs=output, api_name="greet")

demo.launch()