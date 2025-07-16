import json
import re

# Function to infer task_type from query content
def infer_task_type(query):
    query_lower = query.lower()
    if "orthopedic" in query_lower:
        return "Orthopedic Surgery"
    elif any(keyword in query_lower for keyword in ["hepatocellular", "liver regeneration", "hepatotoxicity"]):
        return "Hepatology"
    elif "infantile autism" in query_lower:
        return "Pediatrics"
    elif any(keyword in query_lower for keyword in ["stigmatizing attitudes", "disability"]):
        return "Social Psychology"
    elif any(keyword in query_lower for keyword in ["renal cell carcinoma", "radiation therapy"]):
        return "Oncology"
    elif "renal transplantation" in query_lower:
        return "Nephrology"
    return "Medical General"  # Default fallback

# Function to infer difficulty
def infer_difficulty(tags):
    return "expert"  # Default for PubMedQA due to research complexity

# Function to extract expected answer from gt
def extract_answer(gt):
    return gt.strip()

# Function to determine evaluation metric
def determine_evaluation_metric(answer):
    return "exact_match"  # Default for PubMedQA; can be adjusted if needed

# Load input JSON file
input_file = "../convert-json/PubMedQA.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=29):  # Start from MED_029 to continue from MedQA
    task_id = f"MED_{i:03d}"  # e.g., MED_029, MED_030, ...
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