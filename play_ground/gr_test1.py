import gradio as gr
from gradio_streamvideo import StreamVideo
import time

# Paths can be a list of strings or pathlib.Path objects
# corresponding to filenames or directories.
gr.set_static_paths(paths=["images", "stream"])
def test(input):
    # sleep 20 seconds
    time.sleep(20)
    #sleep(100)
    return input    
# The example files and the default value of the input
# will not be copied to the gradio cache and will be served directly.


with gr.Blocks() as demo:
    input = gr.Textbox()
    click_btn = gr.Button("Click me")
    video = StreamVideo()

    click_btn.click(fn= test, inputs=input, outputs=video)
demo.launch()