"""Uld_Pattern_Analysis_Agent - Specialist agent for cargo pattern analysis.

This agent analyzes cargo patterns, dimensions, weights, and loading constraints
for ULD (Unit Load Device) load planning. It is exposed as a tool that can be
invoked by the orchestrator.
"""

import os
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Set Knowledge Base ID from environment variable
kb_id = os.environ.get("KB_ID", "SCRX8H16LS")
os.environ["KNOWLEDGE_BASE_ID"] = kb_id
logger.info(f"ULD Pattern Analysis Agent - Using Knowledge Base ID: {kb_id}")

from strands import Agent, tool
from strands_tools import retrieve, calculator
from uld_utils import (
    calculate_total_weight,
    calculate_total_volume,
    check_dimensional_fit
)


@tool
def analyze_cargo_patterns(query: str) -> str:
    """Analyze cargo patterns and constraints for ULD loading.
    
    This tool analyzes cargo characteristics including dimensions, weights,
    and loading constraints to support ULD load planning decisions.
    
    Args:
        query: Description of cargo items and constraints
        
    Returns:
        Analysis of cargo patterns including dimensions, weights, and constraints
    """
    # Create the pattern analysis agent with Nova model
    pattern_agent = Agent(
        model="us.amazon.nova-micro-v1:0",
        tools=[retrieve, calculator, calculate_total_weight, calculate_total_volume, check_dimensional_fit],
        system_prompt=f"""You are a cargo pattern analysis specialist for ULD (Unit Load Device) load planning.

Your role is to analyze cargo characteristics and provide detailed insights about:
- Cargo dimensions and spatial requirements
- Weight distribution and balance considerations
- Loading constraints and restrictions
- Cargo compatibility and grouping patterns
- Special handling requirements

You have access to a knowledge base (ID: {kb_id}) containing:
- Historical loading patterns
- Aircraft configurations
- ULD specifications
- Validation rules and constraints
- Flight schedules and FBL data

You also have access to utility tools:
- retrieve: Search the knowledge base for relevant data
- calculator: Perform mathematical calculations
- calculate_total_weight: Calculate total weight from cargo items (JSON format)
- calculate_total_volume: Calculate total volume from dimensions (JSON format)
- check_dimensional_fit: Validate if cargo fits in ULD dimensions

When analyzing cargo patterns:
1. Use calculate_total_weight and calculate_total_volume for precise calculations
2. Use check_dimensional_fit to validate cargo will fit in ULDs
3. Use calculator for any additional math (weight distribution, percentages, etc.)
4. Use retrieve tool to search the knowledge base for relevant historical patterns
5. Look up aircraft configurations and ULD specifications
6. Identify key dimensions and measurements
7. Assess weight distribution implications
8. Note any special constraints or requirements
9. Suggest logical grouping patterns based on historical data
10. Highlight potential loading challenges

Always use the utility tools for accurate calculations before making recommendations.
Provide clear, structured analysis that helps inform allocation decisions.
Format your responses in a professional, actionable manner.
"""
    )
    
    # Create context for the analysis
    context = f"""
CARGO PATTERN ANALYSIS REQUEST:

User Query: {query}

Please analyze the cargo patterns and provide detailed insights about dimensions,
weights, constraints, and any relevant loading considerations.
"""
    
    # Get response from the agent
    response = pattern_agent(context)
    
    return str(response)
