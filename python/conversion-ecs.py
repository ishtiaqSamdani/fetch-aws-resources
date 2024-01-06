import pandas as pd
import json

# Read ECS cluster data from the JSON file
with open('../python_output/ecs.json', 'r') as file:
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
    resources.append("ecs")

    # Id/Name
    cluster_name = cluster.get("ClusterName")
    ids_names.append(cluster_name)

    # Owner
    owner_tag = next((tag["Value"] for tag in cluster.get("Tags", []) if tag.get("Key", "").lower() == "owner"), "-") if "Tags" in cluster else "-"
    owners.append(owner_tag)

    # Region
    regions.append(cluster.get("Region", "-"))

    # Email
    email_tag = next((tag["Value"] for tag in cluster.get("Tags", []) if tag.get("Key", "").lower() == "email"), "-") if "Tags" in cluster else "-"
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

# Save to Excel
df.to_excel("../python_execl/ecs_data.xlsx", index=False)
