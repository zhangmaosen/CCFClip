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
from functions import *
gr.set_static_paths("/home/userroot/dev/CCFClip/stream")
post_sys_prompt = '''
你是一个科技类媒体资深编辑，你的工作是对待编辑的内容中摘录出最有吸引力的内容。注意摘录出的内容不能对原文进行修改。
输出的格式为：* "摘录出的内容"
'''

post_user_prompt = '''
后面是待编辑的内容：
'''

step_1_sys_prompt = '''
你是科技媒体的资深编辑，请分析出字幕中的精彩内容，从精彩内容中总结出标题并输出，输出的标题数量不要超过8个。注意减少对原理性知识的字幕裁剪.
输出的格式为：注意"和"是连接符
"标题1"
'''

step_2_sys_prompt_pre = '''你是一个演讲类视频资深编辑，你对精彩的定义是精辟的定义或者独到的问答或者是通俗易懂的过程描述或者是科技行业的精彩定义。输入视频的速记稿。从速记稿中找到表达
'''
step_2_sys_prompt_post = '''
含义的精彩且连续的完整片段并输出。注意没有找到就输出"没有找到"并且马上停止输出。注意不要改写找到的片段的文字。
输出需严格按照如下格式：
* "文本1" 注意"是连接符
'''

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
                local_or_online = gr.Radio(["local", "online"], value="local", label="Model Source", min_width=30)
                app_key = gr.Textbox(label="API Key", value="", visible=False)
                @gr.render(inputs=[local_or_online])
                def change_model_source(local_or_online):
                    if local_or_online == "online":
                        key = gr.Textbox(label="API Key",scale=4)
                        key.change(fn=lambda x: x, inputs=[key], outputs=[app_key])
                model_select = gr.Dropdown(["qwen2:72b-instruct","qwen2:7b-instruct","llama3.1:70b-instruct-q2_K", "gemma2:27b-instruct-q4_0", "deepseek-v2:16b"], scale=2, label="Model", value="qwen2:72b-instruct")
                temperature = gr.Slider(0, 1, value=0.1, step=0.1, label="Temperature")
                ctx_num = gr.Slider(1000, 40000, value=32000, step=64, label="context num")
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
        with gr.Column(scale=4, visible=True):
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
            step_1_output = gr.Textbox(label="Step 1 Output")
    gr.HTML("<hr>")
    with gr.Row():

        @gr.render(inputs=[gr.Text(step_2_sys_prompt_pre, visible=False), step_1_output, gr.Text(step_2_sys_prompt_post, visible=False)])
        def add_sys_prompt(pre, input, post):
            # get input line by line
            input_lines = input.split('\n')
            with gr.Column():
                for i in range(len(input_lines)) :
                    with gr.Row():
                        sys_prompt = pre.strip()+ input_lines[i].strip() +post.strip()
                        #dynamic_prompts.append()
                        p = gr.Textbox(sys_prompt,scale=3)
                        o = gr.Textbox(i, scale=7)
                        #dynamic_outputs.append()
                        with gr.Column():
                            btn = gr.Button("生成",scale=1)
                            save_btn = gr.Button("保存",scale=1)
                        #dynamic_btns.append()
                        save_btn.click(fn=temp_save, inputs=[o, short_text], outputs=[short_text])
                        btn.click(fn=run_model, inputs=[full_text, model_select, p, step_1_usr_prompt, temperature, ctx_num, keep_alive, pred_num, local_or_online, app_key], outputs=o)

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
    step_1_btn.click(fn=run_model, inputs=[full_text, model_select, step_1_sys_prompt, step_1_usr_prompt, temperature, ctx_num, keep_alive, pred_num, local_or_online, app_key], outputs=step_1_output)
    step_2_btn.click(fn=run_model, inputs=[full_text, model_select, step_2_sys_prompt, step_2_usr_prompt, temperature, ctx_num, keep_alive, pred_num, local_or_online, app_key], outputs=step_2_output)

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

demo.launch(server_name='0.0.0.0') 