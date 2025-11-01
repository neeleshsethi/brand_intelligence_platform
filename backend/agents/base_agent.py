from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from core.config import settings


class AgentState(TypedDict):
    """Base state for all agents."""
    messages: Annotated[list, "The messages in the conversation"]
    context: dict
    output: str | None


class BaseAgent:
    """Base class for LangGraph agents."""

    def __init__(self, name: str):
        self.name = name
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY
        )
        self.graph = None

    def build_graph(self) -> StateGraph:
        """Build the agent graph. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement build_graph()")

    async def run(self, input_data: dict) -> dict:
        """Run the agent with input data."""
        if self.graph is None:
            self.graph = self.build_graph()

        result = await self.graph.ainvoke(input_data)
        return result
