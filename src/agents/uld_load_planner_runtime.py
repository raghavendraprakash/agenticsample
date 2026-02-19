#!/usr/bin/env python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""
Uld_Load_Planner_Runtime - AgentCore Runtime entrypoint for ULD Load Planner.

This module implements the AgentCore Runtime entrypoint for the ULD Load Planner
orchestrator agent. It provides the deployment interface for Amazon Bedrock
AgentCore Runtime.

Key Features:
- AgentCore Runtime entrypoint with @app.entrypoint decorator
- Integration with ULD Load Planner orchestrator
- Request payload handling (inputText/prompt extraction)
- Response formatting for AgentCore Runtime

Architecture:
- Orchestrator coordinates 2 specialized agents:
  1. Uld_Pattern_Analysis_Agent (cargo pattern analysis)
  2. Uld_Allocation_Recommendation_Agent (allocation recommendations)

Deployment:
- Deploy to AgentCore Runtime using bedrock-agentcore CLI
- Invoke via AgentCore Runtime API with load planning queries
"""

import logging
import sys
from pathlib import Path
from typing import Dict, Any

# AgentCore imports
from bedrock_agentcore import BedrockAgentCoreApp

# Add current directory to Python path for local imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import orchestrator
from uld_load_planner_orchestrator import create_load_planner_orchestrator


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("uld-load-planner-runtime")


# ============================================================================
# AGENTCORE APP INITIALIZATION
# ============================================================================

app = BedrockAgentCoreApp()


# ============================================================================
# AGENTCORE RUNTIME ENTRYPOINT
# ============================================================================

@app.entrypoint
def invoke(payload: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AgentCore Runtime entrypoint for the ULD Load Planner orchestrator.
    
    This function is called by AgentCore Runtime when the agent is invoked.
    It handles request processing and response formatting for load planning queries.
    
    Payload Parameters:
        - inputText or prompt (required): User's load planning query
        - session_id (optional): Session identifier for conversation continuity
    
    Returns:
        Dictionary with 'result' key containing the load planning response
        
    Raises:
        Exception: If required parameters are missing or processing fails
        
    Example Payload:
        {
            "inputText": "Plan loading for 5 pallets of electronics, each 120x100x80cm, 500kg",
            "session_id": "session-123"
        }
    """
    # Extract user message (support both 'inputText' and 'prompt' keys)
    user_message = payload.get("inputText") or payload.get("prompt")
    if not user_message:
        raise Exception("Payload must include 'inputText' or 'prompt' parameter")
    
    # Extract optional session_id
    session_id = payload.get("session_id", "default-session")
    
    logger.info(f"Uld_Load_Planner_Runtime - Entrypoint invoked")
    logger.info(f"User message: {user_message}")
    logger.info(f"Session ID: {session_id}")
    
    # Create and invoke orchestrator agent
    try:
        logger.info("Creating ULD Load Planner orchestrator")
        result = create_load_planner_orchestrator(query=user_message)
        
        # Extract message from result
        response_message = result.message if hasattr(result, 'message') else str(result)
        
        logger.info("ULD Load Planner successfully processed request")
        
        return {
            "result": response_message,
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"Error in ULD Load Planner processing: {str(e)}")
        raise


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Run the AgentCore Runtime application.
    
    This starts the AgentCore Runtime server that listens for invocations.
    The server handles request routing and response formatting.
    
    Deployment:
        1. Deploy to AgentCore Runtime:
           bedrock-agentcore deploy --runtime-file uld_load_planner_runtime.py
        
        2. Invoke via AgentCore Runtime API:
           POST /invoke
           {
               "inputText": "Plan loading for 5 pallets of electronics"
           }
    """
    logger.info("Starting Uld_Load_Planner_Runtime AgentCore Runtime application")
    app.run()
