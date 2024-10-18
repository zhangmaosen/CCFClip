import gradio as gr

from utils.personal_workspace import *
from utils.functions import *
from utils.dbs import *
from typing import List
from funasr import AutoModel
from utils.subtitle_utils import *

extract_nice_content_prompts = {
    "Prompt模板1 提取优秀案例或者主题":'''
你是一名科普类短视频博主，你的主要观众在小红书。你需要从科技类演讲的速记稿中寻找适合做科普短视频的案例和包含案例的连续文字。你需要认真学习下面的文字示例：

适合做科普短视频的文字示例1：
* 捕捉“墨子号”卫星上发出的光子难度有多大呢？举一个例子，相当于我坐在飞机上，拿着硬币一个个往下扔，要扔到地面的一个储蓄罐里，储蓄罐有很细的投币口，硬币还得投进去才行——我们做到了。
文字示例1故事情节完整度10分、画面感10分和细节描述连贯10分和通俗程度10分，科学原理的通俗解释10分，以文字示例1为对应的打分标准

适合做科普短视频的文字示例2：
* 为什么电影里的黑洞看起来的是亮的，首先是距离的原因，其次是光线会绕着黑洞绕几圈再进去，有些光线会掉进黑洞，而有些会逃出来，这部分逃出来的光子就是电影中所看到的“黑洞的光”。为什么需要高速自转的黑洞，《星际穿越》的黑洞必须同时具有1亿倍的太阳质量和高速的自转，才能产生1小时=7年的效果，而且宇航员不被黑洞的潮汐力所撕碎。这是导演和科学妥协的结果。
文字示例2对科学原理进行了通俗的解释，加10分，以文字示例2为对应的打分标准

你需要对速记稿中的每一个案例内容进行仔细打分，得分点如下：
1. 故事情节的完整程度加口语化程度，加0到10分
3. 激发读者的画面感的生动程度，加0到10分
4. 细节动作描写的连贯程度，加0到10分
5. 文字中提到日常工作生活会用到的物品的流行程度或者是与我们生活中的联系紧密程度，加0到10分
6. 问题解决前后对比的差异程度，加0-10分
7. 将枯燥的研究过程的简化为通俗故事的程度，加0-10分
8. 对基础概念的通俗解释让读者能够理解的程度，加0-10分
9. 复杂的数学公式和科学专有名词越多减分越多，减0-10分

打分过程示例：
1. 算出每个打分点的得分，比如：得分点1 = 3分， 得分点2 = 2分， 得分点9 = -5分
2. 汇总上一步给出的每个打分点的得分，需要列出算式，算式把所有得分点加和，比如：得分点1的3分 + 得分点2的2分 + 得分点9 的-5分 = 3 + 2 + (-5) = 0分
你需要一步一步的思考如何完成工作，找出符合需求的7个案例，注意要严格按照得分点进行打分，你是严格的评审官，你要直率和严格的输出得分评价。注意每个案例要独立打分。注意列出算式
输出的格式如下：
1. 案例：[案例的核心内容]，得分点[得分]， 最后得分：[汇总得分]，
1. 案例：[案例的核心内容]，得分点[得分]，最后得分： [汇总得分]，
''',
    "提取金句":""
}

extract_key_sentence_prompts = {
    "Prompt模板2 关键句子提取":'''
你是一名短视频脚本编辑，你的工作是从文本内容中找到适合作为短视频脚本的主干句子和精辟的句子并输出，注意输出的内容需要保持对过程描述的完整性，注意要原样输出找到的句子。输出格式：
* "输出"
...
* "输出"'''
}
funasr_model = AutoModel(model="iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
                                vad_model="damo/speech_fsmn_vad_zh-cn-16k-common-pytorch",
                                punc_model="damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
                                spk_model="damo/speech_campplus_sv_zh-cn_16k-common",
                                disable_update=True
                                )
workspaces_list = gr.Dropdown(label="Select Workspace", choices=get_workspace_names(), value=None, interactive=True, scale=2)
gr.set_static_paths("/home/userroot/dev/CCFClip/stream")
# for video and srt upload 
video_upload = gr.File(label="Upload Video File", file_types=['.mp4'])
srt_upload = gr.File(label="Upload SRT File", file_types=['.srt'])
# videos_uploaded = gr.Dropdown(label="Uploaded Videos", interactive=True, scale=2)
# srt_uploaded = gr.Dropdown(label="Uploaded SRT", interactive=True, scale=2)
# for llm
llm_model_select = gr.Dropdown(["qwen2.5:72b-instruct","qwen2.5:32b-instruct","qwen2.5:7b-instruct"], label="Model", value="qwen2.5:32b-instruct")
llm_model_temperature = gr.Slider(minimum=0, maximum=1, step=0.1, label="Temperature")
llm_model_context_num = gr.Slider(minimum=8096*3, maximum=8096*4, step=1, label="Number of Context")
ollama_predict_num = gr.Slider(minimum=768*2, maximum=4096, step=64, label="Number of Predictions")
ollama_keep_alive = gr.Radio(choices=[0,-1], value=-1, label="Keep Alive Forever")

# for srt file and build chunks and index
chunk_similarity_input = gr.Slider(value = 95, minimum=50, maximum=100, step=5, label="Similarity Threshold")
chunk_size_input = gr.Slider(value = 200, minimum=50, maximum=400, step=10, label="Chunk Size")
chunk_btn = gr.Button(value="Format SRT to LLM Chunks")
srt_file = gr.FileExplorer(label="SRT File", glob="*.srt", root_dir='srts', file_count="single", height=390, scale=2)

srt_chunks_output = gr.Textbox(label="Chunks", max_lines=10)
chunk_length_output = gr.Textbox(label="Chunk Length")

nice_extract_prompt_input = gr.Textbox(label="Prompt for Extracting Nice Content", scale=3)
nice_extract_btn = gr.Button("Extract Nice Content")
nice_extract_stop_btn = gr.Button("Stop")
nice_content_output = gr.Textbox(label="Nice Content")

selected_contents_output = gr.Textbox(label="Selected Contents", scale=4)
query_chunks_topN_input = gr.Slider(value=1, minimum=1, maximum=3, step=1, label="Top N")
matched_chunks_btn = gr.Button('Find Matched Chunks')
matched_chunks_output = gr.Textbox(label="Matched Chunks")

key_sentence_prompt_input = gr.Textbox(label="Prompt for Extracting Key Sentences", scale=4)
key_sentence_extract_btn = gr.Button("Extract Key Sentences")
key_sentence_extracted_output = gr.Textbox(label="Key Sentences", scale=4)

user_prompt_input = gr.Textbox(label="User Prompt", value= "{}", visible=False)

matched_srt_output = gr.Textbox(label="Matched SRT Text")
find_matched_srt_btn = gr.Button("Find Matched SRT Text")
fuzzy_search_param = gr.Slider(value = 70, minimum = 50, maximum = 100, step = 10, label="Fuzzy Search Param")

gen_marketing_btn = gr.Button("生成营销文案")
marketing_style = gr.Dropdown(choices=["小红书","微信视频号", "抖音", "快手"], value="小红书", interactive=True)
marketing_prompt = gr.Textbox(label="营销文案提示词", value = lambda x: f"输出{x}风格的营销标题和文案，字数不要超过100字", inputs= marketing_style, scale=2)
marketing_output = gr.Textbox(label="Marketing Text")

video_file_explorer = gr.FileExplorer(label="Video File", glob="*.mp4", root_dir='video', file_count="single", height=390)
def load_workspace(worksapce_name):
    print(f'workspace_name is {worksapce_name}')
    if worksapce_name == []:
         name = ""
         time = ""
         data = [{}]
    else:
        name = worksapce_name.split(' ')[0]
        time = worksapce_name.split(' ')[-1]
        data = get_workspace_by_name_ts(name, time)
    if len(data) > 0:
        #print(f'data is {data}')
        srt_chunk = data[0].get("srt_chunk","")
        extract_prompt = data[0].get("extract_prompt","")
        key_sentence_prompt = data[0].get("key_sentence_prompt","")
        srt_sub_content = data[0].get("srt_sub", "")
        return [data[0], srt_sub_content, srt_chunk, extract_prompt, key_sentence_prompt]
    
    #return {'data':data}

def save_workspace(workspace_input,
                   srt_chunk, 
                   srt_sub_content,
                   nice_extract_prompt_input,
                   key_sentence_prompt_input,
                   workspace):
    print(f"workspace is {workspace} \n workspace_input is {workspace_input}")
    if len(workspace_input) > 0:
        data = {**workspace, "name": workspace_input, "srt_chunk":srt_chunk, "srt_sub": srt_sub_content, "extract_prompt":nice_extract_prompt_input, "key_sentence_prompt":key_sentence_prompt_input}
    else:
        data = {**workspace, "srt_chunk":srt_chunk, "srt_sub": srt_sub_content, "extract_prompt":nice_extract_prompt_input, "key_sentence_prompt":key_sentence_prompt_input}

    print(f'data is {data}')
    data = save_workspace_data(data)
    return data
    
def create_srt_file_name_pinyin(file_name):
    if file_name is None:
        return ""
    file_name = os.path.basename(file_name).split(".")[0]
    file_name_pinyin = translate_filename_to_pinyin(file_name)
    file_name_pinyin = ''.join(filter(str.isalnum, file_name_pinyin))
    # 截断file_name_pinyin 不要超过30个字符 不要小于3个字符
    file_name_pinyin = file_name_pinyin[:63] if len(file_name_pinyin) > 63 else file_name_pinyin
    # 如果file_name_pinyin 的长度小于3，则使用_补全
    file_name_pinyin = file_name_pinyin if len(file_name_pinyin) >= 3 else file_name_pinyin + "a"*(3-len(file_name_pinyin))
    
    # 把file_name_pinyin中的_字符替换为1
    file_name_pinyin = file_name_pinyin.replace("_","1")
    print(f"file_name_pinyin is {file_name_pinyin} ")
    return file_name_pinyin
def format_chunks(db_name, srt_txt_content, chunks_param, chunks_size):

    docs :List[Document] = build_chunks(db_name, srt_txt_content, chunks_param)
    print(f"format_chunks {db_name}")
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

def on_select(value, value_2, evt:gr.SelectData):
                        global temp_txt
                        value_2 +=  evt.value + '\n'
                        #print(evt.target.value)
                        return [gr.Textbox(value=value+'  '), value_2]

def generate_srt_file(video_file):
    input_file_name = os.path.basename(video_file)
    input_file_name_without_ext = os.path.splitext(input_file_name)[0]
    output_file = f"./wav/{input_file_name_without_ext}.wav"
    try:
        (
            ffmpeg
            .input(video_file)
            .output(output_file, format='wav')
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
    rec_result = funasr_model.generate(input=output_file)
    srt = generate_srt(rec_result[0]['sentence_info'])
    #write srt content to file
    with open(f"./srts/{input_file_name_without_ext}.srt", "w", encoding='utf-8') as file:
        file.write(srt)
    return f"./srts/{input_file_name_without_ext}.srt"

with gr.Blocks() as demo:
    srt_sub_content = gr.State("")
    srt_chunks_content = gr.State("")
    srt_file_name_pinyin = gr.State("")
    workspace_data = gr.State({})
    current_workspace_name = gr.State('')
    demo.load(lambda : gr.Dropdown( choices= get_workspace_names()), None, workspaces_list)
    gr.Markdown(value='''
                第一步：     
                     
                1. 新建你的工作名称用来保存你的工作，工作名只能是英文并且需要大于3个字母
                2. 或者从下拉框中选择已经保存的工作，继续开始工作
                3. 可以从下拉框中选择template，这样会默认使用template中的prompt
                4. 遇到任何问题请在 https://github.com/zhangmaosen/CCFClip/issues 提交问题，我会尽快解答
'''
    )
    with gr.Row():
        with gr.Column(scale=2):
            with gr.Row():
                workspace_input = gr.Textbox(label="Workspace Name", scale=2)
                save_workspace_btn = gr.Button("Create or Save Workspace", variant="primary", size='lg')
                workspaces_list.render()
                                #load_workspace_btn = gr.Button("Load Workspace")
                
        with gr.Column():
            with gr.Row():
                
                create_workspace_button = gr.Button("Create Workspace", scale=1, visible=False)
                
    current_data = gr.Textbox(label="Workspace Data", inputs= workspace_data, value=lambda x:x, visible=False)
    current_name = gr.Textbox(label="Workspace Name", inputs= current_workspace_name, value=lambda x:x, visible=False) 

    workspaces_list.change(load_workspace, inputs=[workspaces_list], outputs=[workspace_data, 
                                                                              srt_sub_content,
                                                                              srt_chunks_output, 
                                                                              nice_extract_prompt_input,
                                                                              key_sentence_prompt_input])\
    .then(lambda x: x.get("name",""), inputs=[workspace_data], outputs=current_workspace_name)
    
    create_workspace_button.click(create_workspace_by_name, inputs=[workspace_input], outputs=[workspace_data])\
        .then(lambda : gr.Dropdown(label="Select Workspace", choices=get_workspace_names(), interactive=True), None, workspaces_list)\
        .then(lambda x:x['name'] + ' at ' + x['time'], workspace_data, workspaces_list)
    
    save_workspace_btn.click(save_workspace, inputs=[workspace_input, srt_chunks_output, srt_sub_content, nice_extract_prompt_input, key_sentence_prompt_input, workspace_data], outputs=[workspace_data])\
        .then(lambda : gr.Dropdown(label="Select Workspace", choices=get_workspace_names(), interactive=True), None, workspaces_list)\
        .then(lambda x:x['name'] + ' at ' + x['time'], workspace_data, workspaces_list)
    
    #load_workspace_btn.click(load_workspace, inputs=[workspaces_list], outputs=[workspace_data])
    gr.Markdown(value='''
                第二步：     
                     
                1. 点击查看你的视频文件和视频字幕文件是否已上传，如果没有请点击上传
'''
    )
    with gr.Accordion("Upload new video or srt file", open=False):
        with gr.Row():
            # def refresh_srt_file_list(idx=""):
            #     names = get_file_list("srts")
            #     if idx == "":
            #         value = names[0] if len(names) > 0 else ""
            #     else :
            #         value = os.path.basename(idx)
            #     return gr.Dropdown(choices=names, label="Select SRT File", value=value, interactive=True)
            
            def refresh_video_file_list(idx=""):
                names = get_file_list("video")
                if idx == "":
                    value = names[0] if len(names) > 0 else ""
                else :
                    value = os.path.basename(idx)
                return gr.Dropdown(choices=names, label="Select SRT File", value=value, interactive=True)
            
            video_upload.render()
            video_files = gr.FileExplorer(root_dir="video", file_count="single", height=500,scale=3)
            gen_srt_btn = gr.Button("Generate SRT File")
            srt_files = gr.FileExplorer(root_dir="srts", file_count="single", height=500, scale=3)
            
            
            srt_upload.render()
            
            gen_srt_btn.click(generate_srt_file, video_files, srt_files).then(
                lambda : gr.FileExplorer(root_dir="./", height=500,scale=3),None, srt_files
            ).then(
                lambda : gr.FileExplorer(root_dir="srts", height=500,scale=3),None, srt_files
            ).then(
                lambda : gr.FileExplorer(label="SRT File", glob="*.srt", root_dir='./', file_count="single", height=390, scale=2),None, srt_file
            ).then(
                lambda : gr.FileExplorer(label="SRT File", glob="*.srt", root_dir='srts', file_count="single", height=390, scale=2),None, srt_file
            )
            
            
            srt_upload.upload(move_file_to, inputs=[srt_upload, gr.State("srts")], outputs=[]).then(
                lambda : gr.FileExplorer(root_dir="./", height=500,scale=3),None, srt_files
            ).then(
                lambda : gr.FileExplorer(root_dir="srts", file_count="single", height=500,scale=3),None, srt_files
            ).then(
                lambda : gr.FileExplorer(label="SRT File", glob="*.srt", root_dir='./', file_count="single", height=390, scale=2),None, srt_file
            ).then(
                lambda : gr.FileExplorer(label="SRT File", glob="*.srt", root_dir='srts', file_count="single", height=390, scale=2),None, srt_file
            )
            
            video_upload.upload(move_file_to, inputs=[video_upload, gr.State("video")], outputs=[]).then(
                lambda : gr.FileExplorer(root_dir="./", height=500,scale=3),None, video_files
            ).then(
                lambda : gr.FileExplorer(root_dir="video", file_count="single", height=500,scale=3),None, video_files
            ).then(
                 lambda : gr.FileExplorer(label="Video File", glob="*.mp4", root_dir='./', file_count="single", height=390),None, video_file_explorer
            ).then(
                 lambda : gr.FileExplorer(label="Video File", glob="*.mp4", root_dir='video', file_count="single", height=390),None, video_file_explorer
            )
    gr.Markdown(value='''
                第三步：     
                     
                1. 选择你要处理的字幕文件，点击格式化按钮，将字幕文件格式化为可以输入LLM的格式，字幕文件会根据字幕的相似度进行合并，合并后的字幕文件会显示在右侧
                '''
    )
    with gr.Row():
        srt_file.render()
        with gr.Column(scale=3):
            with gr.Row():
                chunk_length_output.render()
                chunk_similarity_input.render()
                chunk_size_input.render()
                chunk_btn.render()
            #srt_chunks_content.render()
            srt_chunks_output.render()
            #srt_sub_content.render()

    srt_file.change(load_text_from_srt, inputs=[srt_file], outputs=[srt_chunks_content, srt_sub_content])\
    .then(create_srt_file_name_pinyin, srt_file, srt_file_name_pinyin)\
    .then(lambda : "", None, srt_chunks_output)
    
    chunk_btn.click(format_chunks, inputs=[srt_file_name_pinyin, srt_chunks_content, chunk_similarity_input, chunk_size_input], outputs=[srt_chunks_output])
    srt_chunks_output.change(lambda x: len(x), srt_chunks_output, chunk_length_output)
    gr.Markdown(value='''
                第四步：     
                     
                1. 选择一个合适的大模型，输入你的prompt，点击提取按钮，模型会根据你的prompt和字幕内容提取出精彩内容，提取后的结果会显示在下方
                2. 注意大模型的参数越多，性能越慢，请按需选择
                3. 从大模型生成的内容文本框中，找到你认为可以作为精彩短视频使用的文字内容，例如：
                "案例：xxxxx"
                4. 在内容文本框中用鼠标高亮选择你认可的文字内容， 可以多次选择，每次高亮选择的文字都会自动输出到下一步的文本框中备用
                '''
    )
    with gr.Row():
        with gr.Accordion("LLM Config Details", open=True):
            with gr.Row():
                llm_model_select.render()
                llm_model_temperature.render()
                llm_model_context_num.render()
                ollama_predict_num.render()
                ollama_keep_alive.render()
        with gr.Column(scale=7):
            with gr.Row():
                user_prompt_input.render()
                #nice_extract_prompt_examples.render()\
                with gr.Column(scale=4):
                    nice_extract_prompt_examples = gr.Examples(["Prompt模板1 提取优秀案例或者主题"], inputs=gr.Textbox(visible=False), fn=lambda x:extract_nice_content_prompts[x], outputs=nice_extract_prompt_input, run_on_click=True)

                    nice_extract_prompt_input.render()
                    with gr.Row():
                        nice_extract_btn.render()  
                        nice_extract_stop_btn.render()
            with gr.Row():
                nice_content_output.render()
        
    
    
    
    
    click_e = nice_extract_btn.click(run_model,inputs=[nice_extract_prompt_input, 
                                             srt_chunks_output, 
                                             llm_model_select, 
                                             user_prompt_input,
                                             llm_model_temperature, 
                                             llm_model_context_num, 
                                             ollama_keep_alive,
                                             ollama_predict_num
                                             ], outputs=nice_content_output)
    nice_extract_stop_btn.click(None, None, None, cancels=[click_e])
        
    nice_content_output.select(on_select, inputs=[nice_content_output, selected_contents_output], outputs=[nice_content_output, selected_contents_output])\
    .then(lambda x:x.strip(), nice_content_output, nice_content_output)
    
    
    gr.Markdown(value='''
                第五步：     
                1.  第四步中你选择的精彩主题或者案例描述已经自动加载到下面的文本框中，你可以进行修改或者不修改，目的是让AI能够根据这个描述从字幕全文中找到最合适的原文片段     
                
                2.  点击Find按钮，将生成合适的原文片段， Top N参数框用来控制找到的内容范围，N越大，AI会找到越多的相关内容
                ''')
    with gr.Row():
        selected_contents_output.render()
        query_chunks_topN_input.render()
        matched_chunks_btn.render()
    matched_chunks_output.render()
    

    matched_chunks_btn.click(query_chunks, inputs=[srt_chunks_output, srt_file_name_pinyin, selected_contents_output, query_chunks_topN_input], outputs=[matched_chunks_output])

    
    gr.Markdown(value='''
第六步：     
                1. 在prompt文本框中输入合适的内容，目的是让AI从原文中提取出最合适的句子，例如："xxxx"，"yyyy"，"zzzz"，    
                2. 点击提取关键句子按钮     
                3. 点击Find Matched SRT 按钮，AI会根据你的关键句子，从字幕全文中定位出最合适的字幕时间戳，用于后面从长视频中裁剪出短视频
                ''')
    with gr.Row():
        example_key_sentence_prompt_input = gr.Examples(["Prompt模板2 关键句子提取"], inputs=gr.Textbox(visible=False), fn=lambda x:extract_key_sentence_prompts[x], outputs=key_sentence_prompt_input, run_on_click=True)
        key_sentence_prompt_input.render()
        key_sentence_extract_btn.render()
    with gr.Row():
        key_sentence_extracted_output.render()
        fuzzy_search_param.render()
        find_matched_srt_btn.render()
    key_sentence_extract_btn.click(run_model,inputs=[key_sentence_prompt_input, 
                                             matched_chunks_output, 
                                             llm_model_select, 
                                             user_prompt_input,
                                             llm_model_temperature, 
                                             llm_model_context_num, 
                                             ollama_keep_alive,
                                             ollama_predict_num,
    ], outputs=key_sentence_extracted_output)

    matched_srt_output.render()
    
    
    
    find_matched_srt_btn.click(create_srt_file_name_pinyin, srt_file, srt_file_name_pinyin)\
    .then(load_text_from_srt, inputs=[srt_file], outputs=[srt_chunks_content, srt_sub_content])\
    .then(invert_find, inputs=[key_sentence_extracted_output, srt_sub_content, fuzzy_search_param], outputs=matched_srt_output)
    
    gr.Markdown(value='''
第七步：     
                1. 选择不同的平台，让AI生成不同风格的营销文案    
                2. 选择需要裁剪的长视频文件名称    
                3. 点击预览，将会根据第六步输出的时间戳从长视频中裁剪出短视频，如果长视频是h265格式，裁剪的过程可能会很慢需要耐心等待    
                4. 如果预览视频内容满足你的要求，点击生成下载视频，将生成高清晰度的短视频供下载，如果长视频是h265格式，生成过程可能会很慢需要耐心等待    
                ''')
    with gr.Row():
        with gr.Column():
            with gr.Row():
                marketing_style.render()
                marketing_prompt.render()
            gen_marketing_btn.render()
            marketing_output.render()
            
            gen_marketing_btn.click(run_model,inputs=[marketing_prompt, 
                                             key_sentence_extracted_output, 
                                             llm_model_select, 
                                             user_prompt_input,
                                             llm_model_temperature, 
                                             llm_model_context_num, 
                                             ollama_keep_alive,
                                             ollama_predict_num
   ], outputs=marketing_output)
            
        with gr.Column():
            video_file_explorer.render()
            s_video = StreamVideo()
            #video_selected = gr.Dropdown(get_file_list("video"), label="Video List")
            clips_btn = gr.Button("生成预览视频")
            clips_btn.click(fn=gen_prev_video, inputs=[matched_srt_output, video_file_explorer], outputs=s_video)
            download_btn = gr.Button("生成下载视频")
            d_video = gr.File()
            download_btn.click(fn=gen_download_video, inputs=[matched_srt_output, video_file_explorer], outputs=d_video)
    
demo.launch(server_name='0.0.0.0', server_port=7777)