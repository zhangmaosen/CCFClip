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
        #gr.Warning("You selected: " + str(evt.target.value))
        return [evt.value, gr.Textbox(value = evt.target.value.strip()+' ', key=1)] 
    def de_select(value:str):
        return gr.Textbox(value = value)

    textbox.select(on_select2 ,None, [statement, textbox])
    txt = 'sdfsfs'
    @gr.render(inputs=statement)
    def render_text(text):
        m = gr.State("sdfs")
        i = gr.Textbox(value="text")
        l = gr.Textbox()
        def test(txt):
            gr.Warning("change !!")
        i.change(test, inputs= i, outputs=l)
        
    t_file = gr.Textbox()
    u_file = gr.File()
    t_file.change(lambda x:x, inputs=t_file, outputs=u_file)
    #d_btn.click(de_select, statement, out)
demo.launch()