import os   
import json
import traceback
import pandas as pd
from src.mcqgenerator.utils import read_file
import streamlit as st
from src.mcqgenerator.looger import logging
from src.mcqgenerator.MCQGENERATOR import completion_evaluation



st.title("Diagnosis application with langchain")

with st.form("report_input"):
    uploaded_report=st.file_uploader("upload your report as a PDF or txt")
    button=st.form_submit_button("Give me the analysis")

    if button and uploaded_report is not None:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_report)

                response=completion_evaluation(text)
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            else:
                st.write(response)
