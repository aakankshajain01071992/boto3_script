# python_script
Python Scripts for various AWS tasks

Here you got python scripts to automate the management of Amazon Web Services (AWS).Before we can get started, you'll need to install Boto3 library in Python and the AWS Command Line Interface (CLI) tool using 'pip' which is a package management system used to install and manage packages that can contain code libraries and dependent files. 

Using 'pip' run the following command to install the AWS CLI and Python's Boto3 library on your machine:

pip install awscli boto3

After creating the user and obtaining the credentials (Access ID and Secret key) by AWS GUI, we can now configure our Python scripting environment with this credential in order to manage AWS services. Use the AWS CI tool to configure these credentials by running the following command from a Bash terminal: 

aws configure

It will prompt you to provide the Access Key ID, Secret Key, Default AWS region, and output format. Once those are provided, credentials are saved in a local file at path ~/.aws/credentials and other configurations like region are stored in ~/.aws/config file.

Now that we've configured our credentials, let's test our any script to check if these credentials work well. for example, to do that, run any python file by below commands: 

python /file_path/ec2-start-stop.py
