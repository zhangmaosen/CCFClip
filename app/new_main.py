import gradio as gr

from utils.personal_workspace import create_workspace, get_workspaces

with gr.Blocks() as demo:
    workspaces_list = gr.Dropdown(label="Select Workspace", choices=get_workspaces())
    load_workspace = gr.Button("Load Workspace")
    workspace_input = gr.Textbox(label="Workspace Name")
    create_workspace_button = gr.Button("Create Workspace")

demo.launch(server_name='0.0.0.0')