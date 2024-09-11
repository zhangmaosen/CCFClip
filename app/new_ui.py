import gradio as gr 
from  utils.functions import *

model_config_html = '''
<div style="text-align: left;">配置大模型相关的参数</div>'''

extract_highlight_html = '''
<div style="text-align: left;">抽取精彩片段</div>'''
callback = gr.CSVLogger()
gr.set_static_paths("/home/userroot/dev/CCFClip/stream")
with gr.Blocks() as demo:
    with gr.Row():
        srt_file = gr.File(label="SRT File", scale=1, file_types=['srt'])
        open_srt_file = gr.Button("Open", size='sm', variant="primary")
        
        srt_length = gr.Textbox(label="length", scale=1)
        srt_txt_content = gr.Textbox(label="srt txt content", scale=6, max_lines=10)
        srt_content = gr.Textbox(label="srt file content", scale=6, max_lines=10, visible=True)
        open_srt_file.click(fn=gen_full_text, inputs=srt_file, outputs=[srt_length, srt_txt_content, srt_content])
    gr.HTML(model_config_html)
    with gr.Row():
        model_select = gr.Dropdown(["qwen2:72b-instruct","qwen2:7b-instruct","phi3:14b-instruct","llama3.1:70b-instruct-q2_K", "gemma2:27b-instruct-q4_0", "deepseek-v2:16b"], label="Model", value="qwen2:72b-instruct")
        temperature = gr.Slider(minimum=0.0, maximum=1.0, step=0.1, label="Temperature", value=0.1)
        num_predict = gr.Slider(minimum=0, maximum=1000, step=1, label="Number of Predictions", value=768)
        keep_alives = gr.Radio([-1, 0, 100], label="Keep Alive", value=-1)
        context_length = gr.Slider(minimum=8096, maximum=32000, step=50,label="context length", value=32000, scale=1)
    gr.HTML(extract_highlight_html)


    with gr.Row():
        with gr.Column(scale=1):
            like_people = gr.Textbox(label="like People", value="科技人士")
            gr.Examples([["科技编辑"], ["大数据工程师"], ["大学生"]], like_people)
        with gr.Column(scale=1):
            target_people = gr.Textbox(label="Target People", value="CEO")
            gr.Examples([["男性CEO"], ["女性"], ["宝妈"]], target_people)
        with gr.Column(scale=1):
            style = gr.Textbox(label="Target style", value = '小红书')
            gr.Examples([["小红书"], ["腾讯视频号"], ["知乎"]], style)
        

    with gr.Row():
        with gr.Column():
            gen_sys_prompt_key_words_btn = gr.Button("生成系统提示")
            sys_prompt_keywords = gr.Textbox(label="System Prompt")
            user_prompt_keywords = gr.Textbox(label="User Prompt", value="后面是速记稿内容：\n")
            gen_sys_prompt_key_words_btn.click(fn=gen_key_words, inputs=[target_people, like_people], outputs=sys_prompt_keywords)

        with gr.Column(scale=2):
            with gr.Row():
                go_btn = gr.Button("Go", variant="primary", size="sm")
                stop_btn = gr.Button("Stop",variant="stop", size="sm")
        
            out_put = gr.Textbox(label="Output",  scale=4, lines=15, max_lines=30)
            go_event = go_btn.click(fn=run_model, inputs=[sys_prompt_keywords, srt_txt_content, model_select, user_prompt_keywords, temperature, context_length, keep_alives, num_predict], outputs=out_put)
            stop_btn.click(None, None, None, cancels=go_event)
    with gr.Row():
        with gr.Column(scale=1):
            key_words = gr.Textbox(label="key words", value = "")
            gr.Examples([["顶流"], ["最佳"], ["第一"]], key_words)
        with gr.Column(scale=1):
            topics = gr.Textbox(label="topics", value = "")
            gr.Examples([["顶流"], ["最佳"], ["第一"]], topics)
    with gr.Row():
        
        with gr.Column():
            gen_sys_prompt_btn = gr.Button("生成系统提示")
            sys_prompt = gr.Textbox(label="System Prompt")
            user_prompt = gr.Textbox(label="User Prompt", value="后面是速记稿内容：\n")
            
            gen_sys_prompt_btn.click(fn=gen_system_prompt, inputs=[target_people, like_people, style, key_words,topics ], outputs=sys_prompt)
            flagging_btn = gr.Button("Flagging", variant="primary")
        with gr.Column(scale=2):
            with gr.Row():
                go_btn = gr.Button("Go", variant="primary", size="sm")
                stop_btn = gr.Button("Stop",variant="stop", size="sm")
                to_edit_btn = gr.Button("to next Edit", variant="secondary", size="sm")
            out_put_2 = gr.Textbox(label="Output",  scale=4, lines=15, max_lines=30)
            #out_put = gr.Textbox(label="Output",  scale=4, lines=15, max_lines=30)
            go_event = go_btn.click(fn=run_model, inputs=[sys_prompt, srt_txt_content, model_select, user_prompt, temperature, context_length, keep_alives, num_predict], outputs=out_put_2)
            stop_btn.click(None, None, None, cancels=go_event)
        callback.setup([sys_prompt_keywords, sys_prompt, user_prompt, model_select, out_put_2,srt_file], "flagged_prompts") 
        flagging_btn.click(lambda *args: callback.flag(list(args)), [sys_prompt_keywords, sys_prompt, user_prompt, out_put_2,srt_file], None, preprocess=False) 

    edit_area = gr.Textbox(label="Edit Area", lines=2)
    temp_area = gr.Textbox(label="Temp Area", visible=False)
    to_edit_btn.click(lambda t,e:e+f"\n“{t}”", [temp_area, edit_area], edit_area)
    def on_select(value, e:gr.SelectData):
        return e.value
    out_put_2.select(on_select , out_put_2, temp_area)
    with gr.Row():
        with gr.Column():
            fuzz_param = gr.Slider(0, 100, value=70, step=1, label="Fuzz Param")
            with gr.Row():
                find_srt_btn = gr.Button("定位到视频时间轴")
                gen_marketing_btn = gr.Button("生成营销文案")
                marketing_style = gr.Dropdown(choices=["小红书","微信视频号", "抖音", "快手"], value="小红书")
                marketing_prompt = gr.Textbox(label="营销文案提示词", value = f"输出{marketing_style.value}风格的营销标题和文案，字数不要超过100字",scale=2)
                marketing_style.change(lambda x:f"输出{x}风格的营销标题和文案，字数不要超过100字", marketing_style, marketing_prompt)
                
            marketing_text = gr.Textbox(label="精彩营销文案")
            gen_marketing_btn.click(run_model, inputs=[marketing_prompt,edit_area, model_select,  user_prompt], outputs=[marketing_text])

            invert_srt_text = gr.Textbox(label="精彩视频时间轴")
            find_srt_btn.click(fn=invert_find, inputs=[edit_area, srt_content, fuzz_param], outputs=invert_srt_text)
        with gr.Column():
            video_selected = gr.Dropdown(get_file_list("video"), label="Video List")
            clips_btn = gr.Button("生成预览视频")
            s_video = StreamVideo()
            clips_btn.click(fn=gen_prev_video, inputs=[invert_srt_text, video_selected], outputs=s_video)
            download_btn = gr.Button("生成下载视频")
            d_video = gr.File()
            download_btn.click(fn=gen_download_video, inputs=[invert_srt_text, video_selected], outputs=d_video)
            
demo.launch()