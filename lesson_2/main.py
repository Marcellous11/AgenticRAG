from utils import ToolAgent, Tools
import nest_asyncio


nest_asyncio.apply()

    
prompt = "Build me a basic HTML input from. Should have a nav bar, Log in for user name as password. Make it look good too."

res = ToolAgent.query(prompt,[Tools.add,Tools.mystery,Tools.get_wiki_data,Tools.write_to_file])

print(res)