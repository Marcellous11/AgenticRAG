from utils import get_router_query_engine

query_engine = get_router_query_engine("data/Boston.txt")

response = query_engine.query("Summaries all the main facts in the data and give me a short description of location")
print(str(response))
