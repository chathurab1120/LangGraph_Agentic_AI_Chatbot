import os
from typing import Dict, List, Tuple, Any, TypedDict, Annotated
from dotenv import load_dotenv
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import BaseTool
from langchain.tools.render import format_tool_to_openai_function
from langgraph.graph import END, StateGraph
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

class ChatState(TypedDict):
    """Type definition for chat state."""
    messages: List[Dict[str, str]]
    current_tool: str | None
    tool_result: str | None

def create_agent():
    """Create and configure the agent with tools."""
    
    # Initialize LLM
    llm = ChatGroq(
        api_key=os.getenv("GROK_API_KEY"),
        model_name="llama3-8b-8192",
        temperature=0.7,
    )

    # Initialize tools
    arxiv_tool = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())
    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    search_tool = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))

    tools = [arxiv_tool, wikipedia_tool, search_tool]
    tool_map = {tool.name: tool for tool in tools}
    
    # Convert tools to OpenAI functions format
    functions = [format_tool_to_openai_function(t) for t in tools]
    
    # Define the tool calling node
    def should_use_tool(state: ChatState) -> Tuple[bool, str | None]:
        """Determine if a tool should be used based on the current state."""
        messages = state["messages"]
        response = llm.predict_messages(
            messages,
            functions=functions
        )
        
        if response.additional_kwargs.get("function_call"):
            function_call = response.additional_kwargs["function_call"]
            return True, function_call["name"]
        
        state["messages"].append({"role": "assistant", "content": response.content})
        return False, None

    def call_tool(state: ChatState, tool_name: str) -> ChatState:
        """Execute the specified tool."""
        messages = state["messages"]
        last_message = messages[-1]["content"]
        
        tool = tool_map[tool_name]
        result = tool.invoke(last_message)
        
        state["tool_result"] = result
        state["current_tool"] = tool_name
        return state

    def process_tool_result(state: ChatState) -> ChatState:
        """Process the result from the tool execution."""
        result = state["tool_result"]
        tool_name = state["current_tool"]
        
        messages = state["messages"]
        messages.append({
            "role": "system",
            "content": f"Tool {tool_name} returned: {result}"
        })
        
        response = llm.predict_messages(messages)
        messages.append({"role": "assistant", "content": response.content})
        
        state["tool_result"] = None
        state["current_tool"] = None
        return state

    # Create the graph
    workflow = StateGraph(ChatState)
    
    # Add nodes
    workflow.add_node("tool_decision", should_use_tool)
    workflow.add_node("call_tool", call_tool)
    workflow.add_node("process_result", process_tool_result)
    
    # Add edges
    workflow.add_edge("tool_decision", "call_tool")
    workflow.add_edge("call_tool", "process_result")
    workflow.add_edge("process_result", "tool_decision")
    workflow.add_edge("tool_decision", END)
    
    # Compile the graph
    chain = workflow.compile()
    
    return chain

def process_message(chain, message: str, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Process a message through the agent chain."""
    state = {
        "messages": history + [{"role": "user", "content": message}],
        "current_tool": None,
        "tool_result": None
    }
    
    result = chain.invoke(state)
    return result["messages"] 