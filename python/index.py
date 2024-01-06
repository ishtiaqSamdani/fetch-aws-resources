import boto3
import json
from botocore.exceptions import ClientError  # Add this line

def get_all_ec2_instances():
    # Create an EC2 client
    ec2_client = boto3.client('ec2')

    # Get a list of all AWS regions
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    ec2_instances_data = []

    for region in regions:
        # Create a new EC2 client for the current region
        ec2_client = boto3.client('ec2', region_name=region)

        # Get information about all EC2 instances in the region
        response = ec2_client.describe_instances()

        # Iterate through reservations and instances
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_data = {
                    "Region": region,
                    "InstanceID": instance['InstanceId'],
                    "InstanceState": instance['State']['Name'],
                    "Tags": [{"Key": tag['Key'], "Value": tag['Value']} for tag in instance.get('Tags', [])]
                }

                ec2_instances_data.append(instance_data)

    return ec2_instances_data

def get_all_eks_clusters():
    # Create an EKS client
    eks_client = boto3.client('eks')

    # Get a list of all AWS regions
    regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

    eks_clusters_data = []

    for region in regions:
        # Create a new EKS client for the current region
        eks_client = boto3.client('eks', region_name=region)

        # Use paginator to handle paginated responses
        paginator = eks_client.get_paginator('list_clusters')
        response_iterator = paginator.paginate()

        # Iterate through EKS clusters
        for response in response_iterator:
            for cluster_name in response.get('clusters', []):
                cluster_data = {
                    "Region": region,
                    "ClusterName": cluster_name,
                    "Tags": eks_client.list_tags_for_resource(resourceArn=f"arn:aws:eks:{region}:365299945243:cluster/{cluster_name}")['tags']
                }

                eks_clusters_data.append(cluster_data)

    return eks_clusters_data

def get_all_cloudfront_distributions():
    # Create a CloudFront client
    cloudfront_client = boto3.client('cloudfront')

    # Get a list of all AWS regions
    regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

    cloudfront_distributions_data = []

    for region in regions:
        # Create a new CloudFront client for the current region
        cloudfront_client = boto3.client('cloudfront', region_name=region)

        # Use paginator to handle paginated responses
        paginator = cloudfront_client.get_paginator('list_distributions')
        response_iterator = paginator.paginate()

        # Iterate through CloudFront distributions
        for response in response_iterator:
            for distribution in response.get('DistributionList', {}).get('Items', []):
                distribution_data = {
                    "Region": region,
                    "DistributionId": distribution['Id'],
                    "Tags": cloudfront_client.list_tags_for_resource(Resource=distribution['ARN'])['Tags']['Items']
                }

                cloudfront_distributions_data.append(distribution_data)

    return cloudfront_distributions_data

def get_all_elastic_ips():
    # Create an EC2 client
    ec2_client = boto3.client('ec2')

    # Get a list of all AWS regions
    regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

    elastic_ips_data = []

    for region in regions:
        # Create a new EC2 client for the current region
        ec2_client = boto3.client('ec2', region_name=region)

        # Describe Elastic IPs
        response = ec2_client.describe_addresses()

        # Iterate through Elastic IPs
        for elastic_ip in response.get('Addresses', []):
            elastic_ip_data = {
                "Region": region,
                "AllocationId": elastic_ip['AllocationId'],
                "PublicIp": elastic_ip['PublicIp'],
                "Tags": ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [elastic_ip['AllocationId']]}])['Tags']
            }

            elastic_ips_data.append(elastic_ip_data)

    return elastic_ips_data


def get_all_ecr_repositories():
    # Create an ECR client
    ecr_client = boto3.client('ecr')

    # Get a list of all AWS regions
    regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

    ecr_repositories_data = []

    for region in regions:
        # Create a new ECR client for the current region
        ecr_client = boto3.client('ecr', region_name=region)

        # List ECR repositories
        response = ecr_client.describe_repositories()

        # Iterate through ECR repositories
        for repository in response.get('repositories', []):
            repository_data = {
                "Region": region,
                "RepositoryName": repository['repositoryName'],
                "RepositoryUri": repository['repositoryUri'],
                "Tags": ecr_client.list_tags_for_resource(resourceArn=repository['repositoryArn'])['tags']
            }

            ecr_repositories_data.append(repository_data)

    return ecr_repositories_data

def get_all_ecs_clusters():
    # Create an ECS client
    ecs_client = boto3.client('ecs')

    # Get a list of all AWS regions
    regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

    ecs_clusters_data = []

    for region in regions:
        # Create a new ECS client for the current region
        ecs_client = boto3.client('ecs', region_name=region)

        # List ECS clusters
        response = ecs_client.list_clusters()

        # Iterate through ECS clusters
        for cluster_arn in response.get('clusterArns', []):
            cluster_name = cluster_arn.split('/')[1]  # Extract cluster name from ARN
            cluster_data = {
                "Region": region,
                "ClusterName": cluster_name,
                "Tags": ecs_client.list_tags_for_resource(resourceArn=cluster_arn).get('tags', [])
            }

            ecs_clusters_data.append(cluster_data)

    return ecs_clusters_data
def get_all_load_balancers():
    # Create an ELB and ALB client
    elbv2_client = boto3.client('elbv2')

    # Get a list of all AWS regions
    regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

    load_balancers_data = []

    for region in regions:
        # Create a new ELB and ALB client for the current region
        elbv2_client = boto3.client('elbv2', region_name=region)

        # List Load Balancers
        response = elbv2_client.describe_load_balancers()

        # Iterate through Load Balancers
        for lb in response.get('LoadBalancers', []):
            load_balancer_data = {
                "Region": region,
                "LoadBalancerArn": lb['LoadBalancerArn'],
                "LoadBalancerName": lb.get('LoadBalancerName', ''),
                "Scheme": lb.get('Scheme', ''),
                "Tags": elbv2_client.describe_tags(ResourceArns=[lb['LoadBalancerArn']])['TagDescriptions'][0].get('Tags', [])
            }

            load_balancers_data.append(load_balancer_data)

    return load_balancers_data

def get_all_rds_instances():
    # Create an RDS client
    rds_client = boto3.client('rds')

    # Get a list of all AWS regions
    regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

    rds_instances_data = []

    for region in regions:
        # Create a new RDS client for the current region
        rds_client = boto3.client('rds', region_name=region)

        # List RDS instances
        response = rds_client.describe_db_instances()

        # Iterate through RDS instances
        for db_instance in response.get('DBInstances', []):
            rds_instance_data = {
                "Region": region,
                "DBInstanceIdentifier": db_instance['DBInstanceIdentifier'],
                "DBInstanceArn": db_instance['DBInstanceArn'],
                "Tags": rds_client.list_tags_for_resource(ResourceName=db_instance['DBInstanceArn']).get('TagList', [])
            }

            rds_instances_data.append(rds_instance_data)

    return rds_instances_data

def main():


    ec2_instances_data = get_all_ec2_instances()
    # Write EC2 instances data to ec2.json
    with open('../python_output/ec2.json', 'w') as ec2_json_file:
        json.dump(ec2_instances_data, ec2_json_file, indent=2)

    eks_clusters_data = get_all_eks_clusters()
    # Write EKS clusters data to eks.json
    with open('../python_output/eks.json', 'w') as eks_json_file:
        json.dump(eks_clusters_data, eks_json_file, indent=2)

    cloudfront_distributions_data = get_all_cloudfront_distributions()
    with open('../python_output/cloudfront.json', 'w') as cloudfront_json_file:
        json.dump(cloudfront_distributions_data, cloudfront_json_file, indent=2)
        
    elastic_ips_data = get_all_elastic_ips()
    # Write Elastic IPs data to elasticip.json
    with open('../python_output/elasticip.json', 'w') as elasticip_json_file:
        json.dump(elastic_ips_data, elasticip_json_file, indent=2)

    ecr_repositories_data = get_all_ecr_repositories()
    # Write ECR repositories data to ecr.json
    with open('../python_output/ecr.json', 'w') as ecr_json_file:
        json.dump(ecr_repositories_data, ecr_json_file, indent=2)
    
    ecs_clusters_data = get_all_ecs_clusters()
    with open('../python_output/ecs.json', 'w') as ecs_json_file:
        json.dump(ecs_clusters_data, ecs_json_file, indent=2)
    # Write Load Balancers data to loadbalancer.json

    load_balancers_data = get_all_load_balancers()
    with open('../python_output/loadbalancer.json', 'w') as loadbalancer_json_file:
        json.dump(load_balancers_data, loadbalancer_json_file, indent=2)

    rds_instances_data = get_all_rds_instances()
    # Write RDS instances data to rds.json
    with open('../python_output/rds.json', 'w') as rds_json_file:
        json.dump(rds_instances_data, rds_json_file, indent=2)


if __name__ == "__main__":
    main()
