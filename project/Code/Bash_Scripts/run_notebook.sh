#!/bin/bash

# Define the path to your notebook and log file
NOTEBOOK_PATH="/nfs/turbo/si-acastel/expert_field_project/data_pipeline/check_for_new_publications.ipynb"
LOG_FILE="/nfs/turbo/si-acastel/expert_field_project/Bash_Scripts/publication_check_log.txt"

# Convert notebook to .py script with correct output name
jupyter nbconvert --to script "$NOTEBOOK_PATH" --output "/nfs/turbo/si-acastel/expert_field_project/data_pipeline/check_for_new_publications"

# Execute the converted script
python3 "/nfs/turbo/si-acastel/expert_field_project/data_pipeline/check_for_new_publications.py"

# Log the date and time of execution
echo "Publication check ran at: $(date)" >> "$LOG_FILE"

# Reschedule this script to run again in one hour
echo "/nfs/turbo/si-acastel/expert_field_project/Bash_Scripts/run_publication_check.sh" | at now + 1 week




