import boto3
client = boto3.client('emr')
response = client.list_clusters()
for i in range(len(response['Clusters'])):
    if ( response['Clusters'][i]['Status']['State'] == "WAITING" ):
        cluster_id = response['Clusters'][i]['Id']
        cid = client.describe_cluster(ClusterId=cluster_id)
        print(cid['Cluster']['MasterPublicDnsName'])

