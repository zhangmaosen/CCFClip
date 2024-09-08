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
from gradio_streamvideo import StreamVideo
import time

gr.set_static_paths("/home/userroot/dev/CCFClip/stream")
post_sys_prompt = '''
你是一个科技类媒体资深编辑，你的工作是对待编辑的内容中摘录出最有吸引力的内容。注意摘录出的内容不能对原文进行修改。
输出的格式为：* "摘录出的内容"
'''

post_user_prompt = '''
后面是待编辑的内容：
'''

step_1_sys_prompt = '''
你是科技媒体的资深编辑，请分析出字幕中的精彩内容，从精彩内容中总结出小标题并输出，输出的小标题数量不要超过8个。注意减少对原理性知识的字幕裁剪.
输出的格式为：
<小标题1>
<小标题2>
<...>
<小标题8>
'''

step_2_sys_prompt_pre = '''
你是一个演讲类视频的字幕分析剪辑器，输入视频的字幕。从字幕中找到关于
'''
step_2_sys_prompt_post = '''
主题的字幕裁剪出来。注意保持裁剪的完整性，注意裁剪过程不要对字幕进行改写或总结，注意减少对原理性知识的字幕裁剪，注意如果从字幕中没有找到就不要裁剪出来，输出为空。
注意严格按照格式，按行输出裁剪出来的字幕，输出格式为：
* "输出的字幕1"
* "输出的字幕2"
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
    return [srt_text, len(srt_text)]
def load_sys_prompt(prompt_file):
    with open(prompt_file, 'r') as f:
        prompt_text = f.read()

    return prompt_text

def temp_save(out, input):
    return out + input 
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

def run_model(full_text, model_select, system_prompt, user_prompt,  temperature=0.1, num_ctx=30000,keep_alive=-1, num_predict=3000):
    response = ollama.chat(model=model_select, messages=[

        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt + full_text }
    ],options= {
        "num_ctx": num_ctx ,
        "temperature" : temperature,
        'num_predict' : num_predict
    }, keep_alive=keep_alive)

    return response['message']['content']
def auto_clip(full_text, model_select, system_prompt, user_prompt,  temperature=0.1, num_ctx=30000,keep_alive=-1, num_predict=768):
    response = ollama.chat(model=model_select, messages=[

        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt + full_text }
    ],options= {
        "num_ctx": num_ctx ,
        "temperature" : temperature,
        'num_predict' : num_predict
    }, keep_alive=keep_alive)

    return response['message']['content']

def post_run(full_text, model_select, system_prompt, user_prompt, temperature=0.1, num_ctx=30000, keep_alive=-1, num_predict=768):
    response = ollama.chat(model=model_select, messages=[

        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt + full_text }
    ],options= {
        "num_ctx": num_ctx ,
        "temperature" : temperature,
        'num_predict' : num_predict
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
            split_text = re.split(r'[，,、？。！…：；]', match)
            
            for seg in split_text:
                #print(f"seg is {seg}")
                for i in range(last_cursor, last_cursor + len(subs)):
                    current_index = i % len(subs)
                    score = (fuzz.ratio(seg, subs[current_index].text))
                    #print(f"score is {score}")
                    if score > fuzz_param :
                        last_cursor = current_index + 1
                        subs_out.append(subs[current_index])
                        break


    #print(subs_out.to_string('srt'))
    return subs_out.to_string('srt')

# def merge_sys_prompt(pre, input, post):
#     # get input line by line
#     input_lines = input.split('\n')
#     out_lines = []
#     for i in range(len(input_lines)):
#         out_lines.append(f"\n第{i+1}步，从字幕中找到关于：\n" + input_lines[i] )
#     output = pre.strip() + "".join(out_lines) + post
#     return output
def get_file_list(directory):
    """获取指定目录下的所有文件名列表"""
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files
def edit_clips(srt_file, video_file):
    video_file = 'video/' + video_file
    print("merge clips")
    subs = pysubs2.SSAFile.from_string(srt_file)
#subs = pysubs2.load('cliped_srt/clip1.srt')
    
    # get current timestamp as second
    ts = int(time.time())
    output_file = 'stream' + f'/output_{ts}.m3u8'

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

    return "http://127.0.0.1:7860/file="+ output_file
def download_clips(srt_file, video_file):
    video_file = 'video/' + video_file
    print("merge clips")
    subs = pysubs2.SSAFile.from_string(srt_file)
#subs = pysubs2.load('cliped_srt/clip1.srt')
    
    # get current timestamp as second
    ts = int(time.time())
    output_file = 'stream' + f'/output_{ts}.mp4'

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
    
    output = ffmpeg.output(video_concat['v'], audio_concat['a'], output_file,format='mp4',  vcodec='h264_nvenc', init_hw_device="cuda:1") #, vcodec='h264_nvenc', acodec='copy')
    output = ffmpeg.overwrite_output(output) 
    
    ffmpeg.run(output)

    #demo.load(None,None,None,js=scripts)

    return output_file

dynamic_prompts = []
dynamic_outputs = []
dynamic_btns = []
callback = gr.CSVLogger()
with gr.Blocks() as demo:
    
    with gr.Row():
        with gr.Column(scale=1):


            srt_file = gr.File(label="SRT File", file_types=[".srt"])
            video_path = gr.Textbox(value="./video", label="Target Directory", visible=True)
            video_file = gr.File(label="Video File", file_types=[".mp4"], visible=True)
            save_video_btn = gr.Button("upload Video", visible=True)
        with gr.Column(scale=2):
            with gr.Row():
                model_select = gr.Dropdown(["qwen2:72b-instruct","llama3.1:70b-instruct-q2_K", "gemma2:27b-instruct-q4_0", "deepseek-v2:16b"], scale=2, label="Model", value="qwen2:72b-instruct")
                temperature = gr.Slider(0, 1, value=0.1, step=0.1, label="Temperature")
                ctx_num = gr.Slider(1000, 40000, value=28092, step=64, label="context num")
                keep_alive = gr.Dropdown([-1, 0, 50], label="Keep Live", value=-1)
                pred_num = gr.Slider(10, 4000, value=150, step=1, label="predict num")
            with gr.Row():
                with gr.Column():
                    srt_text_len = gr.Number(label="Length")
                    srt_text = gr.Textbox(label="SRT Text", scale=3, autoscroll=False,max_lines=10)
                with gr.Column():
                    text_len = gr.Number(label="Text Length")
                    full_text = gr.Textbox(label="Full Text", autoscroll=False, max_lines=10)
            gen_btn = gr.Button("提取全文内容")
    with gr.Row(visible=False):
        

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
            step_1_sys_prompt = gr.Textbox(label="Step 1 System Prompt", value=step_1_sys_prompt)
            step_1_usr_prompt = gr.Textbox(label="Step 1 User Prompt", value=default_usr_prompt, visible=False)
            step_1_btn = gr.Button( "Step 1 Run")
            
        with gr.Column():
            step_1_output = gr.Textbox(label="Step 1 Output", autoscroll=False)
    gr.HTML("<hr>")
    with gr.Row():

        @gr.render(inputs=[gr.Text(step_2_sys_prompt_pre, visible=False), step_1_output, gr.Text(step_2_sys_prompt_post, visible=False)])
        def add_sys_prompt(pre, input, post):
            # get input line by line
            input_lines = input.split('\n')
            with gr.Column():
                for i in range(len(input_lines)) :
                    with gr.Row():
                        sys_prompt = pre+ input_lines[i] + ""+post
                        #dynamic_prompts.append()
                        p = gr.Textbox(sys_prompt,scale=3)
                        o = gr.Textbox(i, scale=7)
                        #dynamic_outputs.append()
                        with gr.Column():
                            btn = gr.Button("生成",scale=1)
                            save_btn = gr.Button("保存",scale=1)
                        #dynamic_btns.append()
                        save_btn.click(fn=temp_save, inputs=[o, short_text], outputs=[short_text])
                        btn.click(fn=run_model, inputs=[full_text, model_select, p, step_1_usr_prompt, temperature, ctx_num, keep_alive, pred_num], outputs=o)

    with gr.Row(visible=False):
        with gr.Column():
            step_2_sys_prompt = gr.Textbox(label="Step 2 System Prompt", value=step_2_sys_prompt_pre)
            step_2_usr_prompt = gr.Textbox(label="Step 2 User Prompt", value=default_usr_prompt, visible=False)
            step_2_btn = gr.Button( "Step 2 Run")
        with gr.Column():
            step_2_output_len = gr.Number(label="Text Length")
            step_2_output = gr.Textbox(label="Step 2 Output", autoscroll=False)
    with gr.Row():

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
            clips_btn = gr.Button("生成预览视频")
            #video = gr.HTML("<video width='640' height='478' controls autoplay></video>")
            #video = gr.Video()
            s_video = StreamVideo()
            download_btn = gr.Button("生成下载视频")
            d_video = gr.File()

    
    #step_1_output.change(fn=merge_sys_prompt, inputs=[gr.Text(step_2_sys_prompt_pre, visible=False), step_1_output, gr.Text(step_2_sys_prompt_post, visible=False)], outputs=step_2_sys_prompt)
    step_1_btn.click(fn=run_model, inputs=[full_text, model_select, step_1_sys_prompt, step_1_usr_prompt, temperature, ctx_num, keep_alive, pred_num], outputs=step_1_output)
    step_2_btn.click(fn=run_model, inputs=[full_text, model_select, step_2_sys_prompt, step_2_usr_prompt, temperature, ctx_num, keep_alive, pred_num], outputs=step_2_output)

    step_2_output.change(fn=lambda x: x, inputs=[step_2_output], outputs=[short_text])
    step_2_output.change(fn=lambda x: len(x), inputs=[step_2_output], outputs=[step_2_output_len])

    save_video_btn.click(fn=save_video, inputs=[video_file, video_path], outputs=None)
    #video_file.change(fn=save_video, inputs=[video_file, video_path], outputs=None)
    flag_btn.click(lambda *args: callback.flag(list(args)), [sys_prompt_text, user_prompt_text], None, preprocess=False)

    # read srt_file 
    srt_file.upload(fn=load_srt_file, inputs=srt_file, outputs=[srt_text,srt_text_len])
    gen_btn.click(fn=gen_full_text, inputs=srt_file, outputs=[full_text, text_len])

    clip_btn.click(fn=auto_clip, inputs=[full_text, model_select, sys_prompt_text, user_prompt_text, temperature, ctx_num, keep_alive], outputs=short_text)

    sys_prompt_file.upload(fn=load_sys_prompt, inputs=sys_prompt_file, outputs=sys_prompt_text)
    user_prompt_file.upload(fn=load_user_prompt, inputs=user_prompt_file, outputs=user_prompt_text)
    
    edit_btn.click(fn=invert_find, inputs=[short_text, short_post_text, srt_text, fuzz_param], outputs=invert_srt_text)
    clips_btn.click(fn=edit_clips, inputs=[invert_srt_text, video_selected], outputs=s_video)
    download_btn.click(fn=download_clips, inputs=[invert_srt_text, video_selected], outputs=d_video)
    post_btn.click(fn=post_run, inputs=[short_text, model_select, post_prompt_text, post_user_text, temperature, ctx_num,  keep_alive], outputs=short_post_text)
    #greet_btn.click(fn=greet, inputs=name, outputs=output, api_name="greet")

demo.launch() 