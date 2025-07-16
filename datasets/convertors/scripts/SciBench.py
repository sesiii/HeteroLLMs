import json

# Function to infer domain from tags
def infer_domain(tags):
    domain_tag = tags[1] if len(tags) > 1 else "general"
    domain_map = {
        "diff": "Physics",
        "fund": "Physics",
        "class": "Physics",
        "atkins": "Chemistry",
        "matter": "Chemistry",
        "chemmc": "Chemistry",
        "stat": "Statistics"
    }
    return domain_map.get(domain_tag, "Science General")

# Function to infer task_type from tags and query
def infer_task_type(tags, query):
    specific_tag = tags[1] if len(tags) > 1 else "general"
    query_lower = query.lower()
    task_type_map = {
        "diff": "Differential Equations",
        "atkins": "Thermodynamics",
        "matter": "Physical Chemistry",
        "fund": "Electrostatics",
        "class": "Classical Mechanics",
        "chemmc": "Quantum Chemistry",
        "stat": "Combinatorial Probability"
    }
    return task_type_map.get(specific_tag, "Science General")

# Function to infer difficulty from tags
def infer_difficulty(tags):
    specific_tag = tags[1] if len(tags) > 1 else "general"
    if specific_tag in ["stat", "chemmc"]:
        return "medium"
    elif specific_tag in ["fund"]:
        return "hard"
    elif specific_tag in ["diff", "atkins", "matter", "class"]:
        return "expert"
    return "hard"  # Default for SciBench

# Function to extract expected answer from gt
def extract_answer(gt):
    return gt.strip()

# Function to determine evaluation metric
def determine_evaluation_metric(answer):
    return "exact_match"  # Numerical answers require precise matching

# Load input JSON file
input_file = "../convert-json/SciBench.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=1):  # Start from SCI_001
    task_id = f"SCI_{i:03d}"  # e.g., SCI_001, SCI_002, ...
    answer = extract_answer(item["gt"])
    output_item = {
        "task_id": task_id,
        "domain": infer_domain(item["tag"]),
        "task_type": infer_task_type(item["tag"], item["query"]),
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