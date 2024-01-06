import os
import pandas as pd
import json

# Read Elastic IP data from the JSON file
with open('../python_output/elasticip.json', 'r') as file:
    elasticip_data = json.load(file)

# Initialize empty lists for each column
resources = []
ids_names = []
owners = []
regions = []
emails = []
statuses = []

# Iterate through the JSON data and extract information
for elastic_ip in elasticip_data:
    # Resource
    resources.append("elasticip")

    # Id/Name
    allocation_id = elastic_ip.get("PublicIp")
    ids_names.append(allocation_id)

    # Owner
    owner_tag = next((tag["Value"] for tag in elastic_ip.get("Tags", []) if tag.get("Key", "").lower() == "owner"), "-") if "Tags" in elastic_ip else "-"
    owners.append(owner_tag)

    # Region
    regions.append(elastic_ip.get("Region", "-"))

    # Email
    email_tag = next((tag["Value"] for tag in elastic_ip.get("Tags", []) if tag.get("Key", "").lower() == "email"), "-") if "Tags" in elastic_ip else "-"
    emails.append(email_tag)

    # Required / Terminated (Assuming Elastic IP does not have a specific state, putting "-")
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
df.to_excel("../python_execl/elasticip_data.xlsx", index=False)
