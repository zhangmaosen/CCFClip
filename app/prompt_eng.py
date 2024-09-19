from utils.functions import *

import gradio as gr
import asyncio
def gen_full_text2(srt_file):
    subs = pysubs2.load(srt_file)
    full_txt = ''
    for line in subs:
        full_txt += line.text + '\n'

    #docs = semantic_chunk(full_txt)
    #print(docs)
    return [ len(full_txt), full_txt]
with gr.Blocks() as demo:
    model_select = gr.Dropdown(value="qwen2:72b-instruct",choices=['qwen2:7b-instruct','qwen2:72b-instruct'], label='Model')
    #system_prompt = gr.Textbox(label='System Prompt')
    user_prompt = gr.Textbox(label='User Prompt', value="资料的原文：{}")
    #srt_content = gr.Textbox(label='srt text')
    srt_txt_content = gr.Textbox(label='srt txt text', lines=5, interactive=True)
    srt_file = gr.UploadButton(file_types=['.srt'])
    #gr.Interface(fn=load_srt_file, inputs=srt_file, outputs=[srt_content, gr.Textbox()])

    gr.Interface(fn=gen_full_text2, inputs=srt_file, outputs=[ gr.Textbox(),srt_txt_content])
    #gr.Interface(fn=functions.post_run, inputs=["text", "text", "text", "text", "number", "number", "number", "number"], outputs="text", label="Hello World")

    gr.Interface(fn=run_model, inputs=["text",srt_txt_content, model_select,  user_prompt, gr.Slider(value=0.1, minimum=0.01, maximum=1), gr.Slider(maximum=30000,value=30000),gr.Radio(choices=[-1],value=-1), gr.Slider(minimum=50, maximum=30000, value=300)], outputs=["text"])

demo.launch(server_name="0.0.0.0")