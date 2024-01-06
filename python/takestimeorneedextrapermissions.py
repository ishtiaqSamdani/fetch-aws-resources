import boto3
import json
from botocore.exceptions import ClientError

def get_all_s3_buckets():
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Get a list of all AWS regions
    regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

    s3_buckets_data = []

    for region in regions:
        # Create a new S3 client for the current region
        s3_client = boto3.client('s3', region_name=region)

        # List S3 buckets
        response = s3_client.list_buckets()

        # Iterate through S3 buckets
        for bucket in response.get('Buckets', []):
            try:
                # Attempt to get bucket tagging, handle NoSuchTagSet error
                tags = s3_client.get_bucket_tagging(Bucket=bucket['Name']).get('TagSet', [])
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchTagSet':
                    tags = []
                else:
                    raise  # Re-raise any other unexpected error

            bucket_data = {
                "Region": region,
                "BucketName": bucket['Name'],
                "Tags": tags
            }

            s3_buckets_data.append(bucket_data)

    return s3_buckets_data
    

def get_all_kms_keys():
    # Create a KMS client
    kms_client = boto3.client('kms')

    # Get a list of all AWS regions
    regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

    kms_keys_data = []

    for region in regions:
        # Create a new KMS client for the current region
        kms_client = boto3.client('kms', region_name=region)

        # List KMS keys
        response = kms_client.list_keys()

        # Iterate through KMS keys
        for key in response.get('Keys', []):
            kms_key_data = {
                "Region": region,
                "KeyId": key['KeyId'],
                "KeyArn": key['KeyArn'],
                "Tags": kms_client.list_resource_tags(KeyId=key['KeyId']).get('Tags', [])
            }

            kms_keys_data.append(kms_key_data)

    return kms_keys_data

def main():
    s3_buckets_data = get_all_s3_buckets()
    kms_keys_data = get_all_kms_keys()

    # Write S3 buckets data to s3.json
    with open('s3.json', 'w') as s3_json_file:
        json.dump(s3_buckets_data, s3_json_file, indent=2)

    # Write KMS keys data to kms.json
    with open('kms.json', 'w') as kms_json_file:
        json.dump(kms_keys_data, kms_json_file, indent=2)

if __name__ == "__main__":
    main()
