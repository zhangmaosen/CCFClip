import gradio as gr

from utils.functions import *

with gr.Blocks() as demo:
    
    gr.Interface(gen_download_video, ["text", "text"], "video")


demo.launch()