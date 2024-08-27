import gradio as gr
import pysubs2
import ollama
from rapidfuzz import fuzz
import re
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
    return full_txt

def auto_clip(full_text, model_select, system_prompt, user_prompt, num_ctx=30000, temperature=0.1):
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
            split_text = re.split(r'[，、？。！…]', match)
            
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

        
with gr.Blocks() as demo:
    with gr.Row():
        srt_file = gr.File(label="SRT File")
        srt_text = gr.Textbox(label="SRT Text", scale=3, autoscroll=False)
    gen_btn = gr.Button("提取全文内容")
    with gr.Row():
        full_text = gr.Textbox(label="Full Text", autoscroll=False)
        with gr.Column():
            sys_prompt_text = gr.Textbox(label="System Prompt")
            sys_prompt_file = gr.File(label="System Prompt File")
        with gr.Column():
            user_prompt_text = gr.Textbox(label="User Prompt")
            user_prompt_file = gr.File(label="User Prompt File")

    clip_btn = gr.Button("摘录精彩片段")
    with gr.Row():
        model_select = gr.Dropdown(["qwen2:72b-instruct", "deepseek-v2:16b"], label="Model")
        short_text = gr.Textbox(label="Short Text")
    
    edit_btn = gr.Button("定位到视频时间轴")
    with gr.Row():
        #model_select = gr.Dropdown(["qwen2:72b-instruct", "deepseek-v2:16b"], label="Model")
        invert_srt_text = gr.Textbox(label="精彩视频时间轴")


    # read srt_file 
    srt_file.upload(fn=load_srt_file, inputs=srt_file, outputs=srt_text)
    gen_btn.click(fn=gen_full_text, inputs=srt_file, outputs=full_text)

    clip_btn.click(fn=auto_clip, inputs=[full_text, model_select, sys_prompt_text, user_prompt_text], outputs=short_text)

    sys_prompt_file.upload(fn=load_sys_prompt, inputs=sys_prompt_file, outputs=sys_prompt_text)
    user_prompt_file.upload(fn=load_user_prompt, inputs=user_prompt_file, outputs=user_prompt_text)
    
    edit_btn.click(fn=invert_find, inputs=[short_text, srt_text], outputs=invert_srt_text)
    #greet_btn.click(fn=greet, inputs=name, outputs=output, api_name="greet")

demo.launch()