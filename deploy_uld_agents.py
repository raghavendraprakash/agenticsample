#!/usr/bin/env python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""
Deploy ULD Load Planner Multi-Agent System to AWS Bedrock AgentCore Runtime.

This script deploys the ULD Load Planner orchestrator agent to Amazon Bedrock
AgentCore Runtime. The orchestrator coordinates with two specialist agents:
1. Uld_Pattern_Analysis_Agent - Analyzes cargo patterns
2. Uld_Allocation_Recommendation_Agent - Provides allocation recommendations

The deployment uses the bedrock-agentcore-starter-toolkit Runtime class to:
- Configure the agent with the runtime entrypoint
- Create necessary IAM roles and permissions
- Deploy to AgentCore Runtime
- Store agent IDs in SSM Parameter Store for reference
"""

from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session
import utils
from dotenv import load_dotenv
import os
import sys
from typing import Dict, Optional

# Load environment variables from .env file
load_dotenv()


def deploy_agent(agent_name: str, runtime_file: str) -> Optional[str]:
    """
    Deploy an agent to AWS Bedrock AgentCore Runtime.
    
    This function configures and launches an agent on AgentCore Runtime,
    creating necessary IAM roles and ECR repositories automatically.
    
    Args:
        agent_name: Name of the agent (with Uld_ prefix per requirements)
        runtime_file: Path to the runtime Python file (relative to project root)
        
    Returns:
        Agent ID from deployment, or None if deployment fails
        
    Raises:
        Exception: If deployment fails due to AWS permissions, network issues,
                   or invalid configuration
                   
    Example:
        >>> agent_id = deploy_agent(
        ...     "Uld_Load_Planner_Agent",
        ...     "src/agents/uld_load_planner_runtime.py"
        ... )
        >>> print(f"Deployed agent: {agent_id}")
    """
    boto_session = Session()
    region = boto_session.region_name
    account_id = boto_session.client("sts").get_caller_identity()["Account"]
    
    print(f"\n{'='*60}")
    print(f"Deploying Agent: {agent_name}")
    print(f"{'='*60}")
    print(f"Region: {region}")
    print(f"Account: {account_id}")
    print(f"Runtime File: {runtime_file}")
    print()
    
    try:
        # Create IAM role for AgentCore
        print(f"🔧 Creating IAM role for {agent_name}...")
        agentcore_role = utils.create_agentcore_role(agent_name.lower())
        role_arn = agentcore_role['Role']['Arn']
        print(f"✅ IAM role created: {role_arn}")
        print()
        
        # Configure AgentCore Runtime
        print(f"🔧 Configuring AgentCore Runtime...")
        agentcore_runtime = Runtime()
        
        response = agentcore_runtime.configure(
            entrypoint=runtime_file,
            execution_role=role_arn,
            auto_create_ecr=True,
            requirements_file="requirements.txt",
            region=region,
            agent_name=agent_name
        )
        print("✅ Configuration successful!")
        print(f"Configuration response: {response}")
        print()
        
        # Launch agent
        print(f"🚀 Launching agent {agent_name}...")
        launch_result = agentcore_runtime.launch(
            auto_update_on_conflict=True
        )
        print("✅ Launch successful!")
        print()
        
        # Extract agent ID
        agent_id = None
        if hasattr(launch_result, 'agent_id'):
            agent_id = launch_result.agent_id
            print(f"📝 Agent ID: {agent_id}")
        else:
            print("⚠️ Warning: Could not extract agent_id from launch_result")
            print(f"Available attributes: {[attr for attr in dir(launch_result) if not attr.startswith('_')]}")
        
        # Extract agent ARN
        if hasattr(launch_result, 'agent_arn'):
            agent_arn = launch_result.agent_arn
            print(f"📝 Agent ARN: {agent_arn}")
        
        return agent_id
        
    except Exception as e:
        print(f"❌ Error deploying {agent_name}: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None


def deploy_all_agents() -> Dict[str, str]:
    """
    Deploy all ULD agents to AWS Bedrock AgentCore Runtime.
    
    This function deploys the ULD Load Planner orchestrator agent and stores
    the agent ID in SSM Parameter Store for later reference and testing.
    
    The deployment process:
    1. Deploys the Load Planner orchestrator (which includes specialist agents as tools)
    2. Stores agent ID in SSM Parameter Store
    3. Outputs agent IDs to console for testing
    4. Creates deployment directory with agent ID files
    
    Returns:
        Dictionary mapping agent names to agent IDs
        
    Example:
        >>> agent_ids = deploy_all_agents()
        >>> print(f"Load Planner ID: {agent_ids['Uld_Load_Planner_Agent']}")
    """
    print("\n" + "="*60)
    print("ULD Load Planner Multi-Agent System Deployment")
    print("="*60)
    print()
    
    agent_ids = {}
    
    # Deploy Load Planner orchestrator
    # Note: The specialist agents (Pattern Analysis and Allocation Recommendation)
    # are embedded as tools within the orchestrator, so we only deploy the orchestrator
    agent_name = "Uld_Load_Planner_Agent"
    runtime_file = "src/agents/uld_load_planner_runtime.py"
    
    agent_id = deploy_agent(agent_name, runtime_file)
    
    if agent_id:
        agent_ids[agent_name] = agent_id
        
        # Store agent ID in SSM Parameter Store
        ssm_param_name = "/app/uld/load_planner_agent_id"
        try:
            print(f"\n💾 Storing agent ID in SSM Parameter Store...")
            print(f"Parameter: {ssm_param_name}")
            utils.put_ssm_parameter(ssm_param_name, agent_id)
            print(f"✅ Agent ID stored in SSM: {ssm_param_name}")
        except Exception as e:
            print(f"⚠️ Warning: Could not store agent ID in SSM: {str(e)}")
        
        # Save agent ID to local file
        try:
            os.makedirs("deployment", exist_ok=True)
            id_file = "deployment/uld_load_planner_agent_id.txt"
            with open(id_file, "w") as f:
                f.write(agent_id)
            print(f"✅ Agent ID saved to: {id_file}")
        except Exception as e:
            print(f"⚠️ Warning: Could not save agent ID to file: {str(e)}")
    else:
        print(f"❌ Failed to deploy {agent_name}")
        sys.exit(1)
    
    # Print deployment summary
    print("\n" + "="*60)
    print("Deployment Summary")
    print("="*60)
    print()
    
    if agent_ids:
        print("✅ Successfully deployed agents:")
        for name, agent_id in agent_ids.items():
            print(f"  - {name}: {agent_id}")
        print()
        print("📋 Agent IDs stored in:")
        print(f"  - SSM Parameter Store: /app/uld/load_planner_agent_id")
        print(f"  - Local file: deployment/uld_load_planner_agent_id.txt")
        print()
        print("🧪 Test the agent:")
        print('  python test_deployed_uld_agents.py')
        print()
    else:
        print("❌ No agents were successfully deployed")
        sys.exit(1)
    
    return agent_ids


if __name__ == "__main__":
    """
    Main entry point for ULD agent deployment.
    
    Usage:
        python deploy_uld_agents.py
        
    Prerequisites:
        - AWS credentials configured
        - Python 3.11 virtual environment activated
        - bedrock-agentcore-starter-toolkit installed
        - Required IAM permissions for AgentCore, ECR, and SSM
    """
    try:
        agent_ids = deploy_all_agents()
        print("\n🎉 Deployment completed successfully!")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️ Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Deployment failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
