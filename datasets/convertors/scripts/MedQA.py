import json
import re

# Function to infer task_type from query content
def infer_task_type(query):
    query_lower = query.lower()
    if any(keyword in query_lower for keyword in ["diagnosis", "biopsy", "most likely diagnosis"]):
        return "Clinical Diagnosis"
    elif any(keyword in query_lower for keyword in ["pharmacotherapy", "drug", "prophylaxis", "medication"]):
        return "Pharmacology"
    elif any(keyword in query_lower for keyword in ["mechanism", "hypersensitivity", "cellular", "transcription factor"]):
        return "Pathophysiology"
    elif any(keyword in query_lower for keyword in ["organism", "culture", "gram stain", "bacteria"]):
        return "Microbiology"
    elif any(keyword in query_lower for keyword in ["pregnancy", "gestation", "prenatal"]):
        return "Obstetrics"
    elif any(keyword in query_lower for keyword in ["stroke", "aphasia", "neurologic", "weakness"]):
        return "Neurology"
    return "Medical General"  # Default fallback

# Function to infer difficulty
def infer_difficulty(tags):
    return "expert"  # Default for MedQA due to clinical complexity

# Function to extract expected answer from gt
def extract_answer(gt):
    return gt.strip()

# Function to determine evaluation metric
def determine_evaluation_metric(answer):
    return "exact_match"  # Multiple-choice answers require precise matching

# Load input JSON file
input_file = "../convert-json/MedQA.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=9):  # Start from MED_009 to continue from MedMCQA
    task_id = f"MED_{i:03d}"  # e.g., MED_009, MED_010, ...
    answer = extract_answer(item["gt"])
    output_item = {
        "task_id": task_id,
        "domain": "Medicine",
        "task_type": infer_task_type(item["query"]),
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