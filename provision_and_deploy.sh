#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Read unit_name from command-line argument
unit_name="$1"

# Call Python script with unit_name argument
python provision_superset.py "$unit_name"

# # Create commit with changes
# git add .
# git commit -m "provision superset $unit_name"

# # Push changes to GitHub repository
# git push origin master