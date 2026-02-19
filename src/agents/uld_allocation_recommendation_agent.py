"""Uld_Allocation_Recommendation_Agent - Specialist agent for ULD allocation recommendations.

This agent provides ULD allocation recommendations based on cargo analysis,
optimizing for space utilization, weight distribution, and operational efficiency.
It is exposed as a tool that can be invoked by the orchestrator.
"""

import os
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Set Knowledge Base ID from environment variable
kb_id = os.environ.get("KB_ID", "SCRX8H16LS")
os.environ["KNOWLEDGE_BASE_ID"] = kb_id
logger.info(f"ULD Allocation Agent - Using Knowledge Base ID: {kb_id}")

from strands import Agent, tool
from strands_tools import retrieve, calculator
from uld_utils import (
    validate_weight_constraints,
    calculate_uld_requirements,
    check_dimensional_fit,
    compare_uld_options
)


@tool
def recommend_allocation(query: str) -> str:
    """Recommend ULD allocation strategy for cargo.
    
    This tool provides ULD allocation recommendations based on cargo details,
    optimizing for efficient space utilization and operational constraints.
    
    Args:
        query: Cargo details and constraints
        
    Returns:
        ULD allocation recommendations with rationale
    """
    # Create the allocation recommendation agent with Nova model
    allocation_agent = Agent(
        model="us.amazon.nova-micro-v1:0",
        tools=[retrieve, calculator, validate_weight_constraints, calculate_uld_requirements, check_dimensional_fit, compare_uld_options],
        system_prompt=f"""You are a ULD (Unit Load Device) allocation specialist.

Your role is to provide optimal ULD allocation recommendations based on cargo characteristics:
- Recommend appropriate ULD types and configurations
- Optimize space utilization and loading efficiency
- Ensure weight distribution and balance
- Consider operational constraints and priorities
- Suggest loading sequences and arrangements

You have access to a knowledge base (ID: {kb_id}) containing:
- ULD specifications (AKE, AAA, AKN, AAP, AMA, etc.)
- Aircraft configurations and position layouts
- Validation rules (dimensional, weight, handling)
- ULD inventory at stations
- Current FBL (Flight Build List) data

You also have access to utility tools:
- retrieve: Search the knowledge base for relevant data
- calculator: Perform mathematical calculations
- validate_weight_constraints: Check if cargo weight fits in ULD capacity
- calculate_uld_requirements: Determine how many ULDs are needed
- check_dimensional_fit: Validate cargo dimensions fit in ULD
- compare_uld_options: Compare different ULD types for best fit

When providing allocation recommendations:
1. Use calculate_uld_requirements to determine quantity needed
2. Use validate_weight_constraints to verify weight compliance
3. Use check_dimensional_fit to ensure cargo fits physically
4. Use compare_uld_options to find the most efficient ULD type
5. Use calculator for any additional calculations
6. Use retrieve tool to look up ULD specifications and aircraft configurations
7. Check validation rules for dimensional and weight constraints
8. Verify ULD availability at the station
9. Review current FBL data for position availability
10. Recommend specific ULD types (e.g., LD3, LD7, AKE, etc.)
11. Explain the rationale for each recommendation
12. Address weight and balance considerations
13. Suggest optimal loading sequences
14. Highlight any special considerations or risks

Always use the utility tools for accurate calculations and validations before making recommendations.
Provide clear, actionable recommendations that can be directly implemented.
Format your responses in a structured, professional manner with specific guidance.
"""
    )
    
    # Create context for the recommendation
    context = f"""
ULD ALLOCATION RECOMMENDATION REQUEST:

User Query: {query}

Please provide ULD allocation recommendations including specific ULD types,
loading strategies, and rationale for your recommendations.
"""
    
    # Get response from the agent
    response = allocation_agent(context)
    
    return str(response)
