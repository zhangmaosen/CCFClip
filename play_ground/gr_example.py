import gradio as gr

with gr.Blocks() as demo:
    prompts = {"a":"sdfsfsd",
               "b":"sdflsafjslfk"}
    text = gr.Textbox(label="Text")
    text2 = gr.Textbox(label="Text2")
    e = gr.Examples(["a","b"], inputs=text, outputs=text2, fn=lambda x: prompts[x], cache_examples=False, run_on_click=True)
    
demo.launch()