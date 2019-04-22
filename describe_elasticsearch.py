import boto3

client = boto3.client('es')
response = client.list_domain_names()
response1 = client.describe_elasticsearch_domain(
    DomainName=response['DomainNames'][0]['DomainName'])
print(response1)
response2 = client.describe_elasticsearch_domain_config(
    DomainName=response['DomainNames'][0]['DomainName'])
print(response2)

