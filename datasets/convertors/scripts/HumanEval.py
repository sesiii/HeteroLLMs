import json

# Function to infer task_type (fixed for HumanEval)
def infer_task_type(query):
    return "Python Function Implementation"

# Function to infer difficulty (fixed for HumanEval)
def infer_difficulty(gt, query):
    return "medium"  # HumanEval problems are moderately challenging

# Function to extract expected answer from gt
def extract_answer(gt):
    return gt.strip()

# Function to determine evaluation metric
def determine_evaluation_metric():
    return "test_case_execution"  # HumanEval problems are evaluated via test cases

# Function to combine query and test into prompt
def combine_prompt(query, test):
    return f"{query}\n\nTest Cases:\n{test.strip()}"

# Load input JSON file
input_file = "../convert-json/HumanEval.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=1):  # Start from CODE_001
    task_id = f"CODE_{i:03d}"  # e.g., CODE_001, CODE_002, ...
    answer = extract_answer(item["gt"])
    prompt = combine_prompt(item["query"], item["test"])
    output_item = {
        "task_id": task_id,
        "domain": "Computer Science",
        "task_type": infer_task_type(item["query"]),
        "prompt": prompt,
        "expected_answer": answer,
        "difficulty": infer_difficulty(item["gt"], item["query"]),
        "evaluation_metric": determine_evaluation_metric()
    }
    output_data.append(output_item)

# Save to output JSON file
output_file = "../input.json"
with open(output_file, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"Conversion complete. Output saved to {output_file}")