import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_core.tools import FunctionTool
from tools.custom_gemini_client import CustomGeminiClient
from agents.research_agents import create_research_agents
from agents.user_proxy import create_user_proxy
from tools.arxiv_search import search_arxiv
from tools.user_interaction import approve_papers

# Load env variables
load_dotenv()

async def run_workflow():
    # Load config from env
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return

    # Initialize Model Client using CustomGeminiClient
    model_client = CustomGeminiClient(
        api_key=api_key,
        model="gemini-2.5-flash"
    )

    # Prepare Tools
    # search_arxiv needs to be a Tool
    paper_search_tool = FunctionTool(
        search_arxiv, 
        description="Search arXiv for papers based on a query."
    )
    
    # Create Agents
    # Pass tools to create_research_agents so they can be assigned to Paper_Discovery_Agent
    agents_dict = create_research_agents(model_client, paper_discovery_tools=[paper_search_tool])
    user_proxy = create_user_proxy()

    # --- Deterministic Selector Logic ---
    from autogen_core.models import ChatCompletionClient, CreateResult, RequestUsage, ModelCapabilities, ModelInfo, LLMMessage
    from typing import Sequence, Any, Union

    class DeterministicSelector(ChatCompletionClient):
        def __init__(self, agent_order: list[str]):
            self.agent_order = agent_order
            self._capabilities = ModelCapabilities(vision=False, function_calling=False, json_output=False)
            self._usage = RequestUsage(prompt_tokens=0, completion_tokens=0)

        @property
        def capabilities(self): return self._capabilities
        @property
        def model_capabilities(self): return self._capabilities
        @property
        def model_info(self): return ModelInfo(vision=False, function_calling=False, json_output=False, family="deterministic")
        
        def remaining_tokens(self, *args, **kwargs): return float("inf")
        def actual_usage(self): return self._usage
        def total_usage(self): return self._usage
        def close(self): pass
        def count_tokens(self, *args, **kwargs): return 0

        async def create_stream(self, messages, **kwargs):
             result = await self.create(messages, **kwargs)
             yield result

        async def create(self, messages: Sequence[LLMMessage], **kwargs) -> CreateResult:
            prompt = messages[0].content
            
            # Parse Prompt to find Last Speaker and Content
            last_speaker = None
            prompt_str = prompt
            
            known_agents = self.agent_order
            max_idx = -1
            
            for agent in known_agents:
                idx = prompt_str.rfind(agent)
                if idx > max_idx:
                    max_idx = idx
                    last_speaker = agent
            
            target_agent = "Topic_Refinement_Agent" # Default fallback
            
            # Check for explicit help request in recent text (simple check)
            if "REQUEST_USER_HELP" in prompt_str[max_idx:]:
                return CreateResult(content="User_Proxy", usage=self._usage, finish_reason="stop", cached=False)
            
            if last_speaker == "Gap_Analysis_Agent":
                # Handover to User for review
                target_agent = "User_Proxy"
                
            elif last_speaker == "User_Proxy":
                # User has spoken. Restart cycle
                target_agent = "Topic_Refinement_Agent"
                
            elif last_speaker == "Report_Compiler_Agent":
                target_agent = "Gap_Analysis_Agent"
                
            elif last_speaker == "Insight_Synthesizer_Agent":
                target_agent = "Report_Compiler_Agent"
                
            elif last_speaker == "Paper_Discovery_Agent":
                if "Tool Call" in prompt_str[max_idx:] or "search_arxiv" in prompt_str[max_idx:]:
                     target_agent = "Paper_Discovery_Agent"
                else:
                     target_agent = "Insight_Synthesizer_Agent"
                     
            elif last_speaker == "Topic_Refinement_Agent":
                target_agent = "Paper_Discovery_Agent"
            
            return CreateResult(content=target_agent, usage=self._usage, finish_reason="stop", cached=False)

    selector_client = DeterministicSelector([
        "user", "Topic_Refinement_Agent", "Paper_Discovery_Agent", "User_Proxy", 
        "Insight_Synthesizer_Agent", "Report_Compiler_Agent", "Gap_Analysis_Agent"
    ])

    selector_prompt = "You are a deterministic selector. This prompt is ignored by the logic."

    termination = TextMentionTermination(text="TERMINATE")

    team = SelectorGroupChat(
        participants=[
            user_proxy,
            agents_dict["topic_refinement_agent"],
            agents_dict["paper_discovery_agent"],
            agents_dict["insight_agent"],
            agents_dict["report_agent"],
            agents_dict["gap_agent"]
        ],
        model_client=selector_client,
        selector_prompt=selector_prompt,
        termination_condition=termination,
        allow_repeated_speaker=True
    )

    # Run the workflow
    print("Initiating Research Assistant (AutoGen 0.4)...")
    initial_message = """I want to research "Multi-Agent Systems for Autonomous Driving". 
Please refine this topic, find relevant papers, synthesize insights, compile a report, and identify research gaps.
"""
    
    # Run with streaming to see progress
    stream = team.run_stream(task=initial_message)
    async for msg in stream:
        print(f"DEBUG: Msg type: {type(msg)}")
        if hasattr(msg, 'source'):
            print(f"DEBUG: Source: {msg.source}")
        if hasattr(msg, 'content'):
            print(f"[{msg.source}]: {msg.content}")
        elif hasattr(msg, 'delta'): # ModelToken
            print(msg.delta, end="", flush=True)
        else:
            print(f"DEBUG: Unhandled msg: {msg}")

def main():
    asyncio.run(run_workflow())

if __name__ == "__main__":
    main()
