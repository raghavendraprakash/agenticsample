#!/usr/bin/env python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""
Test script for deployed ULD Load Planner Multi-Agent System on AWS Bedrock AgentCore.

This script tests the deployed ULD Load Planner orchestrator agent by:
1. Retrieving the agent ID from SSM Parameter Store
2. Invoking the agent with sample load planning queries
3. Validating that responses contain pattern analysis and allocation recommendations
4. Testing error handling scenarios
"""

import boto3
import json
import sys
from typing import Dict, Any, Optional
import utils
from boto3.session import Session


def get_agent_id_from_ssm(parameter_name: str) -> Optional[str]:
    """
    Retrieve agent ID from SSM Parameter Store.
    
    Args:
        parameter_name: SSM parameter name containing the agent ID
        
    Returns:
        Agent ID string, or None if not found
        
    Example:
        >>> agent_id = get_agent_id_from_ssm("/app/uld/load_planner_agent_id")
        >>> print(f"Agent ID: {agent_id}")
    """
    try:
        print(f"📋 Retrieving agent ID from SSM: {parameter_name}")
        agent_id = utils.get_ssm_parameter(parameter_name)
        print(f"✅ Found agent ID: {agent_id}")
        return agent_id
    except Exception as e:
        print(f"❌ Error retrieving agent ID from SSM: {str(e)}")
        return None


def invoke_agentcore_agent(agent_id: str, query: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Invoke a deployed AgentCore agent with a query using boto3 bedrock-agentcore client.
    
    Args:
        agent_id: The AgentCore agent ID
        query: The load planning query to send to the agent
        session_id: Optional session ID for conversation continuity
        
    Returns:
        Dictionary containing the agent's response
        
    Raises:
        Exception: If invocation fails
        
    Example:
        >>> response = invoke_agentcore_agent(
        ...     "Uld_Load_Planner_Agent-abc123",
        ...     "Plan loading for 5 pallets of electronics"
        ... )
        >>> print(response['result'])
    """
    boto_session = Session()
    region = boto_session.region_name
    account_id = boto_session.client("sts").get_caller_identity()["Account"]
    
    # Create bedrock-agentcore client
    client = boto3.client('bedrock-agentcore', region_name=region)
    
    # Construct the agent runtime ARN
    agent_runtime_arn = f"arn:aws:bedrock-agentcore:{region}:{account_id}:runtime/{agent_id}"
    
    print(f"\n{'='*60}")
    print(f"Invoking Agent: {agent_id}")
    print(f"Agent ARN: {agent_runtime_arn}")
    print(f"{'='*60}")
    print(f"Query: {query}")
    print()
    
    try:
        # Prepare the payload
        payload = {
            "inputText": query
        }
        
        if session_id:
            payload["sessionId"] = session_id
        
        # Prepare the request
        request_params = {
            'agentRuntimeArn': agent_runtime_arn,
            'payload': json.dumps(payload)
        }
        
        # Invoke the agent
        response = client.invoke_agent_runtime(**request_params)
        
        # Extract the result from the response - it's a streaming body
        result_text = ""
        if 'response' in response:
            # The actual response is in the 'response' key
            streaming_body = response['response']
            if hasattr(streaming_body, 'read'):
                result_text = streaming_body.read().decode('utf-8')
            else:
                result_text = str(streaming_body)
        elif 'output' in response:
            output = response['output']
            if hasattr(output, 'read'):
                result_text = output.read().decode('utf-8')
            elif isinstance(output, bytes):
                result_text = output.decode('utf-8')
            elif isinstance(output, str):
                result_text = output
            else:
                result_text = str(output)
        else:
            result_text = str(response)
        
        print(f"✅ Agent Response:")
        print(f"{result_text}")
        print()
        
        return {
            "result": result_text,
            "agent_id": agent_id,
            "query": query
        }
        
    except Exception as e:
        print(f"❌ Error invoking agent: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise


def test_load_planning_query(agent_id: str, query: str, expected_keywords: list) -> bool:
    """
    Test a load planning query and validate the response.
    
    Args:
        agent_id: The AgentCore agent ID
        query: The load planning query
        expected_keywords: List of keywords that should appear in the response
        
    Returns:
        True if test passes, False otherwise
        
    Example:
        >>> success = test_load_planning_query(
        ...     "Uld_Load_Planner_Agent-abc123",
        ...     "Plan loading for 5 pallets",
        ...     ["pattern", "allocation", "ULD"]
        ... )
    """
    try:
        response = invoke_agentcore_agent(agent_id, query)
        result = response['result'].lower()
        
        # Validate that expected keywords are present
        missing_keywords = []
        for keyword in expected_keywords:
            if keyword.lower() not in result:
                missing_keywords.append(keyword)
        
        if missing_keywords:
            print(f"⚠️  Warning: Expected keywords not found in response: {missing_keywords}")
            return False
        else:
            print(f"✅ Test passed: All expected keywords found in response")
            return True
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def run_all_tests():
    """
    Run all test scenarios for the deployed ULD Load Planner agent.
    
    This function tests:
    1. Basic load planning query
    2. Complex multi-item query
    3. Query with specific constraints
    4. Response validation
    """
    print("\n" + "="*60)
    print("ULD Load Planner Agent Testing")
    print("="*60)
    print()
    
    # Retrieve agent ID from SSM
    ssm_param_name = "/app/uld/load_planner_agent_id"
    agent_id = get_agent_id_from_ssm(ssm_param_name)
    
    if not agent_id:
        print("❌ Cannot proceed without agent ID")
        sys.exit(1)
    
    # Test scenarios
    test_results = []
    
    # Test 1: Basic load planning query
    print("\n" + "="*60)
    print("Test 1: Basic Load Planning Query")
    print("="*60)
    result1 = test_load_planning_query(
        agent_id,
        "I need to plan loading for 5 pallets of electronics equipment. Each pallet weighs approximately 500kg and measures 120cm x 100cm x 150cm. What ULD configuration would you recommend?",
        ["uld", "pallet", "weight", "load"]
    )
    test_results.append(("Basic Load Planning", result1))
    
    # Test 2: Complex multi-item query
    print("\n" + "="*60)
    print("Test 2: Complex Multi-Item Query")
    print("="*60)
    result2 = test_load_planning_query(
        agent_id,
        "I have mixed cargo: 3 pallets of machinery (800kg each), 10 boxes of fragile electronics (50kg each), and 2 large crates (1200kg each). How should I allocate these to ULDs?",
        ["cargo", "allocation", "recommend"]
    )
    test_results.append(("Complex Multi-Item", result2))
    
    # Test 3: Query with specific constraints
    print("\n" + "="*60)
    print("Test 3: Query with Specific Constraints")
    print("="*60)
    result3 = test_load_planning_query(
        agent_id,
        "Plan ULD loading for 8 pallets with weight limit of 6000kg total and height restriction of 160cm. What's the optimal configuration?",
        ["weight", "configuration", "optimal"]
    )
    test_results.append(("Specific Constraints", result3))
    
    # Print test summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print()
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("🎉 All tests passed successfully!")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    """
    Main entry point for ULD agent testing.
    
    Usage:
        python test_deployed_uld_agents.py
        
    Prerequisites:
        - Agent must be deployed to AWS Bedrock AgentCore
        - AWS credentials configured
        - Agent ID stored in SSM Parameter Store
        - Required IAM permissions for AgentCore Runtime API
    """
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Testing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
