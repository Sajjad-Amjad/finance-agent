import streamlit as st
from agent import openai_agent, react_agent
from utils import display_text_and_execute_code, extract_and_clean_code, handle_response
from matplotlib import pyplot as plt
from config import OPENAI_API_KEY
import base64
import pandas as pd


import os
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

st.title("Finance Assistant")

query = st.text_area("Enter your finance-related question:")
if st.button("Submit"):
    response = handle_response(query, react_agent, openai_agent)
    
    if response:
        cleaned_text, code_blocks = extract_and_clean_code(response.response)

        # Split the cleaned text by the placeholder and iterate through parts
        parts = cleaned_text.split("\nPLOT\n")
        for i, part in enumerate(parts):
            st.markdown(part.strip())
            if i < len(code_blocks):
                # Execute the code and capture the plot
                try:
                    exec(code_blocks[i], globals())
                    fig = plt.gcf()
                    st.pyplot(fig)
                    plt.clf()
                except Exception as e:
                    st.error(f"An error occurred while generating the plot: {e}")

# Function to convert matplotlib plot to HTML
def mpl_to_html(fig):
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    return f'<img src="data:image/png;base64,{img_str}"/>'