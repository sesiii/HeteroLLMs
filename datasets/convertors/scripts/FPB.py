import json

# Function to infer task_type (fixed for FPB)
def infer_task_type(query):
    return "Sentiment Analysis"

# Function to infer difficulty (fixed for FPB)
def infer_difficulty(gt, query):
    return "easy"  # Sentiment analysis of headlines is typically straightforward

# Function to extract expected answer from gt
def extract_answer(gt):
    return gt.strip()

# Function to determine evaluation metric
def determine_evaluation_metric(answer):
    return "exact_match"  # Sentiment labels require precise matching

# Load input JSON file
input_file = "../convert-json/FPB.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=12):  # Start from FIN_012 to continue from FinQA
    task_id = f"FIN_{i:03d}"  # e.g., FIN_012, FIN_013, ...
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