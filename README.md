# Finance Assistant Agent

This project is a specialized finance assistant that answers finance-related questions using various datasets. It also generates reports and plots based on user queries. The agent uses advanced AI techniques to provide accurate and concise information.

## Features

- **Finance Expertise**: The agent acts as a finance expert, analyzing provided data to answer questions accurately.
- **Dataset Integration**: It integrates various financial datasets to provide detailed responses.
- **Professional Reports**: Generates comprehensive reports based on user queries.
- **Plot Generation**: Creates and show plots using Matplotlib based on user requests.
- **Error Handling**: Gracefully handles errors and provides accurate information without informing the user of any issues.

## Getting Started

Follow these steps to set up and run the finance assistant on your local machine.

### Prerequisites

- Python 3.11
- Virtual environment tool (venv)

### Setup Instructions

1. **Clone the Repository**

   ```sh
   git clone https://github.com/yourusername/finance-assistant.git
   cd finance-agent

2. **Create a Virtual Environment**

    ```sh
    python -m venv myenv
    ```

3. **Activate the Virtual Environment**

    - On Windows:
    
        ```sh
        myenv\Scripts\activate
        ```
    
    - On macOS/Linux:
    
        ```sh
        source myenv/bin/activate
        ```

4. **Set your `openai_api_key`**

     Open `config.py` file. Replace `your_openai_api_key` with your actual API key.

    ```python
        OPENAI_API_KEY=your_openai_api_key
    ```

5. **Install Dependencies**

    ```sh
    pip install -r requirements.txt
    ```

6. **Run the Streamlit App**
    
    ```sh
    streamlit run app.py
    ```

## Usage

- Enter your finance-related question in the text area.

- Click on "Submit" to get a response.

- The agent will analyze the question and provide an accurate answer based on the datasets.

- If requested, it will generate professional reports or plots.


## Troubleshooting

If you encounter any issues, please ensure all dependencies are installed and the virtual environment is activated. For further assistance, feel free to reach out through GitHub issues.