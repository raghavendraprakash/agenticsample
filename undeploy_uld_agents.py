#!/usr/bin/env python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

"""
Undeploy ULD Load Planner Multi-Agent System from AWS Bedrock AgentCore Runtime.

This script removes the ULD Load Planner orchestrator agent from Amazon Bedrock
AgentCore Runtime and cleans up associated AWS resources including:
- Agent deployments on AgentCore Runtime
- SSM Parameter Store entries
- Local deployment files

The undeployment uses the bedrock-agentcore-starter-toolkit Runtime class to:
- Retrieve agent IDs from SSM Parameter Store
- Undeploy agents from AgentCore Runtime
- Clean up SSM parameters
- Remove local deployment files
"""

from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session
import boto3
import utils
import os
import sys
from typing import Optional, List


def undeploy_agent(agent_id: str) -> bool:
    """
    Remove an agent from AWS Bedrock AgentCore Runtime.
    
    This function undeploys an agent from AgentCore Runtime, removing
    the agent deployment and associated resources.
    
    Args:
        agent_id: Agent ID to undeploy
        
    Returns:
        True if undeployment was successful, False otherwise
        
    Raises:
        Exception: If undeployment fails due to AWS permissions, network issues,
                   or invalid agent ID
                   
    Example:
        >>> success = undeploy_agent("agent-abc123")
        >>> if success:
        ...     print("Agent undeployed successfully")
    """
    boto_session = Session()
    region = boto_session.region_name
    
    print(f"\n{'='*60}")
    print(f"Undeploying Agent: {agent_id}")
    print(f"{'='*60}")
    print(f"Region: {region}")
    print()
    
    try:
        # Configure AgentCore Runtime
        print(f"🔧 Configuring AgentCore Runtime...")
        agentcore_runtime = Runtime()
        print()
        
        # Undeploy agent
        print(f"🗑️  Undeploying agent {agent_id}...")
        agentcore_runtime.undeploy(agent_id=agent_id)
        print("✅ Agent undeployed successfully!")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error undeploying agent {agent_id}: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False


def cleanup_ssm_parameters() -> None:
    """
    Remove SSM parameters created during deployment.
    
    This function removes all SSM Parameter Store entries that were
    created during the ULD agent deployment process.
    
    The following parameters are removed:
    - /app/uld/load_planner_agent_id
    
    Raises:
        Exception: If SSM parameter deletion fails
        
    Example:
        >>> cleanup_ssm_parameters()
        SSM parameters cleaned up successfully
    """
    ssm = boto3.client("ssm")
    
    print(f"\n{'='*60}")
    print("Cleaning up SSM Parameters")
    print(f"{'='*60}")
    print()
    
    # List of SSM parameters to clean up
    ssm_parameters = [
        "/app/uld/load_planner_agent_id"
    ]
    
    for param_name in ssm_parameters:
        try:
            print(f"🗑️  Deleting SSM parameter: {param_name}")
            ssm.delete_parameter(Name=param_name)
            print(f"✅ Deleted: {param_name}")
        except ssm.exceptions.ParameterNotFound:
            print(f"⚠️  Parameter not found (already deleted): {param_name}")
        except Exception as e:
            print(f"❌ Error deleting parameter {param_name}: {str(e)}")
    
    print()


def cleanup_local_files() -> None:
    """
    Remove local deployment files.
    
    This function removes local files created during deployment,
    including agent ID files in the deployment directory.
    
    Example:
        >>> cleanup_local_files()
        Local deployment files cleaned up
    """
    print(f"\n{'='*60}")
    print("Cleaning up Local Files")
    print(f"{'='*60}")
    print()
    
    # List of local files to clean up
    local_files = [
        "deployment/uld_load_planner_agent_id.txt"
    ]
    
    for file_path in local_files:
        try:
            if os.path.exists(file_path):
                print(f"🗑️  Deleting local file: {file_path}")
                os.remove(file_path)
                print(f"✅ Deleted: {file_path}")
            else:
                print(f"⚠️  File not found (already deleted): {file_path}")
        except Exception as e:
            print(f"❌ Error deleting file {file_path}: {str(e)}")
    
    print()


def cleanup_iam_role(agent_name: str) -> None:
    """
    Remove IAM role created for the agent.
    
    This function removes the IAM role and associated policies that were
    created during agent deployment.
    
    Args:
        agent_name: Name of the agent (used to construct role name)
        
    Example:
        >>> cleanup_iam_role("Uld_Load_Planner_Agent")
        IAM role cleaned up successfully
    """
    iam_client = boto3.client('iam')
    role_name = f'agentcore-{agent_name.lower()}-role'
    
    print(f"\n{'='*60}")
    print(f"Cleaning up IAM Role: {role_name}")
    print(f"{'='*60}")
    print()
    
    try:
        # First, delete inline policies
        print(f"🗑️  Deleting inline policies for role: {role_name}")
        try:
            iam_client.delete_role_policy(
                RoleName=role_name,
                PolicyName="AgentCorePolicy"
            )
            print(f"✅ Deleted inline policy: AgentCorePolicy")
        except iam_client.exceptions.NoSuchEntityException:
            print(f"⚠️  Inline policy not found (already deleted)")
        
        # Then delete the role
        print(f"🗑️  Deleting IAM role: {role_name}")
        iam_client.delete_role(RoleName=role_name)
        print(f"✅ Deleted IAM role: {role_name}")
        
    except iam_client.exceptions.NoSuchEntityException:
        print(f"⚠️  IAM role not found (already deleted): {role_name}")
    except Exception as e:
        print(f"❌ Error deleting IAM role {role_name}: {str(e)}")
        print(f"⚠️  You may need to manually delete this role from the AWS Console")
    
    print()


def undeploy_all_agents() -> None:
    """
    Undeploy all ULD agents and clean up resources.
    
    This function orchestrates the complete undeployment process:
    1. Retrieves agent IDs from SSM Parameter Store
    2. Undeploys each agent from AgentCore Runtime
    3. Cleans up SSM parameters
    4. Removes local deployment files
    5. Cleans up IAM roles
    
    The function continues attempting to clean up remaining resources
    even if some operations fail, ensuring maximum cleanup.
    
    Example:
        >>> undeploy_all_agents()
        All agents undeployed and resources cleaned up
    """
    print("\n" + "="*60)
    print("ULD Load Planner Multi-Agent System Undeployment")
    print("="*60)
    print()
    
    # Track success/failure
    undeploy_success = True
    
    # Retrieve agent ID from SSM Parameter Store
    ssm_param_name = "/app/uld/load_planner_agent_id"
    agent_id = None
    
    try:
        print(f"📋 Retrieving agent ID from SSM: {ssm_param_name}")
        agent_id = utils.get_ssm_parameter(ssm_param_name)
        print(f"✅ Found agent ID: {agent_id}")
        print()
    except Exception as e:
        print(f"⚠️  Could not retrieve agent ID from SSM: {str(e)}")
        print(f"⚠️  Will attempt to clean up other resources")
        print()
        undeploy_success = False
    
    # Undeploy agent if we have an agent ID
    if agent_id:
        success = undeploy_agent(agent_id)
        if not success:
            undeploy_success = False
            print(f"⚠️  Agent undeployment failed, but continuing with cleanup...")
            print()
    
    # Clean up SSM parameters (always attempt this)
    try:
        cleanup_ssm_parameters()
    except Exception as e:
        print(f"❌ Error during SSM cleanup: {str(e)}")
        undeploy_success = False
    
    # Clean up local files (always attempt this)
    try:
        cleanup_local_files()
    except Exception as e:
        print(f"❌ Error during local file cleanup: {str(e)}")
        undeploy_success = False
    
    # Clean up IAM role (always attempt this)
    try:
        cleanup_iam_role("Uld_Load_Planner_Agent")
    except Exception as e:
        print(f"❌ Error during IAM role cleanup: {str(e)}")
        undeploy_success = False
    
    # Print undeployment summary
    print("\n" + "="*60)
    print("Undeployment Summary")
    print("="*60)
    print()
    
    if undeploy_success:
        print("✅ All agents undeployed and resources cleaned up successfully!")
        print()
        print("📋 Cleaned up resources:")
        print("  - AgentCore Runtime agent deployment")
        print("  - SSM Parameter Store entries")
        print("  - Local deployment files")
        print("  - IAM roles and policies")
        print()
    else:
        print("⚠️  Undeployment completed with some errors")
        print()
        print("📋 Some resources may require manual cleanup:")
        print("  - Check AWS Console for remaining AgentCore agents")
        print("  - Check SSM Parameter Store for /app/uld/* parameters")
        print("  - Check IAM for agentcore-uld_load_planner_agent-role")
        print()
        print("💡 Manual cleanup instructions:")
        print("  1. AWS Console > Bedrock > AgentCore > Agents")
        print("  2. AWS Console > Systems Manager > Parameter Store")
        print("  3. AWS Console > IAM > Roles")
        print()


if __name__ == "__main__":
    """
    Main entry point for ULD agent undeployment.
    
    Usage:
        python undeploy_uld_agents.py
        
    Prerequisites:
        - AWS credentials configured
        - Python 3.11 virtual environment activated
        - bedrock-agentcore-starter-toolkit installed
        - Required IAM permissions for AgentCore, SSM, and IAM
    """
    try:
        print("\n⚠️  WARNING: This will undeploy all ULD agents and clean up resources!")
        print("Press Ctrl+C to cancel, or Enter to continue...")
        input()
        
        undeploy_all_agents()
        print("\n🎉 Undeployment process completed!")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️  Undeployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Undeployment failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
