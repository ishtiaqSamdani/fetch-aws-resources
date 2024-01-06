import pandas as pd
import json

# Read CloudFront data from the JSON file
with open('../python_output/cloudfront.json', 'r') as file:
    cloudfront_data = json.load(file)

# Initialize empty lists for each column
resources = []
ids_names = []
owners = []
regions = []
emails = []
statuses = []

# Iterate through the JSON data and extract information
for distribution in cloudfront_data:
    # Resource
    resources.append("cloudfront")

    # Id/Name
    distribution_id = distribution.get("DistributionId")
    ids_names.append(distribution_id)

    # Owner
    owner_tag = next((tag["Value"] for tag in distribution.get("Tags", []) if tag["Key"].lower() == "owner"), "-") if "Tags" in distribution else "-"
    owners.append(owner_tag)

    # Region
    regions.append(distribution.get("Region", "-"))

    # Email
    email_tag = next((tag["Value"] for tag in distribution.get("Tags", []) if tag["Key"].lower() == "email"), "-") if "Tags" in distribution else "-"
    emails.append(email_tag)

    # Required / Terminated (Assuming CloudFront does not have an instance state, putting "-")
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
df.to_excel("../python_execl/cloudfront_data.xlsx", index=False)
