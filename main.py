import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph.workflow import create_workflow

# Load environment variables
load_dotenv()

app = FastAPI(title="Multi-Agent Research Assistant (LangGraph + CrewAI)")

# Initialize Graph
graph = create_workflow()

class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    result: list

@app.get("/")
def home():
    return {"message": "Welcome to the Multi-Agent Research Assistant API (LangGraph Edition). Use POST /researchagents to start research."}

@app.post("/researchagents")
def run_research_agents(request: ResearchRequest):
    """
    Endpoint to trigger the research agents.
    """
    topic = request.topic
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")

    try:
        initial_state = {"messages": [HumanMessage(content=topic)]}
        print(f"DEBUG: Invoking graph with topic: {topic}")
        
        # Invoke the graph
        # Note: This is synchronous and blocking. For production, async/streaming is better.
        final_state = graph.invoke(initial_state)
        
        # Extract messages
        messages = []
        for msg in final_state["messages"]:
            messages.append({
                "type": msg.type,
                "content": msg.content
            })
            
        return {"messages": messages}

    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
