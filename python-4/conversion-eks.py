import os
import pandas as pd
import json

# Read ECS cluster data from the JSON file
with open('../python_output/eks.json', 'r') as file:
    ecs_data = json.load(file)

# Initialize empty lists for each column
resources = []
ids_names = []
owners = []
regions = []
emails = []
statuses = []

# Iterate through the JSON data and extract information
for cluster in ecs_data:
    # Resource
    resources.append("EKS")

    # Id/Name
    cluster_name = cluster.get("ClusterName")
    ids_names.append(cluster_name)

    # Owner
    owner_tag = cluster.get("Tags", {}).get("owner", "-")
    owners.append(owner_tag)

    # Region
    regions.append(cluster.get("Region", "-"))

    # Email
    email_tag = cluster.get("Tags", {}).get("email", "-")
    emails.append(email_tag)

    # Required / Terminated (Assuming ECS cluster does not have a specific state, putting "-")
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
df.to_excel("../python_execl/eks_data.xlsx", index=False)
