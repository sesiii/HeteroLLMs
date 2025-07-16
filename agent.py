
# from langchain_together import ChatTogether
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain_core.messages import HumanMessage
# from langchain_core.tools import tool
# from langchain.agents import initialize_agent, Tool
# from langchain.agents.agent_types import AgentType
# from langchain_mcp_adapters.tools import to_fastmcp
# from langchain.chat_models import ChatOpenAI
# from langgraph.graph import StateGraph, END
# from typing import TypedDict, Annotated,List
# from langchain_together import ChatTogether
# from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage
# from langchain_openai import ChatOpenAI
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langgraph.checkpoint.memory import MemorySaver
# from langchain_core.tools import tool
# import operator


# class AgentState(TypedDict):
#     messages: Annotated[list[AnyMessage], operator.add] 


# memory = MemorySaver()
# print(f"Checkpointer type: {type(memory)}")


# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.graph import StateGraph, MessagesState, START
# from langgraph.prebuilt import ToolNode, tools_condition
# from langchain.chat_models import init_chat_model


# client = MultiServerMCPClient(
#     {
#         "csv_r": {
#             "command": "uv",
#             "args":  [
#                 "--directory",
#                 "/home/sesi/testing/agents/ER/agentic-ai/experiments/HeteroLLMs/mcp_server/",
#                 "run",
#                 "main.py"
#             ],
#             "transport": "stdio",
#         }

#     }
# )


# class Agent:
#     def __init__(self, model, tools, checkpointer, system=""):
#         self.system = system
#         graph = StateGraph(AgentState)
#         graph.add_node("llm", self.call_llm)
#         graph.add_node("action", self.take_action)
#         graph.add_conditional_edges("llm", self.exists_action, {True: "action", False: END})
#         graph.add_edge("action", "llm")
#         graph.set_entry_point("llm")
#         self.graph = graph.compile(checkpointer=checkpointer)
#         self.tools = {t.name: t for t in tools}
#         self.model = model.bind_tools(tools)

#     def call_llm(self, state: AgentState):
#         messages = state['messages']
#         if self.system:
#             messages = [SystemMessage(content=self.system)] + messages
#         message = self.model.invoke(messages)
#         return {'messages': [message]}

#     def exists_action(self, state: AgentState):
#         result = state['messages'][-1]
#         return len(result.tool_calls) > 0

#     async def take_action(self, state: AgentState):
#         tool_calls = state['messages'][-1].tool_calls
#         results = []
#         for t in tool_calls:
#             print(f"Calling: {t}")
#             result = await self.tools[t['name']].ainvoke(t['args'])
#             results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
#         print("Back to the model!")
#         return {'messages': results}


# prompt = """You must always first retrieve models via the `list_models` tool. If no models match or the result is insufficient, proceed to check available domains for these models, then check subdomains within these domains. You are NOT allowed to answer or assume anything until you have completed this entire reasoning chain. If, after checking models, domains, and subdomains, you still do not have a clear answer, respond explicitly: “No relevant data found in the tools for this query.”
# Make tool calls
# """

# tools = await client.get_tools()
# model= ChatTogether(
#     # model_name="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
#     model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
#     temperature=0.0
# ) 

# agent = Agent(model, tools, checkpointer=memory, system=prompt)
# thread = {"configurable": {"thread_id": "2"}} #Unique thread identifier for the conversation



# messages = [HumanMessage(content="what models are listed in the csv file available in the tools?.")]
# result = await agent.graph.ainvoke({"messages": messages}, thread)
# print(result['messages'][-1].content)




# messages = [HumanMessage(content="which LLM performs better in history( General-Knowledge domain) related queries? and why? show the metrics also only for history")]
# thread = {"configurable": {"thread_id": "2"}} 
# result = await agent.graph.ainvoke({"messages": messages},thread)
# result['messages'][-1].content


# messages = [HumanMessage(content="which LLM would you prefer for tasks related to astronomical distances calculations? ")]
# thread = {"configurable": {"thread_id": "1"}} #existing conversation thread
# result = await agent.graph.ainvoke({"messages": messages},thread)
# result['messages'][-1].content





from langchain_together import ChatTogether
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage, AIMessage
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import TypedDict, Annotated
import operator, json, ast, re

# Agent state definition
typing_domains = list[str]
typing_subdomains = dict[str, list[str]]
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    step: str
    models: list[str]
    domains: typing_domains
    subdomains: typing_subdomains
    query: str
    metrics: dict
    intent: str
    context: str
    selected_llm: str

# Initialize memory and MCP client
memory = MemorySaver()
client = MultiServerMCPClient({
    "csv_r": {
        "command": "uv",
        "args": [
            "--directory",
            "/path/to/mcp_server/",
            "run", "main.py"
        ],
        "transport": "stdio",
    }
})

class Agent:
    def __init__(self, model, tools, checkpointer):
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)
        self.graph = self._build_graph(checkpointer)

    def _build_graph(self, cp):
        g = StateGraph(AgentState)
        g.add_node("init", self.init_step)
        g.add_node("collect_metrics", self.collect_metrics_step)
        g.add_node("respond", self.respond_step)
        g.add_edge("init", "collect_metrics")
        g.add_edge("collect_metrics", "respond")
        g.set_entry_point("init")
        return g.compile(checkpointer=cp)

    def classify_intent(self, query: str) -> str:
        q = query.lower()
        print(f"DEBUG: classify_intent received query: '{q}'")
        if re.search(r"\b(models|list|available)\b", q):
            return "list_models"
        if re.search(r"\b(compare|better|best|prefer|efficient|memory|performance)\b", q):
            return "compare"
        if re.search(r"\b(metrics|performance)\b", q):
            return "metrics"
        return "unknown"

    async def map_query_to_domain_subdomain_llm(self, query, domains, subdomains):
        lines = []
        for d in domains:
            subs = subdomains.get(d, []) or ["None"]
            lines.append(f"- {d}: {', '.join(subs)}")
        prompt = f"""
You are an AI assistant.
Available domains and subdomains:
{chr(10).join(lines)}
User query: \"{query}\"
Respond with exactly:
Domain: <one domain above>
Subdomain: <one subdomain above or None>
"""
        resp = await self.model.ainvoke([HumanMessage(content=prompt)])
        dm = re.search(r"Domain:\s*(\S+)", resp.content)
        sd = re.search(r"Subdomain:\s*(\S+)", resp.content)
        domain = dm.group(1) if dm else None
        sub = sd.group(1) if sd and sd.group(1) != 'None' else None
        print(f"DEBUG: LLM mapping -> domain={domain}, subdomain={sub}")
        return domain, sub, f"LLM mapped to {domain}/{sub or 'None'}"

    def normalize_accuracy(self, v):
        return v/100 if isinstance(v, (int, float)) and v > 1 else v

    def select_best_llm(self, metrics, task):
        comp = metrics.get("comparison", {})
        if not comp: return None, "no comp data"
        best = max(comp.items(), key=lambda x: x[1])[0]
        return best, f"selected {best} for highest accuracy"

    async def init_step(self, state: AgentState):
        query = state["messages"][-1].content
        intent = self.classify_intent(query)
        # fetch tools
        models = await self.tools["list_models"].ainvoke({})
        domains = await self.tools["list_domains"].ainvoke({})
        subdomains = {d: await self.tools["list_sub_domains"].ainvoke({"domain": d}) for d in domains}
        return {"step":"init","query":query,"intent":intent,
                "models":models,"domains":domains,
                "subdomains":subdomains,"context":"","metrics":{},"selected_llm":None,
                "messages":[]}

    async def collect_metrics_step(self, state: AgentState):
        q = state["query"]
        intent = state["intent"]
        metrics, msgs = {}, []
        dom, sub, reason = await self.map_query_to_domain_subdomain_llm(
            q, state["domains"], state["subdomains"]
        )
        msgs.append(ToolMessage(tool_call_id="map", name="mapping", content=reason))

        def parse(r):
            try: d = r if isinstance(r, dict) else json.loads(r)
            except: d = ast.literal_eval(r) if isinstance(r, str) else {}
            if isinstance(d, dict) and "accuracy" in d:
                d["accuracy"] = self.normalize_accuracy(d["accuracy"])
            return d

        # comparison
        if intent in ["compare","metrics"] and dom:
            if re.search(r"\b(compare|better|best|prefer|efficient|memory)\b", q):
                call = ("compare_models_domain_subdomain" if sub
                        else "compare_models_domain")
                args = {"domain":dom}
                if sub: args["sub_domain"] = sub
                res = await self.tools[call].ainvoke(args)
                comp = parse(res)
                metrics["comparison"] = {m:self.normalize_accuracy(a) for m,a in comp.items()} if isinstance(comp,dict) else {}
                msgs.append(ToolMessage(tool_call_id="cmp", name=call, content=str(comp)))
                best, reason = self.select_best_llm(metrics, sub or dom)
                state["selected_llm"], state["context"] = best, reason

            if re.search(r"\bmetrics\b", q):
                for m in state["models"]:
                    call = "get_metric_domain_subdomain" if sub else "get_metric_domain"
                    args = {"model":m, "domain":dom}
                    if sub: args["sub_domain"] = sub
                    res = await self.tools[call].ainvoke(args)
                    parsed = parse(res)
                    key = f"{m}_{dom}_{sub}" if sub else f"{m}_{dom}"
                    metrics[key] = parsed
                    msgs.append(ToolMessage(tool_call_id=key, name=call, content=str(parsed)))

        return {"step":"metrics","metrics":metrics,
                "messages":msgs,"selected_llm":state["selected_llm"],
                "context":state["context"]}

    async def respond_step(self, state: AgentState):
        resp = "Based on the analysis and context:\n"
        if state["metrics"].get("comparison"):
            cmp = state["metrics"]["comparison"]
            best = max(cmp, key=cmp.get)
            resp += (f"Best model: {best} (acc={cmp[best]:.2f})\n")
        else:
            resp += "No data found. Try a related domain/subdomain."
        return {"step":"done","messages":[AIMessage(content=resp)]}

# Main entrypoint
async def main():
    tools = await client.get_tools()
    model = ChatTogether(model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", temperature=0.0)
    agent = Agent(model, tools, checkpointer=memory)

    queries = [
        "How do metrics compare for Combinatorics across both models and which one is more efficient in memory usage?"
    ]
    state = {"messages":[],"step":"init","models":[],"domains":[],
             "subdomains":{},"query":"","metrics":{},
             "intent":"","context":"","selected_llm":None}

    for q in queries:
        state["messages"] = [HumanMessage(content=q)]
        state["query"] = q
        thread = {"configurable":{"thread_id":"3"}}
        result = await agent.graph.ainvoke(state, thread)
        print(result["messages"][-1].content)
        for f in ["models","domains","subdomains","context","selected_llm"]:
            if f in result: state[f] = result[f]
        state["messages"].extend(result["messages"])

# In Jupyter: await main()
if __name__ == "__main__":
    import asyncio
    # Run the async main() function
    asyncio.run(main())