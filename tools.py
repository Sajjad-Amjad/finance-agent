# tools.py

import os
import pandas as pd
from llama_index.core.tools import FunctionTool, QueryEngineTool, ToolMetadata
from llama_index.experimental.query_engine.pandas import PandasQueryEngine
from llama_index.tools.code_interpreter import CodeInterpreterToolSpec
from llama_index.agent.openai import OpenAIAgent
from llama_index.core import PromptTemplate

# Custom instruction string to handle errors and provide detailed guidance
instruction_str = """\
1. Convert the query to executable Python code using Pandas.
2. The final line of code should be a Python expression that can be called with the `eval()` function.
3. The code should represent a solution to the query.
4. PRINT ONLY THE EXPRESSION.
5. Do not quote the expression.
6. Ensure to handle possible errors gracefully using try-except blocks.
7. If an error occurs, print a meaningful error message instead of the result.
"""

# Function to create custom pandas prompt template


def create_pandas_prompt_template(filename):
    return PromptTemplate(
        f"""\
You are working with a pandas dataframe in Python.
The name of the dataframe is `df`.
The dataframe is loaded from the file '{filename}'.
This is the result of `print(df.head())`:
{{df_str}}

Follow these instructions:
{{instruction_str}}
Query: {{query_str}}

Expression: """
    )


# Custom response synthesis prompt template
response_synthesis_prompt_template = PromptTemplate(
    """\
Given an input question, synthesize a response from the query results.
Query: {query_str}

Pandas Instructions (optional):
{pandas_instructions}

Pandas Output: {pandas_output}

Response: """
)


def initialize_query_engines(folder_path, llm):
    query_engine_tools = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            engine_name = os.path.splitext(filename)[0].replace(' ', '_')
            pandas_query_engine = PandasQueryEngine(df=df, llm=llm, verbose=False, synthesize_response=True,
                                                    response_synthesis_prompt=response_synthesis_prompt_template, instruction_str=instruction_str)

            # Generate the description with column names and types
            column_info = ', '.join(
                [f"{col} ({dtype})" for col, dtype in zip(df.columns, df.dtypes)])            
            description = (
                f"Provides information from the {engine_name.replace('_', ' ')} dataset loaded from the file '{filename}'. "
                f"Columns: {column_info}. "
                "Use a detailed plain text question as input to the tool."
            )


            tool = QueryEngineTool(
                query_engine=pandas_query_engine,
                metadata=ToolMetadata(
                    name=f"{engine_name}_tool",
                    description=description
                ),
            )

            query_engine_tools.append(tool)

    return query_engine_tools

# Custom tool to generate markdown reports


def generate_markdown_report(query: str) -> str:
    """Generates a markdown report based on the user's query."""
    # Analyze the query and create a markdown report (simple example below)
    report = f"# Report\n\n## Query\n\n{
        query}\n\n## Analysis\n\nThis section contains the analysis of the query."
    return report

# Define the function that interacts with the CodeInterpreterToolSpec to generate the plotting code


def generate_custom_plot_code(context_str: str, query_str: str) -> str:
    """
    Generate Python code for plotting using Matplotlib based on the user's query and the provided data context.

    Args:
        context_str (str): The context information provided by other tools based on the user's query.
        query_str (str): The user's query requesting a plot or graph.

    Returns:
        str: The generated Python code for plotting.
    """
    # Initialize the CodeInterpreterToolSpec
    code_spec = CodeInterpreterToolSpec()
    agent = OpenAIAgent.from_tools(code_spec.to_tool_list())

    # Formulate the message to pass to the agent
    complete_query = f"Given the following context:\n{
        context_str}\n\n{query_str}"

    # Get the response from the agent
    response = agent.chat(complete_query)

    # Extract the generated Python code from the response
    generated_code = response.sources[0].raw_input['kwargs']['code']

    return generated_code
