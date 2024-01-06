#!/bin/bash
# Change to the complete path of the 'python' directory
# Example: cd /home/ishts/Desktop/Projects/aws-data-scrap/python
# **NOTE**: Using an absolute path is crucial when running this script with cron, as the working directory of cron jobs may differ.
# cd python will work but not with cron
cd <complete path>/python

# Run the main Python script
python3 -u index.py

# Write a message indicating completion to file.txt
# echo "Completed JSON creation" > file.txt

for script_file in conversion-*.py; do
    # Check if the file exists
    if [ -f "$script_file" ]; then
        echo "Running $script_file"
        # Execute the Python script
        python3 -u "$script_file"
        echo "Finished $script_file"
        echo
    fi
done

