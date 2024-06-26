# utils.py

import re
from pydantic import BaseModel
from typing import Optional
from llama_index.core.program import FunctionCallingProgram
from llama_index.llms.openai import OpenAI

def extract_and_clean_code(response_text):
    """
    Extracts Python code blocks from the response text using regex and removes them from the text.

    Args:
    response_text (str): The agent's response containing Python code blocks.

    Returns:
    tuple: A cleaned response text without Python code blocks and a list of extracted code blocks in their original positions.
    """
    code_pattern = re.compile(r'```python(.*?)```', re.DOTALL)
    code_blocks = []
    cleaned_text_parts = []
    last_end = 0

    for match in code_pattern.finditer(response_text):
        code_blocks.append(match.group(1).strip())
        cleaned_text_parts.append(response_text[last_end:match.start()])
        cleaned_text_parts.append("\nPLOT\n")
        last_end = match.end()

    cleaned_text_parts.append(response_text[last_end:])
    cleaned_text = ''.join(cleaned_text_parts).strip()

    return cleaned_text, code_blocks

def display_text_and_execute_code(response_text):
    """
    Extracts and executes Python code blocks from the response text, displaying the text and graphs.

    Args:
    response_text (str): The agent's response containing Python code blocks.
    """
    cleaned_text, code_blocks = extract_and_clean_code(response_text)

    # Split the cleaned text by the placeholder and iterate through parts
    parts = cleaned_text.split("\nPLOT\n")
    for i, part in enumerate(parts):
        print(part.strip())
        if i < len(code_blocks):
            exec(code_blocks[i], globals())


class ResponseClassification(BaseModel):
    success: bool

# Define a function to classify the response
def classify_response(response_text: str) -> bool:
    prompt_template_str = """
    Classify the following response into a structured format.
    
    Response: {response_text}
    
    The classification should be as follows:
    - success: true if the response is successful, false otherwise
    
    The output should be in JSON format with the field: success.
    """
    
    llm = OpenAI(model="gpt-3.5-turbo")
    
    program = FunctionCallingProgram.from_defaults(
        output_cls=ResponseClassification,
        prompt_template_str=prompt_template_str,
        llm=llm,
    )
    
    output = program(response_text=response_text)
    return output.success

def handle_response(query: str, primary_agent, fallback_agent):
    try:
        response = primary_agent.chat(query)
        is_valid = classify_response(response.response)
        
        if not is_valid:
            st.warning("Primary agent failed. Trying fallback agent...")
            response = fallback_agent.chat(query)
            is_valid = classify_response(response.response)
            
            if not is_valid:
                st.error("Both agents failed to provide a valid response.")
                return None
        return response
    except Exception as e:
        st.error(f"Error handling response: {e}")
        return None
    
