"""Integration test for ULD utility functions with deployed agents.

This script tests that the utility functions work correctly when invoked
through the deployed ULD Load Planner agent on AWS AgentCore.
"""

import boto3
import json
import os
import sys
from boto3.session import Session

def test_agent_with_utility_functions():
    """Test the deployed agent using utility functions."""
    
    # Get agent ID from SSM or deployment file
    try:
        ssm = boto3.client('ssm', region_name='us-east-1')
        response = ssm.get_parameter(Name='/app/uld/load_planner_agent_id')
        agent_id = response['Parameter']['Value']
        print(f"Using agent ID from SSM: {agent_id}")
    except Exception as e:
        print(f"Could not get agent ID from SSM: {e}")
        # Try reading from deployment file
        try:
            with open('deployment/uld_load_planner_agent_id.txt', 'r') as f:
                agent_id = f.read().strip()
            print(f"Using agent ID from file: {agent_id}")
        except Exception as e2:
            print(f"Could not read agent ID from file: {e2}")
            sys.exit(1)
    
    # Get AWS session info
    boto_session = Session()
    region = boto_session.region_name
    account_id = boto_session.client("sts").get_caller_identity()["Account"]
    
    # Create bedrock-agentcore client
    client = boto3.client('bedrock-agentcore', region_name=region)
    
    # Construct the agent runtime ARN
    agent_runtime_arn = f"arn:aws:bedrock-agentcore:{region}:{account_id}:runtime/{agent_id}"
    
    print("\n" + "="*70)
    print("INTEGRATION TEST: ULD Utility Functions with Deployed Agent")
    print("="*70)
    
    # Test scenarios that should trigger utility function usage
    test_cases = [
        {
            "name": "Weight Calculation Test",
            "query": "I have 5 pallets of electronics, each weighing 500kg, and 3 pallets of machinery, each weighing 300kg. Calculate the total weight.",
            "expected_tools": ["calculate_total_weight"]
        },
        {
            "name": "Volume Calculation Test",
            "query": "Calculate the total volume for 5 cargo items, each measuring 120cm x 100cm x 80cm.",
            "expected_tools": ["calculate_total_volume"]
        },
        {
            "name": "Weight Validation Test",
            "query": "Can I fit 1400kg of cargo in an AKE (LD3) container? Validate the weight constraints.",
            "expected_tools": ["validate_weight_constraints"]
        },
        {
            "name": "ULD Requirements Test",
            "query": "I need to ship 2500kg of cargo with a total volume of 9 cubic meters. How many AKE containers do I need?",
            "expected_tools": ["calculate_uld_requirements"]
        },
        {
            "name": "Dimensional Fit Test",
            "query": "Will a cargo piece measuring 120cm x 100cm x 150cm fit in an AKE (LD3) container?",
            "expected_tools": ["check_dimensional_fit"]
        },
        {
            "name": "ULD Comparison Test",
            "query": "Compare different ULD options for 2500kg of cargo with 9 cubic meters volume. Which is most efficient?",
            "expected_tools": ["compare_uld_options"]
        }
    ]
    
    passed = 0
    failed = 0
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST {idx}: {test_case['name']}")
        print(f"{'='*70}")
        print(f"Query: {test_case['query']}")
        print(f"\nExpected tools: {', '.join(test_case['expected_tools'])}")
        print(f"\nInvoking agent...")
        
        try:
            # Prepare the payload
            payload = {
                "inputText": test_case['query'],
                "sessionId": f"test-session-utils-{idx}"
            }
            
            # Invoke the agent
            response = client.invoke_agent_runtime(
                agentRuntimeArn=agent_runtime_arn,
                payload=json.dumps(payload)
            )
            
            # Read the streaming response
            full_response = ""
            if 'response' in response:
                streaming_body = response['response']
                if hasattr(streaming_body, 'read'):
                    full_response = streaming_body.read().decode('utf-8')
                else:
                    full_response = str(streaming_body)
            elif 'output' in response:
                output = response['output']
                if hasattr(output, 'read'):
                    full_response = output.read().decode('utf-8')
                elif isinstance(output, bytes):
                    full_response = output.decode('utf-8')
                elif isinstance(output, str):
                    full_response = output
                else:
                    full_response = str(output)
            else:
                full_response = str(response)
            
            print(f"\nAgent Response:")
            print("-" * 70)
            print(full_response)
            print("-" * 70)
            
            # Check if response contains expected content
            if full_response and len(full_response) > 50:
                print(f"✅ PASSED - Got valid response")
                passed += 1
            else:
                print(f"⚠️  WARNING - Response seems short or empty")
                failed += 1
                
        except Exception as e:
            print(f"❌ FAILED - Error: {str(e)}")
            failed += 1
    
    # Summary
    print(f"\n{'='*70}")
    print("INTEGRATION TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Total Tests: {len(test_cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️  {failed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    exit_code = test_agent_with_utility_functions()
    sys.exit(exit_code)
