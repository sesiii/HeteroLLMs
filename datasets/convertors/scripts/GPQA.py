import json

# Function to infer domain from tags
def infer_domain(tags):
    # Take the first tag after "GPQA" as the domain
    for tag in tags:
        if tag != "GPQA" and "level" not in tag.lower():
            return tag
    return "Science"  # Default fallback

# Function to infer task_type from tags
def infer_task_type(tags):
    # Look for specific subfield tags
    for tag in tags:
        if tag in ["Physics (general)", "Statistical Mechanics", "Quantum Mechanics", "Relativistic Mechanics", 
                   "Astrophysics", "Organic Chemistry", "Chemistry (general)", "Molecular Biology", "Genetics"]:
            return tag
    return "General Science"  # Default fallback

# Function to infer difficulty from tags
def infer_difficulty(tags):
    
    return "hard"  # Default for GPQA problems

# Function to extract expected answer from gt
def extract_answer(gt):
    return gt.strip()

# Function to determine evaluation metric
def determine_evaluation_metric(answer):
    return "exact_match"  # Multiple-choice answers require precise matching

# Load input JSON file
input_file = "../convert-json/GPQA.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=6):  # Start from SCI_006 to continue from GPQA-Diamond
    task_id = f"SCI_{i:03d}"  # e.g., SCI_006, SCI_007, ...
    answer = extract_answer(item["gt"])
    output_item = {
        "task_id": task_id,
        "domain": infer_domain(item["tag"]),
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