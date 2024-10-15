import gradio as gr

from utils.personal_workspace import *
from utils.functions import *
from utils.dbs import *
from typing import List

workspaces_list = gr.Dropdown(label="Select Workspace", choices=get_workspace_names(), interactive=True, scale=2)

# for llm
llm_model_select = gr.Dropdown(["qwen2.5:72b-instruct","qwen2.5:32b-instruct","qwen2.5:7b-instruct","phi3:14b-instruct","llama3.1:70b-instruct-q2_K", "gemma2:27b-instruct-q4_0", "deepseek-v2:16b"], label="Model", value="qwen2.5:7b-instruct")
llm_model_temperature = gr.Slider(minimum=0, maximum=1, step=0.1, label="Temperature")
llm_model_context_num = gr.Slider(minimum=8096, maximum=8096*3, step=1, label="Number of Context")
ollama_predict_num = gr.Slider(minimum=768, maximum=4096, step=64, label="Number of Predictions")
ollama_keep_alive = gr.Radio(choices=[0,-1], value=-1, label="Keep Alive Forever")

# for srt file and build chunks and index
chunk_similarity_input = gr.Slider(minimum=50, maximum=100, step=5, label="Similarity Threshold")
chunk_size_input = gr.Slider(minimum=50, maximum=400, step=10, label="Chunk Size")
chunk_btn = gr.Button()
srt_file = gr.File(label="SRT File", file_types=['.srt'])
srt_chunks_output = gr.Textbox(label="Chunks")
chunk_length_output = gr.Textbox(label="Chunk Length")

nice_extract_prompt_input = gr.Textbox(label="Prompt for Extracting Nice Content")
nice_extract_btn = gr.Button("Extract Nice Content")
nice_extract_stop_btn = gr.Button("Stop")
nice_content_output = gr.Textbox(label="Nice Content")

selected_contents_output = gr.Textbox(label="Selected Contents")
query_chunks_topN_input = gr.Slider(value=1, minimum=1, maximum=3, step=1, label="Top N")
matched_chunks_btn = gr.Button('Find Matched Chunks')
matched_chunks_output = gr.Textbox(label="Matched Chunks")

key_sentence_prompt_input = gr.Textbox(label="Prompt for Extracting Key Sentences")
key_sentence_extract_btn = gr.Button("Extract Key Sentences")
key_sentence_extracted_output = gr.Textbox(label="Key Sentences")

user_prompt_input = gr.Textbox(label="User Prompt", value= "{}", visible=False)

matched_srt_output = gr.Textbox(label="Matched SRT Text")
find_matched_srt_btn = gr.Button("Find Matched SRT Text")
fuzzy_search_param = gr.Slider(value = 90, minimum = 50, maximum = 100, step = 10, label="Fuzzy Search Param")
gen_marketing_btn = gr.Button("生成营销文案")
marketing_style = gr.Dropdown(choices=["小红书","微信视频号", "抖音", "快手"], value="小红书")
marketing_prompt = gr.Textbox(label="营销文案提示词", value = f"输出{marketing_style.value}风格的营销标题和文案，字数不要超过100字",scale=2)

def load_workspace(worksapce_name):
    #print(f'workspace_name is {worksapce_name}')
    name = worksapce_name.split(' ')[0]
    time = worksapce_name.split(' ')[-1]
    data = get_workspace_by_name_ts(name, time)
    if len(data) > 0:
        #print(f'data is {data}')
        srt_chunk = data[0].get("srt_chunk","")
        extract_prompt = data[0].get("extract_prompt","")
        key_sentence_prompt = data[0].get("key_sentence_prompt","")
        return [data[0], srt_chunk, extract_prompt, key_sentence_prompt]
    
    return {'data':data}

def save_workspace(srt_chunk, 
                   nice_extract_prompt_input,
                   key_sentence_prompt_input,
                   workspace):
    data = {**workspace, "srt_chunk":srt_chunk, "extract_prompt":nice_extract_prompt_input, "key_sentence_prompt":key_sentence_prompt_input}
    print(f'data is {data}')
    data = save_workspace_data(data)
    return data
    
    
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

def on_select(value, value_2, evt:gr.SelectData):
                        global temp_txt
                        value_2 +=  evt.value + '\n'
                        #print(evt.target.value)
                        return [gr.Textbox(value=value+'  '), value_2]

with gr.Blocks() as demo:
    workspace_data = gr.State({})
    current_workspace_name = gr.State('')
    demo.load(lambda : gr.Dropdown( choices= get_workspace_names()), None, workspaces_list)
    with gr.Row():
        with gr.Column(scale=2):
            with gr.Row():
                
                save_workspace_btn = gr.Button("Save Workspace")
                workspaces_list.render()
                                #load_workspace_btn = gr.Button("Load Workspace")
                
        with gr.Column():
            with gr.Row():
                workspace_input = gr.Textbox(label="Workspace Name", scale=2)
                create_workspace_button = gr.Button("Create Workspace", scale=1)
                
    current_data = gr.Textbox(label="Workspace Data", inputs= workspace_data, value=lambda x:x)
    current_name = gr.Textbox(label="Workspace Name", inputs= current_workspace_name, value=lambda x:x) 

    workspaces_list.change(load_workspace, inputs=[workspaces_list], outputs=[workspace_data, 
                                                                              srt_chunks_output, 
                                                                              nice_extract_prompt_input,
                                                                              key_sentence_prompt_input])\
    .then(lambda x: x['name'], inputs=[workspace_data], outputs=current_workspace_name)
    
    create_workspace_button.click(create_workspace_by_name, inputs=[workspace_input], outputs=[workspace_data])\
        .then(lambda : gr.Dropdown(label="Select Workspace", choices=get_workspace_names(), interactive=True), None, workspaces_list)\
        .then(lambda x:x['name'] + ' at ' + x['time'], workspace_data, workspaces_list)
    
    save_workspace_btn.click(save_workspace, inputs=[srt_chunks_output, nice_extract_prompt_input, key_sentence_prompt_input, workspace_data], outputs=[workspace_data])\
        .then(lambda : gr.Dropdown(label="Select Workspace", choices=get_workspace_names(), interactive=True), None, workspaces_list)\
        .then(lambda x:x['name'] + ' at ' + x['time'], workspace_data, workspaces_list)
    
    #load_workspace_btn.click(load_workspace, inputs=[workspaces_list], outputs=[workspace_data])
    
    with gr.Row():
        srt_file.render()
        with gr.Column(scale=3):
            with gr.Row():
                chunk_length_output.render()
                chunk_similarity_input.render()
                chunk_size_input.render()
                chunk_btn.render()
            srt_chunks_output.render()

    srt_file.change(load_text_from_srt, inputs=[srt_file], outputs=[srt_chunks_output])\
    .then(lambda x: len(x), inputs=[srt_chunks_output], outputs=[chunk_length_output])
    chunk_btn.click(format_chunks, inputs=[current_workspace_name, srt_chunks_output, chunk_similarity_input, chunk_size_input], outputs=[srt_chunks_output])
        
            
    with gr.Row():
        with gr.Column(scale=7):
            with gr.Accordion("LLM Config Details", open=False):
                with gr.Row():
                    llm_model_select.render()
                    llm_model_temperature.render()
                    llm_model_context_num.render()
                    ollama_predict_num.render()
                    ollama_keep_alive.render()
            user_prompt_input.render()
            nice_extract_prompt_input.render()
        with gr.Column(scale=1):
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
    
    selected_contents_output.render()
    query_chunks_topN_input.render()
    matched_chunks_output.render()
    matched_chunks_btn.render()

    matched_chunks_btn.click(query_chunks, inputs=[current_workspace_name, selected_contents_output, query_chunks_topN_input], outputs=[matched_chunks_output])

    key_sentence_prompt_input.render()
    key_sentence_extract_btn.render()
    key_sentence_extracted_output.render()
    
    key_sentence_extract_btn.click(run_model,inputs=[key_sentence_prompt_input, 
                                             matched_chunks_output, 
                                             llm_model_select, 
                                             user_prompt_input,
                                             llm_model_temperature, 
                                             llm_model_context_num, 
                                             ollama_keep_alive,
    ], outputs=key_sentence_extracted_output)
    
demo.launch(server_name='0.0.0.0', server_port=7777)