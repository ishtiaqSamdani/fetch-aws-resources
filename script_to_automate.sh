#!/bin/bash
cd /home/ishts/Desktop/Projects/aws-data-scrap/python
python3 -u index.py

echo "completed json creation" > file.txt
for script_file in conversion-*.py; do
    if [ -f "$script_file" ]; then
        echo "Running $script_file"
        python3 -u "$script_file"
        echo "Finished $script_file"
        echo
    fi
done

