from functions import *

import gradio as gr


with gr.Blocks() as demo:
    model_select = gr.Dropdown(value="qwen2:72b-instruct",choices=['qwen2:72b-instruct'], label='Model')
    #system_prompt = gr.Textbox(label='System Prompt')
    user_prompt = gr.Textbox(label='User Prompt')
    #srt_content = gr.Textbox(label='srt text')
    srt_txt_content = gr.Textbox(label='srt txt text', lines=5)
    srt_file = gr.File(file_types=['srt'])
    #gr.Interface(fn=load_srt_file, inputs=srt_file, outputs=[srt_content, gr.Textbox()])

    gr.Interface(fn=gen_full_text, inputs=srt_file, outputs=[srt_txt_content, gr.Textbox()])
    #gr.Interface(fn=functions.post_run, inputs=["text", "text", "text", "text", "number", "number", "number", "number"], outputs="text", label="Hello World")

    gr.Interface(fn=run_model, inputs=[srt_txt_content, model_select, "text", "text", gr.Slider(value=0.1, minimum=0.01, maximum=1), gr.Slider(value=30000),gr.Radio(choices=[-1],value=-1), gr.Slider(minimum=50, maximum=900, value=300)], outputs=["text"])
    gr.Interface(fn=run_model, inputs=[srt_txt_content, model_select, "text", user_prompt, gr.Slider(value=0.1, minimum=0.01, maximum=1), gr.Slider(value=30000),gr.Radio(choices=[-1],value=-1), gr.Slider(minimum=50, maximum=900, value=300)], outputs=["text"])

    #gr.Interface(fn=run_model, inputs=srt_file, outputs=[srt_txt_content, gr.Textbox()])

    #gr.Interface(fn=run_model, inputs=srt_file, outputs=[srt_txt_content, gr.Textbox()])
demo.launch(server_name="0.0.0.0")