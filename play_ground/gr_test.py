import gradio as gr

with gr.Blocks() as demo:

    textbox = gr.Textbox("Hello World!")
    statement = gr.Textbox()

    def on_select(value, evt: gr.SelectData):
        return f"You selected {evt.value} at {evt.index} from {evt.target}"

    textbox.select(on_select, textbox, statement)

demo.launch()