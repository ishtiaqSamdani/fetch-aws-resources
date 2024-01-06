import pandas as pd
import json

# Read RDS data from the JSON file
with open('../python_output/rds.json', 'r') as file:
    rds_data = json.load(file)

# Initialize empty lists for each column
resources = []
ids_names = []
owners = []
regions = []
emails = []
statuses = []

# Iterate through the JSON data and extract information
for rds_instance in rds_data:
    # Resource
    resources.append("rds")

    # Id/Name
    db_instance_identifier = rds_instance.get("DBInstanceIdentifier")
    ids_names.append(db_instance_identifier)

    # Owner
    owner_tag = next((tag["Value"] for tag in rds_instance.get("Tags", []) if tag.get("Key", "").lower() == "owner"), "-") if "Tags" in rds_instance else "-"
    owners.append(owner_tag)

    # Region
    regions.append(rds_instance.get("Region", "-"))

    # Email (Assuming RDS does not have an email tag, putting "-")
    emails.append("-")

    # Required / Terminated (Assuming RDS does not have a specific state, putting "-")
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
df.to_excel("../python_execl/rds_data.xlsx", index=False)
