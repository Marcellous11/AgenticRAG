# AgenticRAG

## Description

AgenticRAG is a Python project that leverages the capabilities of the LlamaIndex library to create an intelligent agent capable of querying and summarizing documents, performing live chat interactions, and retrieving data from Wikipedia. The project is structured into multiple lessons, each demonstrating different functionalities and use cases of the agent.

## Features

1. **Document Query and Summarization**:
   - The project includes tools to load documents, split them into nodes, and create vector and summary indices. These indices are used to perform queries and generate summaries of the documents.
   - Example: The `get_router_query_engine` function in `lesson_1/utils.py` demonstrates how to set up a query engine for a document.

2. **Live Chat Interaction**:
   - The project supports live chat interactions with the agent, allowing users to ask questions and receive responses in real-time.
   - Example: The `chat` function in `lesson_3/utils.py` demonstrates how to set up a live chat with the agent.

3. **Wikipedia Data Retrieval**:
   - The project includes tools to retrieve data from Wikipedia and save it locally. This data can then be used for further processing and querying.
   - Example: The `get_wiki_data` function in `tools.py` and `lesson_3/utils.py` demonstrates how to retrieve Wikipedia data.

## Setup Instructions

### Prerequisites

- Python 3.9.6 or higher
- Git

### Clone the Repository

```sh
git clone https://github.com/yourusername/agenticrag.git
cd agenticrag
