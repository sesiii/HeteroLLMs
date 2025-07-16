#!/usr/bin/env bash
###############################################################################
# Universal parallel benchmark runner
# Creates     Results1/Mathematics/<model>/iter_<n>.json
###############################################################################

# --- configuration -----------------------------------------------------------
ITERATIONS=${1:-5}
SCRIPT_DIR="/home/dadi/Desktop/Ericsson/ER/agentic-ai/experiments/HeteroLLMs"
PYTHON_SCRIPT="test_script.py"
DATASET_PATH="datasets/Domain/Mathematics/ref.json"
RESULTS_ROOT="Results1/Mathematics"
LOG_FILE="logs/Mathematics/run_parallel_ref.log"
OLLAMA_API="http://127.0.0.1:11434"
# model list (must match Python CONFIG['MODELS'])
MODELS=( "qwen2.5_1.5B" "llama3.2_1B" )

# --- helpers -----------------------------------------------------------------
die() { echo "$*" >&2; exit 1; }

# --- sanity checks -----------------------------------------------------------
[[ "$ITERATIONS" =~ ^[1-9][0-9]*$ ]] || die "Need a positive integer for iterations"
cd "$SCRIPT_DIR" || die "Directory $SCRIPT_DIR not found"
[[ -f "$PYTHON_SCRIPT" ]]   || die "$PYTHON_SCRIPT missing"
[[ -f "$DATASET_PATH" ]]    || die "$DATASET_PATH missing"

# --- prepare filesystem ------------------------------------------------------
mkdir -p "logs/Mathematics"
for m in "${MODELS[@]}"; do
    mkdir -p "$RESULTS_ROOT/$m"
done
chmod u+rwx "$RESULTS_ROOT" "logs/Mathematics"

# --- start log ---------------------------------------------------------------
echo "$(date '+%F %T') Starting $ITERATIONS iterations for ${MODELS[*]}" | tee -a "$LOG_FILE"

# --- Ollama tuning -----------------------------------------------------------
export OLLAMA_MAX_LOADED_MODELS=2
export OLLAMA_NUM_PARALLEL=1

# --- main loop ---------------------------------------------------------------
for ((i=1; i<=ITERATIONS; i++)); do
    echo "===== Iteration $i =====" | tee -a "$LOG_FILE"

    # basic resource snapshot
    { echo "Memory:"; free -m; echo "Top:"; top -bn1 | head -5; } >> "$LOG_FILE"

    # restart Ollama cleanly
    pkill -f ollama 2>/dev/null || true
    rm -rf ~/.ollama/models/cache/*
    ollama serve >/dev/null 2>&1 &
    sleep 5
    curl -s --connect-timeout 5 "$OLLAMA_API" >/dev/null || \
        die "Ollama not reachable at $OLLAMA_API"

    # run Python script once
    python3 "$PYTHON_SCRIPT" --iteration "$i" \
        >"logs/Mathematics/iter_${i}.stdout" \
        2>"logs/Mathematics/iter_${i}.stderr"

    # verify per-model outputs
    for m in "${MODELS[@]}"; do
        out_file="$RESULTS_ROOT/$m/ref_results_iter_${i}.json"
        if [[ -f "$out_file" ]]; then
            echo "✓ $out_file"
        else
            echo "✗ Missing: $out_file" | tee -a "$LOG_FILE"
            cat "logs/Mathematics/iter_${i}.stderr" >> "$LOG_FILE"
        fi
    done

    sleep 10   # small cooldown
done

# # --- aggregation -------------------------------------------------------------
# echo "$(date '+%F %T') Aggregating results" | tee -a "$LOG_FILE"
# python3 aggregate_results.py >> "$LOG_FILE" 2>&1 || \
#     die "Aggregation failed"

# --- cleanup -----------------------------------------------------------------
rm -f logs/Mathematics/iter_{1..$ITERATIONS}.{stdout,stderr}
echo "All iterations completed. Logs → $LOG_FILE"