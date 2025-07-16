import json
import re

# Function to infer domain from tags
def infer_domain(tags):
    domain_tag = tags[1] if len(tags) > 1 else "general"
    domain_map = {
        "college_medicine": "Medicine",
        "security_studies": "Security Studies",
        "high_school_macroeconomics": "Economics",
        "elementary_mathematics": "Mathematics",
        "professional_law": "Law",
        "college_physics": "Physics",
        "machine_learning": "Machine Learning"
    }
    return domain_map.get(domain_tag, "General Knowledge")

# Function to infer task_type from tags and query
def infer_task_type(tags, query):
    specific_tag = tags[1] if len(tags) > 1 else "general"
    query_lower = query.lower()
    task_type_map = {
        "college_medicine": "Physiology" if "muscle contraction" in query_lower else "Medical General",
        "security_studies": "Global Justice" if "historical materialism" in query_lower else "Security Studies",
        "high_school_macroeconomics": "Macroeconomics",
        "elementary_mathematics": "Arithmetic",
        "college_physics": "Nuclear Physics" if "thermonuclear" in query_lower else "Physics",
        "machine_learning": "Neural Networks" if "neural networks" in query_lower else "Machine Learning",
        "professional_law": "Torts" if any(keyword in query_lower for keyword in ["battery", "invasion of privacy", "strict liability"]) else "Property Law" if "deed" in query_lower else "Legal General"
    }
    return task_type_map.get(specific_tag, "General Knowledge")

# Function to infer difficulty from tags
def infer_difficulty(tags):
    specific_tag = tags[1] if len(tags) > 1 else "general"
    if specific_tag in ["elementary_mathematics", "high_school_macroeconomics"]:
        return "easy"
    elif specific_tag in ["college_medicine", "college_physics", "machine_learning"]:
        return "hard"
    elif specific_tag in ["security_studies", "professional_law"]:
        return "expert"
    return "hard"  # Default for MMLU

# Function to extract answer text from query based on gt
def extract_answer_text(query, gt):
    # Extract the letter from gt (e.g., "(A)" -> "A")
    letter = gt.strip("()")
    # Find the answer text in the query
    match = re.search(rf"\({letter}\)\s*([^\n]+)", query)
    if match:
        return f"({letter}) {match.group(1).strip()}"
    return gt  # Fallback to gt if answer text not found

# Function to determine evaluation metric
def determine_evaluation_metric(answer):
    return "exact_match"  # Multiple-choice answers require precise matching

# Load input JSON file
input_file = "../convert-json/MMLU.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=12):  # Start from MMLU_012 to continue from MMLU-Pro
    task_id = f"MMLU_{i:03d}"  # e.g., MMLU_012, MMLU_013, ...
    answer = extract_answer_text(item["query"], item["gt"])
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