import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Sample dataset: 50 queries with embeddings and rewards
np.random.seed(42)
num_queries = 50
num_arms = 2
context_dim = 5
llms = ["GPT4", "Claude3-Sonnet"]

# 50 sample queries
queries = [
    "What is the capital of France?",
    "How does photosynthesis work?",
    "Write a Python function to sort a list.",
    "Who won the Nobel Peace Prize in 2020?",
    "Explain quantum entanglement.",
    "What are the benefits of recycling?",
    "How to solve a quadratic equation?",
    "What is the history of the Roman Empire?",
    "Describe the theory of relativity.",
    "How to implement a binary search tree?",
    "What causes climate change?",
    "Who was Cleopatra?",
    "What is machine learning?",
    "How to bake a chocolate cake?",
    "What is the Pythagorean theorem?",
    "Explain the water cycle.",
    "How to create a REST API in Flask?",
    "What are black holes?",
    "Who invented the telephone?",
    "What is the greenhouse effect?",
    "How to calculate compound interest?",
    "What is the significance of the Magna Carta?",
    "Explain neural networks.",
    "What is the structure of DNA?",
    "How to optimize a SQL query?",
    "What is the French Revolution?",
    "Describe the solar system.",
    "How to train a dog?",
    "What is artificial intelligence?",
    "How to draw a realistic portrait?",
    "What are renewable energy sources?",
    "Explain the concept of blockchain.",
    "What is the periodic table?",
    "How to write a resume?",
    "What is the theory of evolution?",
    "How to build a simple website?",
    "What are the causes of World War I?",
    "Explain the concept of gravity.",
    "How to perform a t-test in statistics?",
    "What is the life cycle of a star?",
    "Who was Albert Einstein?",
    "What is cloud computing?",
    "How to meditate effectively?",
    "What is the history of the Internet?",
    "Explain the concept of supply and demand.",
    "How to create a mobile app?",
    "What is the ozone layer?",
    "Who was Leonardo da Vinci?",
    "What is deep learning?",
    "How to grow vegetables at home?"
]

# Generate simulated embeddings and rewards
query_embeddings = np.random.rand(num_queries, context_dim)
true_rewards = {
    "GPT4": np.clip(np.random.normal(0.85, 0.05, num_queries), 0, 1),  # Adjusted mean
    "Claude3-Sonnet": np.clip(np.random.normal(0.75, 0.05, num_queries), 0, 1)
}

# Create dataset
dataset = pd.DataFrame({
    "query": queries,
    "embedding": list(query_embeddings),
    "rewards": [ {llms[i]: true_rewards[llms[i]][j] for i in range(num_arms)} for j in range(num_queries) ]
})

# Contextual UCB Algorithm
class ContextualUCB:
    def __init__(self, num_arms, context_dim, exploration_factor=1.0):  # Increased exploration
        self.num_arms = num_arms
        self.context_dim = context_dim
        self.exploration_factor = exploration_factor
        self.weights = [np.zeros(context_dim) for _ in range(num_arms)]
        self.pulls = [0] * num_arms
        self.A = [np.identity(context_dim) for _ in range(num_arms)]
        self.b = [np.zeros(context_dim) for _ in range(num_arms)]

    def select_arm(self, context, t):
        ucb_values = []
        for arm in range(self.num_arms):
            mean_reward = np.dot(self.weights[arm], context)
            A_inv = np.linalg.inv(self.A[arm])
            uncertainty = self.exploration_factor * np.sqrt(np.dot(context, A_inv @ context))
            ucb = mean_reward + uncertainty
            ucb_values.append((ucb, mean_reward, uncertainty))
        return ucb_values

    def update(self, arm, context, reward):
        context = np.array(context)
        self.pulls[arm] += 1
        self.A[arm] += np.outer(context, context)
        self.b[arm] += reward * context
        self.weights[arm] = np.linalg.inv(self.A[arm]) @ self.b[arm]

# Run UCB algorithm with detailed logging
ucb = ContextualUCB(num_arms=num_arms, context_dim=context_dim, exploration_factor=1.0)
cumulative_regret = 0
top1_correct = 0
regrets = []
per_step_regrets = []
selections = [0] * num_arms

print("Step-by-Step UCB Execution (First 10 Steps):")
for t in range(num_queries):
    context = dataset["embedding"][t]
    rewards = dataset["rewards"][t]
    
    ucb_values = ucb.select_arm(context, t)
    selected_arm = np.argmax([ucb for ucb, _, _ in ucb_values])
    selected_llm = llms[selected_arm]
    mean_reward = ucb_values[selected_arm][1]
    uncertainty = ucb_values[selected_arm][2]
    
    actual_reward = rewards[selected_llm]
    
    ucb.update(selected_arm, context, actual_reward)
    
    optimal_llm = max(rewards, key=rewards.get)
    regret = rewards[optimal_llm] - actual_reward
    cumulative_regret += regret
    regrets.append(cumulative_regret)
    per_step_regrets.append(regret)
    
    selections[selected_arm] += 1
    
    if selected_llm == optimal_llm:
        top1_correct += 1
    
    if t < 50:  # Log first 10 steps
        print(f"\nStep {t + 1}: Query: {dataset['query'][t][:50]}...")
        print(f"  UCB Scores: GPT4={ucb_values[0][0]:.3f} (Mean={ucb_values[0][1]:.3f}, Uncertainty={ucb_values[0][2]:.3f}), "
              f"Claude3-Sonnet={ucb_values[1][0]:.3f} (Mean={ucb_values[1][1]:.3f}, Uncertainty={ucb_values[1][2]:.3f})")
        print(f"  Selected LLM: {selected_llm}")
        print(f"  Actual Reward: {actual_reward:.3f}")
        print(f"  Optimal LLM: {optimal_llm}, Reward: {rewards[optimal_llm]:.3f}")
        print(f"  Regret: {regret:.3f}, Cumulative Regret: {cumulative_regret:.3f}")
        print(f"  Exploration or Exploitation: {'Exploration' if uncertainty > mean_reward else 'Exploitation'}")

# Print final results
print(f"\nFinal Results:")
print(f"Cumulative Regret: {cumulative_regret:.2f}")
print(f"Top-1 Accuracy: {top1_correct / num_queries * 100:.2f}%")
print(f"Selection Counts: GPT4={selections[0]}, Claude3-Sonnet={selections[1]}")

# Plot cumulative regret and per-step regret
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(regrets)
plt.xlabel("Time Step")
plt.ylabel("Cumulative Regret")
plt.title("Cumulative Regret Over Time")

plt.subplot(1, 2, 2)
plt.plot(per_step_regrets, marker='o')
plt.xlabel("Time Step")
plt.ylabel("Per-Step Regret")
plt.title("Per-Step Regret")
plt.tight_layout()

# Plot LLM selection frequency
plt.figure(figsize=(6, 4))
plt.bar(llms, selections)
plt.xlabel("LLM")
plt.ylabel("Number of Selections")
plt.title("LLM Selection Frequency")
plt.show()