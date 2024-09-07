
import gradio as gr
from gradio_streamvideo import StreamVideo
import time

example = StreamVideo().example_value()

demo = gr.Interface(
    lambda x:x,
    StreamVideo(),  # interactive version of your component
    StreamVideo(),  # static version of your component
    # examples=[[example]],  # uncomment this line to view the "example version" of your component
)

 
if __name__ == "__main__":
    demo.launch() 