from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field

load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch


class Source(BaseModel):
    """schema for a source used by the agent"""

    url:str = Field(description="The URL of the source")

class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""

    answer:str = Field(description="The agent's answer to the query")
    sources: List[Source] = Field(default_factory=list, description="List of sources used to generate the answer")

llm = ChatOllama(temperature=0,model = "qwen2.5:3b")
tools = [TavilySearch(max_results = 3,topic="general",search_depth="advanced")]
agent = create_agent(model = llm, tools = tools, response_format=AgentResponse)

def webSearchAgent():
    print("hello from web search agent")
    result = agent.invoke({"messages": HumanMessage(content = "search for 3 job postings for an ai engineer using langchain in the area on linkedin and list their details")})
    print(result)
    



if __name__ == "__main__":
    webSearchAgent()    