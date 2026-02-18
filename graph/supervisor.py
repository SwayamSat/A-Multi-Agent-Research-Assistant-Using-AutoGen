from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import SystemMessage
from graph.state import AgentState
import os

# Define the list of workers
workers = ["Topic_Refiner", "Paper_Discoverer", "Insight_Synthesizer", "Report_Compiler", "Gap_Analyst"]

async def supervisor_node(state: AgentState):
    """
    The Supervisor node decides which agent should act next.
    """
    messages = state["messages"]
    system_prompt = (
        "You are the supervisor of a research team.\n"
        "Your goal is to manage the research workflow: Refine Topic -> Discover Papers -> Synthesize Insights -> Compile Report -> Analyze Gaps.\n"
        "Given the conversation history, decide who should act next.\n"
        " - If the user just started, pick 'Topic_Refiner'.\n"
        " - If the topic is refined, pick 'Paper_Discoverer'.\n"
        " - If papers are returned, pick 'Insight_Synthesizer'.\n"
        " - If insights are ready, pick 'Report_Compiler'.\n"
        " - If report is done, pick 'Gap_Analyst'.\n"
        " - If Gap Analysis is done, pick 'FINISH'.\n\n"
        "Return ONLY the name of the next agent or 'FINISH'."
    )
    
    # We can use a simpler LLM call here since it's just routing
    api_key = os.getenv("GEMINI_API_KEY")
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", api_key=api_key)
    
    
    # Simple prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "Who should act next?")
    ])
    
    chain = prompt | llm
    # Use ainvoke for async execution
    result = await chain.ainvoke({"messages": messages})
    next_agent = result.content.strip().replace("'", "").replace('"', "")
    
    print(f"\n[Supervisor]: Logic thinks next step is '{next_agent}'")
    
    # Fallback cleanup
    if next_agent not in workers and next_agent != "FINISH":
         # Basic heuristic fallback if LLM gets confused
         last_msg = messages[-1].content
         if "Refinement_Agent" in last_msg: next_agent = "Paper_Discoverer"
         elif "Discovery_Agent" in last_msg: next_agent = "Insight_Synthesizer"
         elif "Insight_Agent" in last_msg: next_agent = "Report_Compiler"
         elif "Report_Agent" in last_msg: next_agent = "Gap_Analyst"
         elif "Gap_Agent" in last_msg: next_agent = "FINISH"
         else: next_agent = "Topic_Refiner"
         
         print(f"[Supervisor]: Fallback override -> '{next_agent}'")

    print(f"[Supervisor]: Routing to -> {next_agent}\n")
    return {"next": next_agent}
