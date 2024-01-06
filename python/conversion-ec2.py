import pandas as pd
import json

# Read EC2 data from the JSON file
with open('../python_output/ec2.json', 'r') as file:
    ec2_data = json.load(file)

# Initialize empty lists for each column
resources = []
ids_names = []
owners = []
regions = []
emails = []
statuses = []

# Iterate through the JSON data and extract information
for instance in ec2_data:
    # Resource
    resources.append("ec2")

    # Id/Name
    instance_id = instance.get("InstanceID")
    if instance_id:
        id_name = instance_id
    else:
        tags = instance.get("Tags", [])
        id_name = next((tag.get("Value", "N/A") for tag in tags if tag.get("Key", "").lower() == "name"), "N/A")
    ids_names.append(id_name)

    # Owner
    owner_tag = next((tag["Value"] for tag in instance.get("Tags", []) if tag["Key"].lower() == "owner"), "-") if "Tags" in instance else "-"
    owners.append(owner_tag)

    # Region
    regions.append(instance.get("Region", "-"))

    # Email
    email_tag = next((tag["Value"] for tag in instance.get("Tags", []) if tag["Key"].lower() == "email"), "-") if "Tags" in instance else "-"
    emails.append(email_tag)

    # Required / Terminated
    statuses.append("Required" if instance.get("InstanceState") == "running" else "Terminated")

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
df.to_excel("../python_execl/ec2_data.xlsx", index=False)
