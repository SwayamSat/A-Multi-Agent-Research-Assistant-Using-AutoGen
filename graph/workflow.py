from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import (
    topic_refiner_node,
    paper_discoverer_node,
    insight_synthesizer_node,
    report_compiler_node,
    gap_analyst_node
)
from graph.supervisor import supervisor_node

def create_workflow():
    workflow = StateGraph(AgentState)

    # Add Supervisor
    workflow.add_node("Supervisor", supervisor_node)

    # Add Workers
    workflow.add_node("Topic_Refiner", topic_refiner_node)
    workflow.add_node("Paper_Discoverer", paper_discoverer_node)
    workflow.add_node("Insight_Synthesizer", insight_synthesizer_node)
    workflow.add_node("Report_Compiler", report_compiler_node)
    workflow.add_node("Gap_Analyst", gap_analyst_node)

    # Entry Point
    workflow.set_entry_point("Supervisor")

    # Edges
    # From Workers back to Supervisor
    workflow.add_edge("Topic_Refiner", "Supervisor")
    workflow.add_edge("Paper_Discoverer", "Supervisor")
    workflow.add_edge("Insight_Synthesizer", "Supervisor")
    workflow.add_edge("Report_Compiler", "Supervisor")
    workflow.add_edge("Gap_Analyst", "Supervisor")

    # Conditional Logic from Supervisor
    workflow.add_conditional_edges(
        "Supervisor",
        lambda state: state["next"],
        {
            "Topic_Refiner": "Topic_Refiner",
            "Paper_Discoverer": "Paper_Discoverer",
            "Insight_Synthesizer": "Insight_Synthesizer",
            "Report_Compiler": "Report_Compiler",
            "Gap_Analyst": "Gap_Analyst",
            "FINISH": END
        }
    )

    return workflow.compile()
