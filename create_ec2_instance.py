import boto3

# Replace these with your real values
AMI_ID = 'ami-0ddac208607ae06a0'
INSTANCE_TYPE = 't2.micro'
KEY_NAME = 'key-pair-xx'
SECURITY_GROUP_IDS = ['sg-123456789']  # Must exist in your VPC
SUBNET_ID = 'subnet-123456789'   # Must be public if you want external access


def launch_instance():
	ec2 = boto3.client('ec2')

	response = ec2.run_instances(
    	ImageId=AMI_ID,
    	InstanceType=INSTANCE_TYPE,
    	KeyName=KEY_NAME,
    	MaxCount=1,
    	MinCount=1,
    	SecurityGroupIds=SECURITY_GROUP_IDS,
    	SubnetId=SUBNET_ID,
    	TagSpecifications=[
        	{
            	'ResourceType': 'instance',
            	'Tags': [
                	{'Key': 'Name', 'Value': 'Boto3-Launched-Instance'},
            	]
        	}
    	]
	)

	instance_id = response['Instances'][0]['InstanceId']
	print(f"Launched instance with ID: {instance_id}")

if __name__ == "__main__":
	launch_instance()
