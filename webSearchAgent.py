from dotenv import load_dotenv


load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama


@tool
def search(query: str) -> str:
    """
    Tool that searches over internet
    Args:
        query: The query to search for 
    Returns:
        The search result    
    """
    print(f"searching for {query}")
    return "Tokyo is sunny"


llm = ChatOllama(temperature=0,model = "qwen2.5:3b")
tools = [search]
agent = create_agent(model = llm, tools = tools)

def webSearchAgent():
    print("hello from web search agent")
    result = agent.invoke({"messages": HumanMessage(content = "what is the weather in Tokyo")})
    print(result["messages"][-1])



if __name__ == "__main__":
    webSearchAgent()    