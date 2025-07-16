import json
import re

# Function to infer task_type based on query content
def infer_task_type(query):
    query_lower = query.lower()
    if "balance sheet" in query_lower or "working capital" in query_lower:
        return "Financial Analysis"
    elif "business segment" in query_lower or "net revenue" in query_lower:
        return "Corporate Finance"
    elif "products and services" in query_lower:
        return "Business Overview"
    elif "gain" in query_lower or "separation" in query_lower:
        return "Corporate Finance"
    else:
        return "Financial Analysis"  # Default for finance problems

# Function to infer difficulty based on gt explanation
def infer_difficulty(gt):
    lines = gt.split("\n")
    # Heuristic: more lines or complex terms indicate higher difficulty
    if len(lines) <= 1 or "simple" in gt.lower():
        return "easy"
    elif len(lines) <= 3 or "calculation" in gt.lower():
        return "medium"
    else:
        return "hard"

# Function to extract expected answer from gt
def extract_answer(gt, query):
    # For FinanceBench, gt typically contains the concise answer
    return gt.strip()

# Function to determine evaluation metric
def determine_evaluation_metric(answer):
    # Use exact_match for numerical or single-value answers, text_contains for descriptive answers
    if re.match(r"^-?\d+(\.\d+)?$|^\w+$", answer):  # Matches numbers or single letters
        return "exact_match"
    else:
        return "text_contains"

# Load input JSON file
input_file = "FinanceBench.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=1):
    task_id = f"FIN_{i:03d}"  # e.g., FIN_001, FIN_002, ...
    answer = extract_answer(item["gt"], item["query"])
    output_item = {
        "task_id": task_id,
        "domain": "Finance",
        "task_type": infer_task_type(item["query"]),
        "prompt": item["query"],
        "expected_answer": answer,
        "difficulty": infer_difficulty(item["gt"]),
        "evaluation_metric": determine_evaluation_metric(answer)
    }
    output_data.append(output_item)

# Save to output JSON file
output_file = "converted_data.json"
with open(output_file, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"Conversion complete. Output saved to {output_file}")