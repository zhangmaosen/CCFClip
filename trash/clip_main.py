import streamlit as st
from utils.dbs import * 

@st.dialog("resume or create your work")
def select_wk():
    wk_space = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"),
)
    
    if st.button("Submit"):
        st.session_state.wk_space = wk_space
        st.rerun()
    if st.button("New"):
        st.session_state.wk_space = ""


if "wk_space" not in st.session_state :
    select_wk()
else:
    st.text_input(label=" ", value = st.session_state.wk_space)