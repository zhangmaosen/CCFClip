import gradio as gr
from ..app.functions import *

with gr.Blocks() as demo:
    gr.Interface(fn=functions.load_srt_file, inputs="file", outputs="text", label="Hello World")
    #gr.Interface(fn=functions.gen_full_text, inputs="text", outputs="text", label="Hello World")
    #gr.Interface(fn=functions.post_run, inputs=["text", "text", "text", "text", "number", "number", "number", "number"], outputs="text", label="Hello World")

