import os
import json
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph.workflow import create_workflow

# Load environment variables
load_dotenv()

app = FastAPI(title="Multi-Agent Research Assistant (LangGraph + CrewAI)")

# Enable CORS for Frontend (Allow all origins for deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for production deployment
    allow_credentials=False,  # Must be False when allow_origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Graph
graph = create_workflow()

class ResearchRequest(BaseModel):
    topic: str

@app.get("/")
def home():
    return {"message": "Welcome to the Multi-Agent Research Assistant API. Use POST /research-stream for real-time updates."}

@app.post("/researchagents")
def run_research_agents(request: ResearchRequest):
    """
    Legacy synchronous endpoint.
    """
    topic = request.topic
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")

    try:
        initial_state = {"messages": [HumanMessage(content=topic)]}
        print(f"DEBUG: Invoking graph with topic: {topic}")
        
        final_state = graph.invoke(initial_state)
        
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

@app.post("/research-stream")
async def stream_research_agents(request: Request, body: ResearchRequest):
    """
    Streaming endpoint using Server-Sent Events (SSE).
    """
    topic = body.topic
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")

    async def event_generator():
        initial_state = {"messages": [HumanMessage(content=topic)]}
        
        # We use graph.stream to get updates from each node
        try:
            # Send initial status
            yield f"data: {json.dumps({'type': 'status', 'agent': 'Supervisor', 'status': 'planning'})}\n\n"
            
            # Using stream with stream_mode="updates" ensures we get the output of each node as it finishes
            for output in graph.stream(initial_state, stream_mode="updates"):
                if await request.is_disconnected():
                    print("DEBUG: Client disconnected. Stopping research.")
                    break
                
                print(f"DEBUG: Graph step output: {output.keys()}")
                for key, value in output.items():
                    # key is the node name (e.g., 'Topic_Refiner', 'Supervisor')
                    
                    if key == "Supervisor":
                        next_agent = value.get("next", "Unknown")
                        print(f"DEBUG: Supervisor routing to {next_agent}")
                        
                        # Emit Supervisor thought/decision as a message
                        thought_content = f"Analyzed current state. Deciding next step: **{next_agent}**."
                        yield f"data: {json.dumps({'type': 'message', 'agent': 'Supervisor', 'content': thought_content})}\n\n"
                        await asyncio.sleep(0.1) # Force yield
                        
                        yield f"data: {json.dumps({'type': 'status', 'agent': next_agent, 'status': 'working'})}\n\n"
                        await asyncio.sleep(0.1) # Force yield
                    
                    else:
                        print(f"DEBUG: Agent {key} finished task.")
                        # Worker node content
                        if "messages" in value and value["messages"]:
                            last_msg = value["messages"][-1]
                            content = last_msg.content
                            yield f"data: {json.dumps({'type': 'message', 'agent': key, 'content': content})}\n\n"
                            await asyncio.sleep(0.1) # Force yield
                            
                            # Log completion of this agent
                            yield f"data: {json.dumps({'type': 'status', 'agent': key, 'status': 'completed'})}\n\n"
                            await asyncio.sleep(0.1) # Force yield

            yield f"data: {json.dumps({'type': 'status', 'agent': 'System', 'status': 'finished'})}\n\n"
            await asyncio.sleep(0.1) # Force yield
            
        except Exception as e:
            print(f"ERROR: Stream loop failed: {e}")
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream", headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache", "Connection": "keep-alive"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
