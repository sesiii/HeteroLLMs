import json
import re

# Function to infer task_type based on query content
def infer_task_type(query):
    query_lower = query.lower()
    if "asset" in query_lower or "liabilities" in query_lower or "working capital" in query_lower:
        return "Financial Analysis"
    elif "goodwill" in query_lower or "intangible assets" in query_lower:
        return "Accounting"
    elif "net sales" in query_lower or "revenue" in query_lower:
        return "Corporate Finance"
    else:
        return "Financial Analysis"  # Default for finance problems

# Function to infer difficulty based on gt explanation
def infer_difficulty(gt, query):
    # Heuristic: assess complexity based on query and gt content
    query_lower = query.lower()
    if "percentage change" in query_lower or "average" in query_lower:
        return "easy" if len(gt.split("\n")) <= 1 else "medium"
    elif "impairment" in query_lower or "decommissioning" in query_lower:
        return "hard"
    else:
        return "medium"

# Function to extract expected answer from gt
def extract_answer(gt):
    # For FinQA, gt is typically a concise numerical or percentage answer
    return gt.strip()

# Function to determine evaluation metric
def determine_evaluation_metric(answer):
    # Use exact_match for numerical or percentage answers
    if re.match(r"^-?\d+(\.\d+)?%?$|^-?\d+$", answer):  # Matches numbers or percentages
        return "exact_match"
    else:
        return "text_contains"  # Fallback for non-numerical answers

# Load input JSON file
input_file = "../FinQA.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=6):  # Start from FIN_006 to continue from FinanceBench
    task_id = f"FIN_{i:03d}"  # e.g., FIN_006, FIN_007, ...
    answer = extract_answer(item["gt"])
    output_item = {
        "task_id": task_id,
        "domain": "Finance",
        "task_type": infer_task_type(item["query"]),
        "prompt": item["query"],
        "expected_answer": answer,
        "difficulty": infer_difficulty(item["gt"], item["query"]),
        "evaluation_metric": determine_evaluation_metric(answer)
    }
    output_data.append(output_item)

# Save to output JSON file
output_file = "../input.json"
with open(output_file, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"Conversion complete. Output saved to {output_file}")