import os
from dotenv import load_dotenv
load_dotenv()
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from tools.reddit_search import search_reddit
from tools.product_search import search_products
import json

print("Reddit ID:", os.getenv("REDDIT_CLIENT_ID"))
print("SerpAPI Key:", os.getenv("SERPAPI_API_KEY")[:6] + "...")

llm = ChatOpenAI(temperature=0.3, model_name="gpt-4")

tools = [
    Tool(
        name="RedditGiftSearch",
        func=lambda q: search_reddit(q),
        description="Search Reddit for gift ideas based on a query"
    ),
    Tool(
        name="AmazonSearch",
        func=lambda q: search_products(q, site="amazon.com"),
        description="Find product listings on Amazon"
    ),
    Tool(
        name="EtsySearch",
        func=lambda q: search_products(q, site="etsy.com"),
        description="Find product listings on Etsy"
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

with open("gift_data.json") as f:
    gift_data = json.load(f)

query = (
    f"Find gift ideas for a {gift_data['age']} year old who likes "
    f"{', '.join(gift_data['interests'])}. "
    f"Use Reddit to get consensus and then suggest real products within ${gift_data['budget']}."
)

agent.run(query)
