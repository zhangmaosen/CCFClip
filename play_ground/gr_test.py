import gradio as gr

with gr.Blocks() as demo:

    textbox = gr.Textbox("Hello World!", autofocus=True, key =2)
    print(id(textbox))
    statement = gr.Textbox()
    out = gr.Textbox()
    with gr.Row():
        d_btn = gr.Button("Demo")
        d_btn2 = gr.Button("Demo")
    tmp=""
    def on_select2(evt: gr.SelectData):
        gr.Warning("You selected: " + str(evt.target.value))
        return [evt.value, gr.Textbox(value = evt.target.value.strip()+' ', key=1)] 
    def de_select(value:str):
        return gr.Textbox(value = value)

    textbox.select(on_select2 ,None, [statement, textbox])
    


    #d_btn.click(de_select, statement, out)
demo.launch()