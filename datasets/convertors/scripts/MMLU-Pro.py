import json

# Function to infer domain from tags
def infer_domain(tags):
    domain_tag = tags[1] if len(tags) > 1 else "other"
    domain_map = {
        "history": "History",
        "engineering": "Engineering",
        "biology": "Biology",
        "health": "Health",
        "math": "Mathematics",
        "law": "Law",
        "economics": "Economics",
        "other": "Public Relations" if "ori_mmlu-public_relations" in tags or "ori_mmlu-human_sexuality" in tags else "General Knowledge"
    }
    return domain_map.get(domain_tag, "General Knowledge")

# Function to infer task_type from tags
def infer_task_type(tags):
    specific_tag = tags[2] if len(tags) > 2 else "general"
    task_type_map = {
        "ori_mmlu-high_school_us_history": "US History",
        "ori_mmlu-public_relations": "Public Relations",
        "stemez-ElectricalMachines": "Electrical Engineering",
        "stemez-Biology": "Biology",
        "ori_mmlu-nutrition": "Nutrition",
        "ori_mmlu-elementary_mathematics": "Elementary Mathematics",
        "ori_mmlu-professional_law": "Professional Law",
        "ori_mmlu-high_school_macroeconomics": "Macroeconomics",
        "ori_mmlu-human_sexuality": "Human Sexuality"
    }
    return task_type_map.get(specific_tag, "General Knowledge")

# Function to infer difficulty from tags
def infer_difficulty(tags):
    specific_tag = tags[2] if len(tags) > 2 else "general"
    if specific_tag in ["ori_mmlu-elementary_mathematics", "ori_mmlu-high_school_macroeconomics", "ori_mmlu-high_school_us_history"]:
        return "medium"
    elif specific_tag in ["stemez-Biology", "stemez-ElectricalMachines", "ori_mmlu-nutrition"]:
        return "hard"
    elif specific_tag in ["ori_mmlu-professional_law", "ori_mmlu-public_relations", "ori_mmlu-human_sexuality"]:
        return "expert"
    return "hard"  # Default for MMLU-Pro

# Function to extract expected answer from gt
def extract_answer(gt):
    return gt.strip()

# Function to determine evaluation metric
def determine_evaluation_metric(answer):
    return "exact_match"  # Multiple-choice answers require precise matching

# Load input JSON file
input_file = "../convert-json/MMLU-Pro.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=1):  # Start from MMLU_001
    task_id = f"MMLU_{i:03d}"  # e.g., MMLU_001, MMLU_002, ...
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