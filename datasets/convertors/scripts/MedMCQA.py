import json

# Function to infer task_type from tags
def infer_task_type(tags):
    # Look for subfield tags
    for tag in tags:
        if tag in ["Physiology", "Surgery", "Dental", "Anaesthesia", "Anatomy", "Orthopaedics"]:
            return tag
    return "Medical General"  # Default fallback

# Function to infer difficulty from tags
def infer_difficulty(tags):
    for tag in tags:
        if tag in ["AIIMS 2017", "AIIMS 2018"]:
            return "expert"
    return "hard"  # Default for MedMCQA problems

# Function to extract expected answer from gt
def extract_answer(gt):
    return gt.strip()

# Function to determine evaluation metric
def determine_evaluation_metric(answer):
    return "exact_match"  # Multiple-choice answers require precise matching

# Load input JSON file
input_file = "../convert-json/MedMCQA.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=1):  # Start from MED_001
    task_id = f"MED_{i:03d}"  # e.g., MED_001, MED_002, ...
    answer = extract_answer(item["gt"])
    output_item = {
        "task_id": task_id,
        "domain": "Medicine",
        "task_type": infer_task_type(item["tag"]),
        "prompt": item["query"],
        "expected_answer": answer,
        "difficulty": infer_difficulty(item["tag"]),
        "evaluation_metric": determine_evaluation_metric(answer)
    }
    output_data.append(output_item)

# Save to output JSON file
output_file = "../input.json"
with open(output_file, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"Conversion complete. Output saved to {output_file}")