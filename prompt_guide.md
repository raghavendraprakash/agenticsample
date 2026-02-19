## – For Reference Only – 

General instruction:

*   Agentic analysis is paramount
*   Design your agentic system on the table first
*   You may use the project code base structure as reference and template, modify accordingly without using any AI IDE assitance
*   In case you want to try out with KIRO, below are the references that may help you.

**Multi-Agent system \[Spec driven\]**

Create a multi-agent system considering the implementation code references for the requirements in #samplecase.md . Keep it very simple, avoid too many requirements (keep it 1 or 2), use bedrock-agentcore runtime, test only the agents deployed on AgentCore on AWS. Do not overwhelm with unnecessary documentation, code, and tasks. Just keep the tasks to development of relevant agents, creation of deployment/un-deployment scripts. Execute the tasks and create artifacts with the prefix "uld\_". Use Python3.11 virtual environment. Just focus on agent development and deployment.

**UI Layer \[Vibe code\] - Use this to create UI layer for your backend agentic**

Create UI layer without creating overwhelming documentation in the folder "uld\_ui" with React JS framework as frontend, and FlaskAPI backend server, a python based framework that connects to AgentCore endpoint of agent with name \<uld\_load\_planner\_agent> and ARN arn:aws:bedrock-agentcore:us-east-1:153264177053:runtime/\<uld\_load\_planner\_agent-4IYK1O4xnZ>

## – Powering your agentic with Knowledge base --

### **Synthetic data creation \[Do it in consultation with your product specialists\]**

\[You may use Vibe coding\] 

For the #samplecase.md create sample files with relevant synthetic data in .txt format in a folder called "uld\_data"

### **Amazon KnowledgeBases \[Manual creation\] – For hackathon, create through AWS console, note down KB\_ID**

[s3://\<bucket-name>/uld-knowledege-base/ ](https://us-east-1.console.aws.amazon.com/s3/buckets/rpbktuse1/uld-knowledege-base/?region=us-east-1) \[Once you are ready with synthetic data, upload to the bucket and sync KB data source\]

*   ARN of AKB ID \[Note down, E.g SCRX8H16LS\]
*   Set as environment variable: export KB\_ID=SCRX8H16LS (export KB\_ID=SCRX8H16LS as environment variable)

**\[If you are using KIRO vibe coding, extend the basic agent development with KB integration\]**

Integrate with KB\_ID using retrieve from strands-tools as implemented in educational\_assistant\_agent.py into uld agents to use Knowledge base as tool as required. Test the agents to see if knowledge base integration is complete.