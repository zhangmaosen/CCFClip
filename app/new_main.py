import gradio as gr

from utils.personal_workspace import *
from utils.functions import *
# for llm
llm_model_select = gr.Dropdown(["qwen2.5:72b-instruct","qwen2.5:32b-instruct","qwen2.5:7b-instruct","phi3:14b-instruct","llama3.1:70b-instruct-q2_K", "gemma2:27b-instruct-q4_0", "deepseek-v2:16b"], label="Model", value="qwen2.5:7b-instruct")
llm_model_temperature = gr.Slider(minimum=0, maximum=1, step=0.1, label="Temperature")
llm_model_context_num = gr.Slider(minimum=8096, maximum=8096*3, step=1, label="Number of Context")
ollama_predict_num = gr.Slider(minimum=768, maximum=4096, step=64, label="Number of Predictions")
ollama_keep_alive = gr.Checkbox(value=True, label="Keep Alive Forever")

# for srt file and build chunks and index
chunk_similarity_input = gr.Slider(minimum=50, maximum=100, step=5, label="Similarity Threshold")
chunk_size_input = gr.Slider(minimum=50, maximum=400, step=10, label="Chunk Size")
chunk_btn = gr.Button()
srt_file = gr.File(label="SRT File")
srt_chunks_output = gr.Textbox(label="Chunks")

nice_extract_prompt_input = gr.Textbox(label="Prompt for Extracting Nice Content")
nice_extract_btn = gr.Button("Extract Nice Content")
nice_content_output = gr.Textbox(label="Nice Content")

key_sentence_prompt_input = gr.Textbox(label="Prompt for Extracting Key Sentences")

user_prompt_input = gr.Textbox(label="User Prompt")

def load_workspace(worksapce_name):
    print(f'workspace_name is {worksapce_name}')
    name = worksapce_name.split(' ')[0]
    return {'name':name}

def save_workspace(srt_chunk, workspace):
    data = {"srt_chunk":srt_chunk, **workspace}
    save_workspace_data(data)
    
with gr.Blocks() as demo:
    workspace_data = gr.State({})
    with gr.Row():
        with gr.Column():
            with gr.Row():
                workspaces_list = gr.Dropdown(label="Select Workspace", choices=get_workspace_names(), interactive=True, scale=2)
                load_workspace_btn = gr.Button("Load Workspace")
                save_workspace_btn = gr.Button("Save Workspace")
        with gr.Column():
            with gr.Row():
                workspace_input = gr.Textbox(label="Workspace Name", scale=2)
                create_workspace_button = gr.Button("Create Workspace")
                
    current_data = gr.Textbox(label="Workspace Data", inputs= workspace_data, value=lambda x:x)
        
    create_workspace_button.click(create_workspace_by_name, inputs=[workspace_input], outputs=[workspace_data])\
        .then(lambda : gr.Dropdown(label="Select Workspace", choices=get_workspace_names(), interactive=True), None, workspaces_list)\
        .then(lambda x:x['name'] + ' at ' + x['time'], workspace_data, workspaces_list)
    
    save_workspace_btn.click(save_workspace, inputs=[srt_chunks_output, workspace_data], outputs=[])
    
    load_workspace_btn.click(load_workspace, inputs=[workspaces_list], outputs=[workspace_data])
    
    with gr.Row():
        srt_file.render()
        with gr.Column(scale=3):
            with gr.Row():
                chunk_similarity_input.render()
                chunk_size_input.render()
                chunk_btn.render()
            srt_chunks_output.render()
        
        
            
    with gr.Row():
        with gr.Column(scale=3):
            with gr.Accordion("LLM Config Details", open=False):
                with gr.Row():
                    llm_model_select.render()
                    llm_model_temperature.render()
                    llm_model_context_num.render()
                    ollama_predict_num.render()
                    ollama_keep_alive.render()
            user_prompt_input.render()
            nice_extract_prompt_input.render()
        nice_extract_btn.render()  
    
    with gr.Row():
        
        nice_content_output.render()
    
    nice_extract_btn.click(run_model,inputs=[nice_extract_prompt_input, 
                                             srt_chunks_output, 
                                             llm_model_select, 
                                             user_prompt_input,
                                             llm_model_temperature, 
                                             llm_model_context_num, 
                                             ollama_keep_alive,
                                             ollama_predict_num
                                             ], outputs=nice_content_output)
demo.launch(server_name='0.0.0.0')