Of course. Here is a professional and well-structured `README.md` file crafted from your report. It is designed to be clear, informative, and engaging for visitors to your GitHub repository.

---

# Heterogeneous Multi-Agent System with Dynamic LLM Selection

![License](https://img.shields.io/badge/License-MIT-blue.svg) [![Multi-Agent Systems](https://img.shields.io/badge/Field-Multi--Agent_Systems-green)](https://github.com/topics/multi-agent-systems) [![LLM](https://img.shields.io/badge/Technology-LLM-orange)](https://github.com/topics/llm)

This repository contains the research and implementation for a novel framework that enhances **Multi-Agent Systems (MAS)** by dynamically selecting the most optimal **Large Language Model (LLM)** for each task, overcoming the limitations of traditional homogeneous systems.

Developed during an internship at **Ericsson Research**, this work addresses key challenges in AI-driven telecommunications, such as network optimization and deploying intelligence in resource-constrained environments.

## 🧠 Problem Statement

Traditional homogeneous MAS rely on a single LLM for all agents, which introduces significant limitations:
*   **Inherent Model Biases:** The system inherits all the biases and blind spots of the single LLM.
*   **Inconsistent Performance:** A single model cannot be optimal across all domains (e.g., coding, law, medicine).
*   **Constrained Collective Intelligence:** Limits the system's ability to leverage specialized expertise.
*   **Hindered Error Correction:** Reduces the system's robustness and ability to self-correct.

## 💡 Proposed Solution

We propose a dynamic, Agentic AI framework that intelligently routes tasks within a MAS to the best-suited LLM from a diverse, heterogeneous pool.

**Core Innovation:** An LLM-powered **orchestrator agent** that uses real-time performance data to make intelligent LLM selection decisions, automating the process identified as a manual gap in prior research (e.g., the X-MAS paper).

## ⚙️ Key Components

### 1. Extended Benchmark Test Suite (`X-MAS-Bench-Extended`)
We extended the existing X-MAS-Bench with new domains and comprehensive metrics to thoroughly evaluate LLM performance.

| Domain | Number of Queries | Status |
| :--- | :--- | :--- |
| Coding | 3,495 | Original |
| Finance | 2,120 | Original |
| **General-Knowledge** | **2,919** | **New** |
| **Law** | **208** | **New** |
| Mathematics | 1,792 | Original |
| Medical | 2,550 | Original |
| **Research** | **43** | **New** |
| Science | 2,349 | Original |

**Total Evaluations:** ~2.09 million (query × function × model), surpassing the original benchmark.

**Tracked Metrics:** Accuracy, Latency, Peak Memory, Prompt/Completion Tokens, and Throughput.

### 2. Agentic AI Orchestrator
An intelligent agent (built with **LangGraph**) that decides which LLM to assign to a given task based on:
*   **Task Domain/Sub-domain** (e.g., "Medical", "Python Coding")
*   **Performance Metrics** (Accuracy, Latency, Cost)
*   **Resource Constraints** (e.g., available memory on an edge device)

### 3. Model Context Protocol (MCP) Integration
The **MCP server** acts as the central knowledge base for the orchestrator, hosting a detailed score matrix of LLM performance across all domains and metrics.
*   **Analogy:** MCP is like USB-C for LLMs—a standard protocol for connecting models to data and tools.
*   **Function:** The orchestrator agent queries the MCP server via tool calls to access the latest performance data before making a selection.

## 🚀 Architecture & Workflow

### High-Level Agent Workflow
1.  **Receive Input:** The MAS receives a user query.
2.  **Query MCP:** The orchestrator agent queries the MCP server for available domains and LLM performance data.
3.  **Domain Mapping:** The query is mapped to its relevant domain and sub-domain.
4.  **Score Calculation:** A weighted score is computed for each candidate LLM based on task priorities (e.g., high accuracy vs. low latency).
5.  **LLM Selection & Assignment:** The optimal LLM is selected and assigned to the agent responsible for the task.
6.  **Response:** The result is returned through the MAS pipeline.

### Integration with MAS
The dynamic selector seamlessly integrates into existing MAS topologies (e.g., `X-MAS-Proto`), intercepting tasks and assigning the best LLM for each step in a pipeline (Planning → QA → Revision → Aggregation → Evaluation).

*(Insert schematic diagrams from your report here, e.g., `Figure 3: Agent Workflow`, `Figure 4: MAS Integration`)*

## 📊 Comparative Analysis: Agentic AI vs. Multi-Armed Bandits (MAB)

| Feature | **Agentic AI (Our Approach)** | **Multi-Armed Bandits (MAB)** |
| :--- | :--- | :--- |
| **Decision Process** | Interpretable, reasoning-based | Statistical, black-box |
| **Flexibility** | High; can incorporate complex constraints (e.g., cost, memory) | Medium; primarily optimizes for a single reward metric |
| **Adaptability** | Excels in dynamic environments with new tasks/domains | Slower to adapt to completely new contexts |
| **Initialization** | Can leverage pre-existing benchmark data (warm-start) | Requires a cold-start or exploration phase |

## 🚧 Progress & Future Directions

*   **Completed:** Implementation of the Agentic AI orchestrator, conceptual comparison with MAB approaches, and extension of the benchmark suite.
*   **Initial Results:** Demonstrates superior adaptability and interpretability in dynamic task environments.
*   **Future Work:**
    *   Automated LLM discovery and onboarding.
    *   Enhanced explainability for the orchestrator's decisions.
    *   Training specialized MAS-specific agents.
    *   Deployment and testing on edge devices (e.g., smartphones, Raspberry Pis).

## 📚 Citation & Related Work

This work builds upon and extends the foundational research presented in the **X-MAS paper**. It also leverages the open standard **Model Context Protocol (MCP)**.

For related advancements, please see:
*   [X-MAS Paper] (Link to be added)
*   [MCP Universe: Evaluating LLMs with Real-World MCP Servers - Salesforce AI Research](https://arxiv.org/abs/2406.07528)
*   Reinforcement Learning for dynamic agent assignment.
*   Projects on deploying LLMs/SLMs to edge devices.

## 📝 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

## 👨‍💻 Author

Developed as part of an AI Research Internship at **Ericsson Research**.

---

**Disclaimer:** This project is a research prototype. The code and models are intended for experimental use.
