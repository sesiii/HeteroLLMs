Multi-Agent Systems with Dynamic LLM Selection
This repository documents my work as an AI Research Intern at Ericsson Research, focusing on advancing Multi-Agent Systems (MAS) through the integration of heterogeneous Large Language Models (LLMs). The project addresses the limitations of homogeneous MAS, which rely on a single LLM and are constrained by uniform model biases and inconsistent performance across domains. Our solution introduces a dynamic LLM selection framework powered by Agentic AI, leveraging the diverse strengths of multiple LLMs to optimize MAS performance.
Project Overview
The goal of this project is to enhance MAS by developing a novel framework for dynamic LLM selection, inspired by the X-MAS paper. This framework automates LLM assignment using Agentic AI, improving collective intelligence and error correction in MAS. Key contributions include:

Foundational Research: Exploring concepts of AI agents, MAS, and the Model Context Protocol (MCP).
Test Bench Development: Extending the X-MAS-Bench with new domains and comprehensive metrics.
Agentic AI Framework: Implementing an LLM-powered agent for dynamic LLM selection.
Experimental Evaluations: Demonstrating improved accuracy and efficiency in MAS performance.
Future Directions: Proposing advancements like automated LLM discovery and enhanced explainability.

This work aligns with Ericsson’s mission to innovate in AI-driven telecommunications, with potential applications in network optimization and resource-constrained environments.
Model Context Protocol (MCP)
The MCP is an open-standard protocol that standardizes context provision to LLMs, similar to USB-C for peripheral connectivity. It enables seamless integration of LLMs with external data sources and tools.
MCP Architecture

Clients: Applications (e.g., chatbots, agents) that query LLMs.
Servers: Provide structured data (resources) and callable functions (tools).

Operational Workflow

User submits a query to an LLM-agent.
Agent identifies and selects relevant tools.
Tools are executed via the MCP server.
Results are returned to the agent.
LLM formulates a response based on the results.

Use Case
For real-time queries (e.g., weather data), MCP enables agents to access external sources, reducing hallucinations and improving accuracy. In this project, MCP hosts a score matrix of LLM performance metrics, queried by agents for dynamic LLM selection.
Proposed Test Bench
The proposed test bench extends the X-MAS-Bench by adding new domains (General-Knowledge, Law, Research) and incorporating additional performance metrics beyond accuracy.
Benchmark Dataset Structure



Domain
Number of Queries



Coding
3,495


Finance
2,120


General-Knowledge
2,919 (new)


Law
208 (new)


Mathematics
1,792


Medical
2,550


Research
43 (new)


Science
2,349


Total Evaluations: ~15,476 queries × 5 functions × 27 models ≈ 2.09 million evaluations, surpassing the 1.7 million evaluations in X-MAS-Bench.
Metrics

Latency (ms): Wall-clock time from HTTP request to response.
Peak Memory (MB): Maximum resident set size during a call.
Prompt Tokens: Number of tokens in the input prompt.
Completion Tokens: Number of tokens in the generated response.
Total Tokens: Sum of prompt and completion tokens.
Throughput (tokens/sec): Total tokens divided by latency.

Agentic AI Solution
The Agentic AI framework dynamically selects optimal LLMs for MAS agents, addressing the manual assignment gap in X-MAS-Design.
Key Features

Integration: Seamlessly integrates with existing MAS frameworks (e.g., X-MAS-Proto).
MCP Utilization: Queries a score matrix of LLM performance metrics via MCP.
Workflow:
Receive input query.
Fetch available domains and models via MCP.
Map query to domain/sub-domain.
Collect performance metrics (e.g., accuracy, latency).
Compute weighted score based on task requirements.
Select optimal LLM and assign to agent.



Implementation

Built with LangGraph for interpretable decision-making.
Incorporates reinforcement learning-like feedback for iterative improvement.
Outperforms alternative approaches like Multi-Armed Bandits (MAB) in dynamic task environments.

Repository Structure

/src: Source code for the Agentic AI framework and dynamic LLM selection.
/data: Benchmark dataset files organized by domain and sub-domain.
/docs: Documentation, including schematics and experimental results.
/tests: Scripts for running evaluations and analyzing metrics.
/notebooks: Jupyter notebooks for exploratory analysis and prototyping.

Installation

Clone the repository:git clone https://github.com/your-username/your-repo-name.git


Install dependencies:pip install -r requirements.txt


Set up the MCP server (refer to /docs/mcp_setup.md for instructions).
Run the test bench:python tests/run_benchmarks.py



Usage

Configure the MCP server with the score matrix of LLM performance metrics.
Run the Agentic AI framework:python src/agentic_ai.py --query "your_query_here"


Analyze results in /results or through provided Jupyter notebooks.

Results
Initial experiments demonstrate:

Improved Accuracy: Dynamic LLM selection outperforms homogeneous MAS by leveraging diverse model strengths.
Enhanced Efficiency: Optimized latency and token usage in resource-constrained environments.
Scalability: Seamless integration with existing MAS topologies (e.g., X-MAS-Proto).

Detailed results and visualizations are available in /docs/results.md.
Related Advancements

MCP Universe: Salesforce AI Research’s evaluation of LLMs with real-world MCP servers.
Reinforcement Learning: RL-based approaches for dynamic agent assignment.
Edge Deployment: Deploying LLMs/SLMs to edge devices like smartphones and Raspberry PIs.
Dynamic Routing: Automating manual routing systems like MASRouter.

Future Directions

Automated LLM Discovery: Enable agents to discover new LLMs dynamically.
Enhanced Explainability: Improve transparency in LLM selection decisions.
MAS-Specific Agents: Train specialized agents for domain-specific tasks.
Edge Optimization: Further optimize for resource-constrained environments.

Contributing
Contributions are welcome! Please submit pull requests or open issues for bugs, feature requests, or improvements. Follow the guidelines in CONTRIBUTING.md.
License
This project is licensed under the MIT License. See LICENSE for details.
Acknowledgments

Ericsson Research: For providing the opportunity and resources to conduct this research.
X-MAS Paper Authors: For foundational insights and benchmarks.
Salesforce AI Research: For contributions to the MCP Universe.
