# agent.py

import os
import pandas as pd
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.experimental.query_engine.pandas import PandasQueryEngine
from llama_index.core import PromptTemplate
from llama_index.core.tools import FunctionTool, QueryEngineTool, ToolMetadata
from llama_index.tools.code_interpreter import CodeInterpreterToolSpec
from llama_index.core.agent import ReActAgent
from llama_index.core import StorageContext, load_index_from_storage

from config import OPENAI_API_KEY, CONTEXT_PATH, CONTEXTDB_PATH, MODEL_NAME
from tools import initialize_query_engines, generate_markdown_report, generate_custom_plot_code

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Initialize the LLM
llm = OpenAI(model=MODEL_NAME)

# Initialize query engines
query_engine_tools = initialize_query_engines(CONTEXT_PATH, llm)

# Initialize company data query
storage_context = StorageContext.from_defaults(persist_dir=CONTEXTDB_PATH)
index = load_index_from_storage(storage_context)
company_data_query = index.as_query_engine(similarity_top_k=3)

# Define the company data tool
company_data_tool = [
    QueryEngineTool(
        query_engine=company_data_query,
        metadata=ToolMetadata(
            name="company_data_tool",
            description=(
                "Provides detailed information about company data including financials, operations, and organizational structure. "
                "Use this tool to query specific details or generate comprehensive reports based on the company's dataset."
            ),
        ),
    )
]

# Define the markdown tool
markdown_tool = FunctionTool.from_defaults(
    generate_markdown_report,
    name="GenerateMarkdownReport",
    description="Generates a markdown report based on the user's query."
)

# Define the custom plotting tool
custom_plotting_tool = FunctionTool.from_defaults(
    generate_custom_plot_code,
    name="generate_custom_plot_code",
    description="Generates Python code for plotting using Matplotlib based on the user's query",
)

# Combine all tools
all_tools = query_engine_tools + [markdown_tool] + [custom_plotting_tool] + company_data_tool

# Initialize ReAct agent
react_agent = ReActAgent.from_tools(all_tools, llm=llm, verbose=False, max_iterations=15)


# Initialize the OpenAIAgent
openai_agent = OpenAIAgent.from_tools(
    tools=all_tools,
    llm=llm,
    verbose=False,
)