# from helper import get_openai_api_key
from llama_index.llms.openai import OpenAI
from llama_index.core.vector_stores import MetadataFilters
from llama_index.core.tools import FunctionTool
from llama_index.core import SummaryIndex
from llama_index.core.tools import QueryEngineTool
from typing import List,Callable
from llama_index.core.vector_stores import FilterCondition
import nest_asyncio
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from pathlib import Path
import requests
nest_asyncio.apply()



class ToolAgent:
    def __init__(self):
        pass

    @staticmethod
    def query(prompt:str,funcs:List[Callable]):
        myTools = [FunctionTool.from_defaults(fn=myfunction) for myfunction in funcs]

        llm = OpenAI(model="gpt-3.5-turbo")
        response = llm.predict_and_call(
            myTools, 
            prompt, 
            verbose=True
        )
        return str(response)
    

class Tools:

    def __init__(self):
        pass

    @staticmethod
    def add(x: int, y: int) -> int:
        """Adds two integers together."""
        return x + y
    
    @staticmethod
    def square(x: int) -> int:
        """Takes a single interager multiples that value by its self"""
        return x ** 2
    

    @staticmethod
    def mystery(x: int, y: int) -> int: 
        """Mystery function that operates on top of two numbers."""
        return (x + y) * (x + y)

    @staticmethod
    def get_wiki_data(city_list:list[str])->None:
        """Get text from wiki page and write to file locally"""

        for title in city_list:
            response = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "format": "json",
                    "titles": title,
                    "prop": "extracts",
                    # 'exintro': True,
                    "explaintext": True,
                },
            ).json()
            page = next(iter(response["query"]["pages"].values()))
            wiki_text = page["extract"]

            data_path = Path("data")
            if not data_path.exists():
                Path.mkdir(data_path)

            with open(data_path / f"{title}.txt", "w") as fp:
                fp.write(wiki_text)


    @staticmethod
    def write_to_file(input:str,file_type:str)->None:
        """Takes Code text and writes it to a corresponding file"""

        with open(f"{"generated"}.{file_type}", "w") as fp:
            fp.write(input)



class RAGtools():
    def __init__(self):
        pass

    @staticmethod
    def vector_search(query:str)->str:
        """Takes a query to preform a vector seach on the current documents"""
        Path("data").mkdir(parents=True, exist_ok=True)
        document = SimpleDirectoryReader(input_dir="data").load_data()
        splitter = SentenceSplitter(chunk_size=1024)
        nodes = splitter.get_nodes_from_documents(document)

        vector_index = VectorStoreIndex(nodes)
        vector_query_engine = vector_index.as_query_engine(
            similarity_top_k=2,
            description=(
                "Useful if you want to get specific information from given text"
            ),
        )
        res = vector_query_engine.query(query)
        return res

    @staticmethod
    def summary_search(query:str)->str:
        "Takes a qeury to perform a summation search on the current documents"
        Path("data").mkdir(parents=True, exist_ok=True)
        document = SimpleDirectoryReader(input_dir="data").load_data()
        splitter = SentenceSplitter(chunk_size=1024)
        nodes = splitter.get_nodes_from_documents(document)

        summary_index = SummaryIndex(nodes)
        summary_query_engine = summary_index.as_query_engine(
            response_mode="tree_summarize",
            use_async=True,
        )
        response = summary_query_engine.query(query)
        return response



    @staticmethod
    def queryTools() -> List[QueryEngineTool]:
        """Get vector query and summary query tools from a document."""

        Path("data").mkdir(parents=True, exist_ok=True)
        document = SimpleDirectoryReader(input_dir="data").load_data()
        splitter = SentenceSplitter(chunk_size=1024)
        nodes = splitter.get_nodes_from_documents(document)

        summary_index = SummaryIndex(nodes)
        summary_query_engine = summary_index.as_query_engine(
            response_mode="tree_summarize",
            use_async=True,
        )

        summary_tool = QueryEngineTool.from_defaults(
            name="summary_tool",
            query_engine=summary_query_engine,
            description=(
                "Useful if you want to get a summary of given text"
            ),
        )
        
        vector_index = VectorStoreIndex(nodes)
        vector_query_engine = vector_index.as_query_engine(
            similarity_top_k=2,
            description=(
                "Useful if you want to get specific information from given text"
            ),

        )

        vector_query_tool = QueryEngineTool.from_defaults(
            name="vector_tool",
            query_engine=vector_query_engine
        )


        return [vector_query_tool,summary_tool]
    
    
