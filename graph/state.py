from typing import TypedDict, Annotated, List, Union
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    # The list of messages in the conversation
    messages: Annotated[List[BaseMessage], operator.add]
    # The next agent to act
    next: str
