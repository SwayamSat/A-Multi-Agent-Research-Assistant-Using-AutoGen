from langchain_core.messages import HumanMessage, AIMessage
from crew.agents import ResearchAgents
from crew.tasks import ResearchTasks
from crewai import Crew, Process
from graph.state import AgentState

# Initialize Agents and Tasks instances globally to avoid recreation
_agents = ResearchAgents()
_tasks = ResearchTasks()

def _run_task(agent, task_func, state: AgentState):
    """
    Helper to run a single task with a single agent.
    """
    messages = state["messages"]
    last_message = messages[-1].content
    
    # Create the task
    task = task_func(agent, last_message if "Refinement" in agent.role else state)

    # Note: CrewAI is designed for teams, but we can run a crew of 1 for granular control
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    result = crew.kickoff()
    return {"messages": [AIMessage(content=str(result))]}

def topic_refiner_node(state: AgentState):
    agent = _agents.topic_refiner()
    # For refiner, we pass the raw topic. For others, context is usually implicit or passed differently.
    # Here simplification: we pass the last message content as the input.
    messages = state["messages"]
    topic = messages[-1].content
    
    # Create task
    task = _tasks.refine_task(agent, topic)
    
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    return {"messages": [AIMessage(content=f"Refinement_Agent: {result}")]}

def paper_discoverer_node(state: AgentState):
    agent = _agents.paper_discoverer()
    # The agent needs the refined topic. In a real graph, we might parse it.
    # Assuming previous message contains the refined topic/instructions.
    task = _tasks.discovery_task(agent)
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    return {"messages": [AIMessage(content=f"Discovery_Agent: {result}")]}

def insight_synthesizer_node(state: AgentState):
    agent = _agents.insight_synthesizer()
    task = _tasks.synthesis_task(agent)
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    return {"messages": [AIMessage(content=f"Insight_Agent: {result}")]}

def report_compiler_node(state: AgentState):
    agent = _agents.report_compiler()
    task = _tasks.report_task(agent)
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    return {"messages": [AIMessage(content=f"Report_Agent: {result}")]}

def gap_analyst_node(state: AgentState):
    agent = _agents.gap_analyst()
    task = _tasks.gap_analysis_task(agent)
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    return {"messages": [AIMessage(content=f"Gap_Agent: {result}")]}
