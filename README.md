# Sample: Multi-Agent implementation with Amazon Bedrock AgentCore
Serves as code template for implementation
Pattern: Agents as tools
Local Python functions as tools that agents can use
Orchestrator agent uses other agents as tools


### Key Components

1. **Orchestrator Agent** - Central coordinator that routes requests to specialized agents
2. **Specialized Agents** - Two domain-specific agents 
3. **Knowledge Base** - Document retrieval for enhanced responses (Sample data is synthetic data set)
   
## What You'll Learn

This sample demonstrates:

- **Multi-agent orchestration** using the "Agents as Tools" pattern
- **Knowledge Base integration** for RAG (Retrieval Augmented Generation)

## Prerequisites

### AWS Account Requirements

- AWS Account with permissions for:
  - Amazon Bedrock models
  - Amazon Bedrock AgentCore Runtime
  - Amazon S3
  - AWS Systems Manager (Parameter Store)
  - AWS IAM

### System Requirements

- **Python**: 3.11 or higher
- **AWS CLI**: Latest version, configured with credentials
- **Operating System**: macOS, Linux, or Windows with WSL

### Required Tools

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Use Python 3.11 virtual environment
# Install Bedrock AgentCore starter toolkit
pip install bedrock-agentcore-starter-toolkit

# Install Python dependencies
pip install -r requirements.txt
```

### AWS Permissions

Your AWS user/role needs permissions for:
- Bedrock model invocation and AgentCore operations
- S3 bucket operations
- IAM role creation and policy attachment
- Systems Manager Parameter Store access

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <url>
cd agenticsample

# Install dependencies
pip install -r requirements.txt

```

### 2. Deploy with One Command

```bash
# Deploy entire system
python deploy_uld_agents.py
```
This deploys:
1. Agent into Bedrock AgentCore runtim

**Deployment time**: ~10-15 minutes

### 3. Test the System

```bash
# Test core AgentCore functionality
python test_deployed_uld_agents.py

### 5. Cleanup When Done

```bash
# Remove all deployed resources
python undeploy_uld_agents.py
```

## Configuration

### Environment Variables

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_PROFILE=default
KB_ID=<KnowledgeBase ID> 
```

### Knowledge Base Documents
Generate synthetic data through prompt inline with samplecase.md
refer to prompt_guide.md
## How It Works

## License

This sample code is provided under the MIT-0 License. See the [LICENSE](LICENSE) file for details.

**Third-Party Dependencies**: This sample uses third-party dependencies with their own licenses. See [THIRD-PARTY-LICENSES](THIRD-PARTY-LICENSES) for details.

---

**Sample Code**: This is sample code and not intended for production use without significant modifications.
