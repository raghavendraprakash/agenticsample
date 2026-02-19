"""Uld_Load_Planner_Agent - Orchestrator agent for ULD load planning.

This orchestrator coordinates ULD (Unit Load Device) load planning by delegating
to specialist agents for pattern analysis and allocation recommendations.
It uses the "Agents as Tools" pattern to coordinate between specialists.
"""

import os
import logging
from strands import Agent
from typing import Any

# Setup logger
logger = logging.getLogger(__name__)

# Set Knowledge Base ID from environment variable
kb_id = os.environ.get("KB_ID", "SCRX8H16LS")
os.environ["KNOWLEDGE_BASE_ID"] = kb_id
logger.info(f"ULD Load Planner Orchestrator - Using Knowledge Base ID: {kb_id}")

# Import specialist agent tools
from uld_pattern_analysis_agent import analyze_cargo_patterns
from uld_allocation_recommendation_agent import recommend_allocation


def create_load_planner_orchestrator(query: str) -> Any:
    """Create and invoke the ULD Load Planner orchestrator agent.
    
    This orchestrator coordinates load planning requests by delegating to
    specialist agents for comprehensive cargo analysis and allocation recommendations.
    
    The orchestrator follows this workflow:
    1. Analyze cargo patterns using the Pattern Analysis Agent
    2. Get allocation recommendations using the Allocation Recommendation Agent
    3. Synthesize results into a coherent load plan
    
    Args:
        query: User's load planning query describing cargo and constraints
        
    Returns:
        Agent response object containing the orchestrated load plan
        
    Example:
        >>> result = create_load_planner_orchestrator(
        ...     "Plan loading for 5 pallets of electronics, each 120x100x80cm, 500kg"
        ... )
        >>> print(result.message)
    """
    # Define orchestrator system prompt
    orchestrator_system_prompt = f"""You are a ULD Load Planner Orchestrator that coordinates cargo loading operations.

Your role is to analyze load planning queries and coordinate with specialist agents:
1. analyze_cargo_patterns - For analyzing cargo patterns and constraints (has access to KB)
2. recommend_allocation - For providing ULD allocation recommendations (has access to KB)

Both specialist agents have access to a comprehensive knowledge base (ID: {kb_id}) containing:
- Historical loading patterns and optimization data
- Aircraft configurations (B777, A350, B747, B767, A330)
- ULD specifications (AKE/LD3, AAA/LD7, AKN/LD8, AAP/LD6, AMA/LD9)
- Validation rules (dimensional, weight, handling codes)
- Flight schedules and current FBL data
- ULD inventory at stations

When you receive a load planning query:
1. First, use analyze_cargo_patterns to understand the cargo characteristics
   - The agent will retrieve relevant historical patterns and constraints from the KB
2. Then, use recommend_allocation to get allocation suggestions
   - The agent will retrieve ULD specs, aircraft configs, and validation rules from the KB
3. Synthesize the results into a coherent load plan

The specialist agents will automatically query the knowledge base for relevant data.
Your job is to coordinate their responses and provide comprehensive load planning guidance.
"""
    
    # Create orchestrator with Amazon Nova Lite model
    orchestrator = Agent(
        model="us.amazon.nova-lite-v1:0",
        system_prompt=orchestrator_system_prompt,
        tools=[analyze_cargo_patterns, recommend_allocation]
    )
    
    # Invoke orchestrator with the query
    response = orchestrator(query)
    
    return response
