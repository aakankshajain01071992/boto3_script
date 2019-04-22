#!/usr/bin/python3

import boto3
import botocore

# Using amazon S3
s3 = boto3.resource('s3')


filename = 'file.txt'
bucket_name = 'my-bucket'
KEY = 'my_image_in_s3.jpg' # replace with your object key


# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)


# Create an S3 client
s3 = boto3.client('s3')
s3.create_bucket(Bucket=bucket_name)


# By this , we can upload file in the bucket.
s3.upload_file(filename, bucket_name, filename)



# By this , we can download file from the bucket.
s3 = boto3.resource('s3')

try:
    s3.Bucket(bucket_name).download_file(KEY, 'my_local_image.jpg')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise


# By this , we can delete file from the bucket.
s3.Object(bucket_name,filename).delete()  
