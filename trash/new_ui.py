import gradio as gr 
from  utils.functions import *
from utils.dbs import *
from langchain_core.documents import BaseDocumentTransformer, Document
from typing import List
model_config_html = '''
<div style="text-align: left;">配置大模型相关的参数</div>'''

extract_highlight_html = '''
<div style="text-align: left;">抽取精彩片段</div>'''
callback = gr.CSVLogger()

def get_url_info(request: gr.Request):
    headers = request.headers
    host = request.client.host
    user_agent = request.headers["user-agent"]
    browser_host = request.headers["host"]
    print(f"request is {browser_host}")
    return {
        "ip": host,
        "user_agent": user_agent,
        "headers": headers,
        "url": browser_host
    }
gr.set_static_paths("/home/userroot/dev/CCFClip/stream")

with gr.Blocks(fill_width=True, css=".srt_file {height:80px}") as demo:
    user_name = gr.Textbox(label="input", value="zms")
    user_btn = gr.Button("Next Step", size='sm', variant="primary", min_width=1)
    user_name_post = gr.Textbox(visible=False)
    s_video = StreamVideo(visible=False)
    user_btn.click(lambda x: x, [user_name], [user_name_post])
    @gr.render(inputs=user_name_post)
    def next_step(user_name):
        if user_name != "":
            wk_data = load_workspace(user_name, db_name="ccfclip")
            if wk_data == {}:
                return gr.HTML("<h1>请先创建一个工作空间</h1>")
            llm_config = wk_data.get("llm",{})
            srt_saved_data = wk_data.get("srt",{})
            srt_prompts_data = wk_data.get("srt_prompts",{})
            #print(srt_prompts_data)
            gr.HTML(model_config_html)
            with gr.Row():
                save_workspace_btn = gr.Button("Save Workspace", size='sm', variant="primary", min_width=1)
                model_select = gr.Dropdown(["qwen2.5:72b-instruct","qwen2.5:32b-instruct","qwen2.5:7b-instruct","phi3:14b-instruct","llama3.1:70b-instruct-q2_K", "gemma2:27b-instruct-q4_0", "deepseek-v2:16b"], label="Model", value=llm_config.get("model_name",""))
                temperature = gr.Slider(minimum=0.0, maximum=1.0, step=0.1, label="Temperature", value=llm_config.get("temperature", 0.1))
                num_predict = gr.Slider(minimum=0, maximum=10000, step=1, label="Number of Predictions", value=llm_config.get("num_predict", 1024))
                keep_alives = gr.Radio([-1, 0, 100], label="Keep Alive", value=llm_config.get("keep_alive", -1))
                context_length = gr.Slider(minimum=8096, maximum=32000, step=50,label="context length", value=llm_config.get("context_num", 18000), scale=1)
            gr.HTML(extract_highlight_html)
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Row():
                        with gr.Group():
                            srt_selected = gr.Dropdown(get_file_list("srts"), label="srts List")
                            srt_load_btn = gr.Button("Load SRT", size='sm', variant="primary", min_width=2)
                            srt_file = gr.File(label="SRT File", scale=1,elem_classes=["srt_file"],file_types=['srt'])
                            db_name = gr.Textbox(label="数据库名称", value="temp_db")
                            chunks_param = gr.Slider(minimum=1, maximum=100, step=1,label="分段参数", value=95, scale=1)
                            chunks_size = gr.Slider(minimum=50, step=5, maximum=1000, label="忽略段落的大小", value=200)
                            chunks_btn = gr.Button("生成段落", size='sm', variant="primary", min_width=2)
                            
                with gr.Column(scale=5):
                    with gr.Row():
                        
                        #chunks_txt = gr.State()
                        chunks_txt_box = gr.Textbox(label="chunks txt", scale=4,max_lines=13, lines=13, value=srt_saved_data.get("chunks_txt_box", ""))
                        chunks_txt_box_len = gr.Textbox(value= len(srt_saved_data.get("chunks_txt_box", "")))
                        srt_length = gr.Textbox(label="length", scale=1,visible=True)
            with gr.Row():
                
                srt_user_prompt = gr.Textbox(value ="后面是速记稿原文：{}", scale=1,visible=False)
                srt_chunks = gr.State()
                
                srt_content = gr.Textbox(label="content", visible=False)
                srt_txt_content = gr.Textbox(label="srt txt content", scale=2, max_lines=5, visible=False)    
                #srt_chunk_content = gr.Textbox(label="srt chunk content", scale=6, max_lines=50)
            
                with gr.Column(scale=8):

                    with gr.Row():
                        d_templates = gr.Radio(["科普类", "教培类", "爱国类"], label="template", value=srt_prompts_data.get("d_templates","科普类"))
                        if srt_prompts_data.get("srt_sys_prompt","") == "":
                            srt_sys_prompt = gr.Textbox( value=load_d_templates, inputs=d_templates, visible=True,interactive=True,scale=4)
                        else:
                            print(srt_prompts_data.get("srt_sys_prompt",""))
                            srt_sys_prompt = gr.Textbox( value=srt_prompts_data.get("srt_sys_prompt",""), visible=True,interactive=True)
                        #srt_sys_prompt = gr.Textbox(scale=6)
                        with gr.Column():
                            flagging_btn = gr.Button("flagging", size='sm', variant="secondary")
                            stop_chunk = gr.Button("Stop", size='sm', variant="stop")
                            discovery_btn = gr.Button("探索精彩文本", size='sm', variant="primary", min_width=2)
                    srt_short_content = gr.Textbox(label="srt short content", scale=2, max_lines=50, value=srt_prompts_data.get("srt_short_content",""))
                    needed_edit_content = gr.Textbox(label="needed edit content", scale=2, max_lines=50)
                    #temp_txt = ""
                    send_content_btn = gr.Button("send content")
                    def on_select(value, value_2, evt:gr.SelectData):
                        global temp_txt
                        value_2 +=  evt.value + '\n'
                        #print(evt.target.value)
                        return [value_2,gr.Textbox(value=value+'  ')]
                    srt_short_content.select(on_select , [srt_short_content, needed_edit_content], [needed_edit_content,srt_short_content]).then(lambda x:x.strip(), srt_short_content, srt_short_content)
                    #needed_edit_content.change(lambda x,y:x+"\n"+y, [needed_edit_content, temp_content], needed_edit_content)
                callback.setup([srt_sys_prompt], "prompts_saved") 
                flagging_btn.click(lambda *args: callback.flag(list(args)), [srt_sys_prompt], None, preprocess=False) 
                def format_chunks(db_name, srt_txt_content, chunks_param, chunks_size):
                    docs :List[Document] = build_chunks(db_name, srt_txt_content, chunks_param)
                    #print(f"format_chunks {chunks}")
                    chunks = []
                    idx = 0
                    for doc in docs:
                        #print(f"doc is {doc}")
                        item = {"length":len(doc.page_content),"content":doc.page_content, "metadata":doc.metadata, "idx":idx}
                        if item["length"] > chunks_size:
                            chunks.append(item)
                            idx += 1
                    #gr.Warning(docs)
                    #chunks = sorted(chunks, key=lambda x:x["length"], reverse=True)
                    return "\n\n".join([chunk["content"] for chunk in chunks])
                def update_srt_files(srt_file, path="srts"):
                    srt_file_name = os.path.basename(srt_file)
                    
                    return gr.Dropdown(get_file_list(path), label="srts List", value=srt_file_name)
                srt_file.upload(fn=move_file_to,inputs=srt_file, outputs=srt_file).then(fn=gen_full_text, inputs=srt_file, outputs=[srt_length, srt_txt_content, srt_content]).then(update_srt_files, srt_file, srt_selected)
                srt_load_btn.click(gen_full_text, inputs=[srt_selected, gr.Textbox('srts',visible=False)], outputs=[srt_length, srt_txt_content, srt_content])#d_templates.change(fn=load_d_templates, inputs=[d_templates], outputs=[srt_sys_prompt])
                chunks_btn.click(fn=format_chunks, inputs=[db_name, srt_txt_content, chunks_param, chunks_size], outputs=[chunks_txt_box]).then(lambda x:len(x), chunks_txt_box, chunks_txt_box_len)
                #chunk_e = discovery_btn.click(fn=gen_full_text, inputs=srt_file, outputs=[srt_length, srt_txt_content])
                dc_e = discovery_btn.click(run_model,inputs=[srt_sys_prompt, chunks_txt_box, model_select, srt_user_prompt, temperature, context_length, keep_alives, num_predict]\
                    , outputs=srt_short_content)
                stop_chunk.click(None, None, None,cancels=dc_e)

            with gr.Row():
                top_k = gr.Slider(minimum=1, maximum=10, value=2, step=1, label="Top K")
                nice_content = gr.Textbox(label="Nice Content", value="", scale=6)

                send_content_btn.click(query_chunks, inputs=[db_name, needed_edit_content, top_k], outputs=nice_content)

            edit_area = gr.Textbox(label="Edit Area", lines=2)
            temp_area = gr.Textbox(label="Temp Area", visible=False)
            punctuation_sys_prompt = gr.Textbox(label="Punctuation System Prompt", value='''你是短视频制作博主，文章中的文字偏多，需要保留主干和幽默的句子，注意保留的句子要保持对原始文章的匹配。输出格式：
        1. 保留的句子："保留的句子"
        1. 保留的句子："保留的句子"''')
            punctuation_user_prompt = gr.Textbox(label="Punctuation User Prompt", value="后面是文章：{}")
            punctuation_btn = gr.Button("Add Punctuation")
            stop_punc_btn = gr.Button("Stop Punctuation")
            p_e = punctuation_btn.click(run_model, [punctuation_sys_prompt, nice_content, model_select, punctuation_user_prompt, temperature, context_length, keep_alives, num_predict], edit_area)
            stop_punc_btn.click(None,None, None,cancels=p_e)# def on_select(value, e:gr.SelectData):
    #     return e.value
        # edit_area.select(on_select , out_put_2, temp_area)
            with gr.Row():
                with gr.Column():
                    fuzz_param = gr.Slider(0, 100, value=70, step=1, label="Fuzz Param")
                    with gr.Row():
                        find_srt_btn = gr.Button("定位到视频时间轴")
                        invert_srt_text = gr.Textbox(label="精彩视频时间轴",scale=4)
                    gen_marketing_btn = gr.Button("生成营销文案")
                    marketing_style = gr.Dropdown(choices=["小红书","微信视频号", "抖音", "快手"], value="小红书")
                    marketing_prompt = gr.Textbox(label="营销文案提示词", value = f"输出{marketing_style.value}风格的营销标题和文案，字数不要超过100字",scale=2)
                    marketing_style.change(lambda x:f"输出{x}风格的营销标题和文案，字数不要超过100字", marketing_style, marketing_prompt)
                    
                    marketing_text = gr.Textbox(label="精彩营销文案")
                    marketing_user_prompt = gr.Textbox(value="{}")
                    gen_marketing_btn.click(run_model, inputs=[marketing_prompt,edit_area, model_select,  marketing_user_prompt], outputs=[marketing_text])

                        
                    find_srt_btn.click(fn=invert_find, inputs=[edit_area, srt_content, fuzz_param], outputs=invert_srt_text)
                with gr.Column():
                    video_selected = gr.Dropdown(get_file_list("video"), label="Video List")
                    clips_btn = gr.Button("生成预览视频")
                    s_video = StreamVideo()
                    clips_btn.click(fn=gen_prev_video, inputs=[invert_srt_text, video_selected], outputs=s_video)
                    download_btn = gr.Button("生成下载视频")
                    d_video = gr.File()
                    download_btn.click(fn=gen_download_video, inputs=[invert_srt_text, video_selected], outputs=d_video)

                def save_workspace(model_select, temperature, context_length,  keep_alives, num_predict,
                                                                    srt_file, db_name, chunks_param, chunks_size,
                                                                      chunks_txt_box,
                                                                      d_templates, srt_sys_prompt, srt_short_content, needed_edit_content,
                                                                      punctuation_sys_prompt,punctuation_user_prompt):
                    workspace = {"wk_name":"zms"}
                    model_config ={"llm": 
                                   {"model_name":model_select, "temperature":temperature, "context_length":context_length, 
                                    "keep_alives":keep_alives, "num_predict":num_predict}}
                    srt_config ={"srt": 
                                 {"srt_file":srt_file, "vector_db_name":db_name, "chunks_param" : chunks_param, "chunks_size":chunks_size,
                                  "chunks_txt_box":chunks_txt_box, } }
                    srt_prompts_data = {"srt_prompts":{"d_templates":d_templates, "srt_sys_prompt":srt_sys_prompt, "needed_edit_content":needed_edit_content, "srt_short_content":srt_short_content}}
                
                    punc_prompts_data = {"punc_prompts":{"punctuation_sys_prompt":punctuation_sys_prompt, "punctuation_user_prompt":punctuation_user_prompt}}
                    insert_workspace({**workspace,**model_config, **srt_config, **srt_prompts_data, **punc_prompts_data}, "ccfclip")
                
                save_workspace_btn.click(fn=save_workspace, inputs=[model_select, temperature, context_length,  keep_alives, num_predict,
                                                                    srt_file, db_name, chunks_param, chunks_size,
                                                                      chunks_txt_box, 
                                                                      d_templates, srt_sys_prompt, srt_short_content, needed_edit_content,
                                                                      punctuation_sys_prompt,punctuation_user_prompt
                                                                      ], outputs = None)
demo.launch(server_name='0.0.0.0')