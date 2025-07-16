from langchain_together import ChatTogether
from langchain_core.messages import HumanMessage

llm = ChatTogether(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    temperature=0.1,
    together_api_key="tgp_v1_9YTKsmfpFswTWt10Oo4EpYaRUogHmPfv4VJkCXI-84Y"  # if not set via env
)

response = llm.invoke([
    HumanMessage(content="What is 5 + 3? Return only a JSON object like this: {'answer': 8}")
])

print("🔍 Raw response content:", repr(response.content))