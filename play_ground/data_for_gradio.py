import gradio as gr
def get_t_value(j):
    print(j)
    return j

def send_value():
    return "hello"

def read_value(v):
    return v
input_textbox = gr.Textbox()
with gr.Blocks() as demo:
    d = gr.State()
    t = gr.Textbox(value=get_t_value,inputs=d, interactive=True)
    t2 = gr.Textbox(value=get_t_value,inputs=d, interactive=True)
    b = gr.Button("click")
    c = gr.Button("click2")
    b.click(send_value,inputs=None,outputs=d)
    c.click(read_value,inputs=t, outputs=d)

    gr.Examples(["hello", "bonjour", "merhaba"], input_textbox)
    input_textbox.render()
demo.launch(share=True)