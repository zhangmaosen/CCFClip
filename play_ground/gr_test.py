import gradio as gr

with gr.Blocks() as demo:

    d = gr.Dropdown(value= None, allow_custom_value= True, choices=["a", "b", "c"], label="Dropdown")
demo.launch()