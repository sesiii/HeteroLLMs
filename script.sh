#!/bin/bash

if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <num_iterations> <domain_name> <test_file> [model_name]"
    echo "Example: $0 5 Mathematics test_algebra qwen2.5:1.5b"
    echo "Example: $0 5 Mathematics test_algebra all"
    exit 1
fi

NUM_ITERATIONS=$1
DOMAIN=$2
TEST_FILE=$3
MODEL_NAME=${4:-all}

TEST_SCRIPT="test_script.py"
EVALUATE_SCRIPT="evaluate_results.py"
AGGREGATE_SCRIPT="aggregate_results.py"
for SCRIPT in "$TEST_SCRIPT" "$EVALUATE_SCRIPT" "$AGGREGATE_SCRIPT"; do
    if [ ! -f "$SCRIPT" ]; then
        echo "Error: $SCRIPT not found"
        exit 1
    fi
done

mkdir -p "datasets/Domain/$DOMAIN"
mkdir -p "Final_Results/$DOMAIN/evaluated"
mkdir -p "logs/Domain/$DOMAIN"

# Define available models
MODELS=("qwen2.5:1.5b" "llama3.2:1b")

# Function to run test script for a single model
run_test_for_model() {
    local model=$1
    for ((i=1; i<=NUM_ITERATIONS; i++))
    do
        echo "Running iteration $i of $NUM_ITERATIONS for model $model in domain $DOMAIN with test file $TEST_FILE..."
        python3 $TEST_SCRIPT --iteration $i --model "$model" --domain "$DOMAIN" --test-file "$TEST_FILE"
        if [ $? -ne 0 ]; then
            echo "Error: Iteration $i failed for model $model"
            exit 1
        fi
        echo "Completed iteration $i for model $model"
    done
}

# Function to run evaluation script for a single model
run_evaluation_for_model() {
    local model=$1
    for ((i=1; i<=NUM_ITERATIONS; i++))
    do
        echo "Evaluating iteration $i of $NUM_ITERATIONS for model $model in domain $DOMAIN with test file $TEST_FILE..."
        python3 $EVALUATE_SCRIPT --iteration $i --model "$model" --domain "$DOMAIN" --test-file "$TEST_FILE"
        if [ $? -ne 0 ]; then
            echo "Error: Evaluation failed for iteration $i of model $model"
            exit 1
        fi
        echo "Completed evaluation for iteration $i of model $model"
    done
}

# Function to run aggregation script for a single model
run_aggregation_for_model() {
    local model=$1
    echo "Aggregating results for $NUM_ITERATIONS iterations in domain $DOMAIN with test file $TEST_FILE for model $model..."
    python3 $AGGREGATE_SCRIPT --domain "$DOMAIN" --test-file "$TEST_FILE" --iterations "$NUM_ITERATIONS" --model "$model"
    if [ $? -ne 0 ]; then
        echo "Error: Aggregation failed for $model"
        exit 1
    fi
    echo "Completed aggregation for $model"
}

# Run tests, evaluation, and aggregation based on model selection
if [ "$MODEL_NAME" = "all" ]; then
    for MODEL in "${MODELS[@]}"; do
        run_test_for_model "$MODEL"
        run_evaluation_for_model "$MODEL"
        run_aggregation_for_model "$MODEL"
    done
else
    # Validate model name
    VALID_MODEL=false
    for MODEL in "${MODELS[@]}"; do
        if [ "$MODEL" = "$MODEL_NAME" ]; then
            VALID_MODEL=true
            break
        fi
    done
    if [ "$VALID_MODEL" = false ]; then
        echo "Error: Invalid model name $MODEL_NAME. Available models: ${MODELS[*]}"
        exit 1
    fi
    
    run_test_for_model "$MODEL_NAME"
    run_evaluation_for_model "$MODEL_NAME"
    run_aggregation_for_model "$MODEL_NAME"
fi

echo "All iterations, evaluations, and aggregations completed successfully"