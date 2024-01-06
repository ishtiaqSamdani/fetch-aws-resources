import os
import pandas as pd
import json

# Read ELB data from the JSON file
with open('../python_output/loadbalancer.json', 'r') as file:
    elb_data = json.load(file)

# Initialize empty lists for each column
resources = []
ids_names = []
owners = []
regions = []
emails = []
statuses = []

# Iterate through the JSON data and extract information
for elb in elb_data:
    # Resource
    resources.append("elb")

    # Id/Name
    load_balancer_arn = elb.get("LoadBalancerName")
    ids_names.append(load_balancer_arn)

    # Owner
    owner_tag = next((tag["Value"] for tag in elb.get("Tags", []) if tag.get("Key", "").lower() == "owner"), "-") if "Tags" in elb else "-"
    owners.append(owner_tag)

    # Region
    regions.append(elb.get("Region", "-"))

    # Email
    email_tag = next((tag["Value"] for tag in elb.get("Tags", []) if tag.get("Key", "").lower() == "email"), "-") if "Tags" in elb else "-"
    emails.append(email_tag)

    # Required / Terminated (Assuming ELB does not have a specific state, putting "-")
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
df.to_excel("../python_execl/loadbalancer_data.xlsx", index=False)
