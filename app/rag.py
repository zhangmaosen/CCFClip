import gradio as gr

from utils.functions import *
from utils.personal_workspace import *

with gr.Blocks() as demo:
    
    d = gr.Dropdown(get_workspace_names(), interactive=True)

    # s = gr.State(get_workspace_names())
    # o = gr.Textbox(value=lambda x:x, inputs= s)

    # b = gr.Button("add workspace ")
    # b.click(lambda x: gr.State("add"), inputs= s, outputs= s)
    # #d.select(get_workspace_names, inputs=None, outputs=d)
    def refresh():
        names = get_workspace_names()
        return gr.Dropdown(choices=names)
    # d.focus(refresh, inputs = None, outputs=d)
    demo.load(refresh, inputs=None, outputs=d)
    d.input(lambda x: print(x), d, None)
    
demo.launch()