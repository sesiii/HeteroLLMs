import json
import logging
import re
from langchain_together import ChatTogether
from langchain_core.messages import SystemMessage, HumanMessage
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# 1. Setup LLM
try:
    llm = ChatTogether(
        model="meta-llama/Llama-3-8b-chat-hf",
        temperature=0.1,
    )
    logger.info("LLM initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LLM: {e}")
    raise


# 2. LLM call with retry logic
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=(
        retry_if_exception_type(Exception)
        | retry_if_result(lambda r: not r or not r.content.strip())
    ),
    before_sleep=lambda retry_state: logger.warning(
        f"Empty/invalid response, retrying attempt {retry_state.attempt_number}/5"
    ),
)
def call_llm(messages):
    try:
        resp = llm.invoke(messages)
        # Treat empty or whitespace-only content as a retry-able failure
        if not resp or not resp.content.strip():
            logger.warning("Received empty response body")
            raise ValueError("Empty response")
        return resp
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise


# 3. Define the evaluation function
def evaluate(prompt: str, expected: str, predicted: str) -> dict:
    try:
        logger.info(
            f"Evaluating prompt: {prompt[:50]}..., "
            f"Expected: {expected}, Predicted: {predicted[:50]}..."
        )

        messages = [
            SystemMessage(
                content=(
                    "You are an evaluator AI. Your task is to compare the Predicted Answer "
                    "with the Expected Answer for the given Prompt. Extract the final numeric "
                    "value from the Predicted Answer, ignoring units (e.g., '$', 'dollars', 'bolts') "
                    "and any surrounding text or reasoning. The numeric value may be an integer "
                    "(e.g., '3'), a decimal (e.g., '3.0'), or a word (e.g., 'three'). Compare it to "
                    "the Expected Answer, which is a numeric string (e.g., '3', '18'). "
                    "Return ONLY a JSON object with: 'reasoning' (brief explanation), "
                    "'final_answer' (the extracted numeric value or null), and 'decision' "
                    "('Yes' if the extracted value matches the Expected Answer, 'No' otherwise). "
                    "Do NOT return any additional commentary or markdown."
                )
            ),
            HumanMessage(
                content=f"""Prompt: {prompt}
Expected Answer: {expected}
Predicted Answer: {predicted}

Return ONLY the JSON object."""
            ),
        ]

        result = call_llm(messages)
        raw = result.content.strip()

        # Try to find a JSON block if the model wrapped it in markdown
        json_match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        if json_match:
            raw = json_match.group(0)

        output = json.loads(raw)

        # Validate structure
        if (
            not isinstance(output, dict)
            or "decision" not in output
            or output["decision"] not in {"Yes", "No"}
        ):
            raise ValueError("Invalid LLM JSON structure")

        logger.info(f"LLM Raw Output: {output}")
        return output

    except Exception as e:
        logger.warning(f"LLM evaluation failed ({e}); switching to fallback extraction")
        # Fallback: simple regex extraction
        match = re.search(r"\$?(\d*\.?\d+)", predicted)
        if match:
            predicted_value = match.group(1)
            reasoning = f"Fallback: Extracted {predicted_value} from predicted answer"
            decision = "Yes" if predicted_value == expected else "No"
            return {
                "reasoning": reasoning,
                "final_answer": predicted_value,
                "decision": decision,
            }

        # Try number words
        number_words = {
            "zero": "0",
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }
        for word, digit in number_words.items():
            if word in predicted.lower():
                reasoning = f"Fallback: Found number word '{word}' in predicted answer"
                decision = "Yes" if digit == expected else "No"
                return {
                    "reasoning": reasoning,
                    "final_answer": digit,
                    "decision": decision,
                }

        return {
            "reasoning": "Fallback: No numeric value or word found",
            "final_answer": None,
            "decision": "No",
        }


# 4. Load JSON input
try:
    logger.info("Reading input data")
    with open(
        "Results1/Mathematics/llama3.2_1B/ref_results_iter_1.json", "r"
    ) as f:
        data = json.load(f)
    logger.info("Input data read")
except Exception as e:
    logger.error(f"Failed to load input data: {e}")
    raise

# 5. Run evaluation on each item
for item in data:
    prompt = item["prompt"]
    expected = item["expected"]
    predicted = item["predicted"]

    logger.info(f"Evaluating task_id: {item.get('task_id')}")
    res = evaluate(prompt, expected, predicted)
    item["correct"] = res["decision"].lower() == "yes"
    item["score"] = 1.0 if item["correct"] else 0.0
    logger.info(
        f"Result: {res}, Correct: {item['correct']}, Score: {item['score']}"
    )
    print(f"\nEvaluating task_id: {item.get('task_id')}")
    print(f"Result: {res['decision']}, Correct: {item['correct']}, Score: {item['score']}")

# 6. Write updated results
try:
    with open(
        "Results1/Mathematics/evaluated/llama3.2_1B/ref_results_iter_1.json", "w"
    ) as f:
        json.dump(data, f, indent=2)
    logger.info("Successfully saved evaluated results")
except Exception as e:
    logger.error(f"Failed to save evaluated results: {e}")
    raise

print("\n✅ Evaluation complete. Results saved.")