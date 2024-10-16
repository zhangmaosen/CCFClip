import streamlit as st
from utils.personal_workspace import *
from streamlit_extras.row import row
st.set_page_config(layout="wide")
@st.dialog("Select your workspace")
def create_workspace_dialog():
    name = st.text_input("What's your name?")
    if st.button("create"):
        workspace_name = create_workspace({"name":name})
        st.session_state.workspace_data = workspace_name
        st.rerun()

if "workspace_data" not in st.session_state:
    col1, col2, col3 = st.columns([2,1,1],vertical_alignment="bottom")
    workspace_data = get_workspaces()
    workspace_list = [item['name'] + ' at ' + item['time'] for item in workspace_data]
    with col1:
        selection = st.selectbox("Select your workspace", workspace_list)
    with col2:
        if st.button("Load workspace", use_container_width=True):
            st.session_state.workspace_data = workspace_data[workspace_list.index(selection)]
            st.rerun()
    with col3:
        if st.button("Create workspace", use_container_width=True):
            create_workspace_dialog()
        #st.rerun()
else:
    col1, col2 = st.columns([2,1], vertical_alignment="bottom")
    with col1:
        st.text_input("Workspace name", st.session_state.workspace_data['name'])
    with col2:
        if st.button("Save workspace"):
            create_workspace(st.session_state.workspace_data)


