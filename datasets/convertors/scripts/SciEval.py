import json
import re

# Function to infer domain from tags
def infer_domain(tags):
    domain_tag = tags[1] if len(tags) > 1 else "general"
    domain_map = {
        "chemistry": "Chemistry",
        "biology": "Biology",
        "physics": "Physics"
    }
    return domain_map.get(domain_tag, "Science General")

# Function to infer task_type from tags and query
def infer_task_type(tags, query):
    specific_tag = tags[2] if len(tags) > 2 else "general"
    query_lower = query.lower()
    task_type_map = {
        "chemistry_SocraticQA": "Organic Chemistry" if "1-methylpropane" in query_lower else "General Chemistry",
        "biology_SocraticQA": "Oncology" if "cancer cells" in query_lower else "Cell Biology" if any(k in query_lower for k in ["x inactivation", "centromeres"]) else "Biology General",
        "physics_SocraticQA": "Thermodynamics" if "heat transfer" in query_lower else "Physics General",
        "biology_MedQA": "Clinical Medicine",
        "chemistry_reagent selection": "Organic Synthesis"
    }
    return task_type_map.get(specific_tag, "Science General")

# Function to infer difficulty from tags
def infer_difficulty(tags):
    specific_tag = tags[2] if len(tags) > 2 else "general"
    if specific_tag in ["chemistry_SocraticQA", "biology_SocraticQA", "physics_SocraticQA"]:
        return "medium"
    elif specific_tag in ["biology_MedQA", "chemistry_reagent selection"]:
        return "expert"
    return "medium"  # Default for SciEval

# Function to extract answer text from query based on gt
def extract_answer_text(query, gt):
    if "reactant" in query.lower():
        return gt  # For reactant selection, return SMILES string directly
    # Extract the letter from gt (e.g., "A")
    letter = gt.strip()
    # Find the answer text in the query
    match = re.search(rf"{letter}\.\s*([^\n]+)", query)
    if match:
        return f"{letter}. {match.group(1).strip()}"
    return gt  # Fallback to gt if answer text not found

# Function to determine evaluation metric
def determine_evaluation_metric(answer):
    return "exact_match"  # Multiple-choice and SMILES require precise matching

# Load input JSON file
input_file = "../convert-json/SciEval.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=10):  # Start from SCI_010 to continue from SciBench
    task_id = f"SCI_{i:03d}"  # e.g., SCI_010, SCI_011, ...
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