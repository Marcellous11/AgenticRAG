from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner
from llama_index.llms.openai import OpenAI
from utils import Tools
from utils import RAGtools
import nest_asyncio
from llama_index.core.tools import FunctionTool
nest_asyncio.apply()





# summary_tool = RAGtools.queryTools()


llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

def chat():
    agent_worker = FunctionCallingAgentWorker.from_tools(
        [ ], 
        llm=llm, 
        verbose=True
    )
    agent = AgentRunner(agent_worker)
    
    print("Live chat started. Type 'exit' to quit.")

    while True:

        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting Chat.")
            break

        response = agent.chat(user_input)
        print("Bot: ",response)



def runner():
    print("Live task-based chat started. Type 'exit' to quit.")

    add_tool = FunctionTool.from_defaults(Tools.add)
    square_tool = FunctionTool.from_defaults(Tools.square)
    wiki_web_tool = FunctionTool.from_defaults(Tools.get_wiki_data)
    write_to_file_tool = FunctionTool.from_defaults(Tools.write_to_file)
    vector_tool = FunctionTool.from_defaults(RAGtools.vector_search)
    summary_tool = FunctionTool.from_defaults(RAGtools.summary_search)
     
    agent_worker = FunctionCallingAgentWorker.from_tools(
        [ add_tool,square_tool,wiki_web_tool,write_to_file_tool,vector_tool,summary_tool], 
        llm=llm, 
        verbose=True
    )

    agent = AgentRunner(agent_worker)

    while True:
        user_input= input("You: ")

        if user_input.lower() == "exit":
            print("Exiting chat.")
            break

        task = agent.create_task(user_input)
        step_output = agent.run_step(task.task_id)
        
        completed_steps = agent.get_completed_steps(task.task_id)
        if completed_steps:
            print(f"****Completed for task {task.task_id}: {len(completed_steps)}")
   
        while not step_output.is_last:
            nudge = input("Extra input: -")
            step_output = agent.run_step(task.task_id,input=nudge)
        upcoming_steps = agent.get_upcoming_steps(task.task_id)
        print(f"***Upcoming steps for task {task.task_id}: {len(upcoming_steps)}")

        response = agent.finalize_response(task.task_id)

        print("Final Response: ",str(response))