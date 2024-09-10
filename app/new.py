import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        gr.Interface(lambda x:x, inputs=[gr.File()], outputs="text")
        gr.Interface(lambda x:x, inputs="text", outputs=None)

    with gr.Row():
        gr.Textbox()
demo.launch()