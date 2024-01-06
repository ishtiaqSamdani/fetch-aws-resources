import os
import pandas as pd
import json

# Read ECR data from the JSON file
with open('../python_output/ecr.json', 'r') as file:
    ecr_data = json.load(file)

# Initialize empty lists for each column
resources = []
ids_names = []
owners = []
regions = []
emails = []
statuses = []

# Iterate through the JSON data and extract information
for repository in ecr_data:
    # Resource
    resources.append("ecr")

    # Id/Name
    repository_name = repository.get("RepositoryName")
    ids_names.append(repository_name)

    # Owner
    owner_tag = next((tag["Value"] for tag in repository.get("Tags", []) if tag["Key"].lower() == "owner"), "-") if "Tags" in repository else "-"
    owners.append(owner_tag)

    # Region
    regions.append(repository.get("Region", "-"))

    # Email
    email_tag = next((tag["Value"] for tag in repository.get("Tags", []) if tag["Key"].lower() == "email"), "-") if "Tags" in repository else "-"
    emails.append(email_tag)

    # Required / Terminated (Assuming ECR does not have a specific state, putting "-")
    statuses.append("-")

# Create a DataFrame
df = pd.DataFrame({
    "Resource": resources,
    "Id/Name": ids_names,
    "Owner": owners,
    "Region": regions,
    "Email": emails,
    "Required/Terminated": statuses,
    "Remark": "-"
})

# create python_execl folder
folder_path = '../python_execl'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    
# Save to Excel
df.to_excel("../python_execl/ecr_data.xlsx", index=False)
