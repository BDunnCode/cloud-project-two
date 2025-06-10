#!/usr/bin/env python3

import boto3
import argparse
import sys
import logging

# Setup logging
logging.basicConfig(
    filename='ec2_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def start_instance(ec2, instance_id):
    try:
        response = ec2.start_instances(InstanceIds=[instance_id])
        state = response['StartingInstances'][0]['CurrentState']['Name']
        print(f"✅ Instance {instance_id} is now {state}.")
        logging.info(f"Started instance: {instance_id}, now {state}")
    except Exception as e:
        print(f"❌ Error starting instance: {e}")
        logging.error(f"Error starting instance {instance_id}: {e}")

def stop_instance(ec2, instance_id):
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        state = response['StoppingInstances'][0]['CurrentState']['Name']
        print(f"🛑 Instance {instance_id} is now {state}.")
        logging.info(f"Stopped instance: {instance_id}, now {state}")
    except Exception as e:
        print(f"❌ Error stopping instance: {e}")
        logging.error(f"Error stopping instance {instance_id}: {e}")

def terminate_instance(ec2, instance_id):
    try:
        response = ec2.terminate_instances(InstanceIds=[instance_id])
        state = response['TerminatingInstances'][0]['CurrentState']['Name']
        print(f"💀 Instance {instance_id} is now {state}.")
        logging.info(f"Terminated instance: {instance_id}, now {state}")
    except Exception as e:
        print(f"❌ Error terminating instance: {e}")
        logging.error(f"Error terminating instance {instance_id}: {e}")

def list_instances(ec2):
    try:
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                name = next(
                    (tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'),
                    'Unnamed'
                )
                print(f"{instance_id} | {state} | {name}")
        logging.info("Listed instances successfully.")
    except Exception as e:
        print(f"❌ Error listing instances: {e}")
        logging.error(f"Error listing instances: {e}")

def main():
    parser = argparse.ArgumentParser(description="Manage EC2 instances: start, stop, terminate, list")
    parser.add_argument('--action', choices=['start', 'stop', 'terminate', 'list'], required=True, help="Action to take")
    parser.add_argument('--instance-id', help="EC2 instance ID (not required for 'list')")

    args = parser.parse_args()
    ec2 = boto3.client('ec2')

    if args.action == 'start':
        if not args.instance_id:
            print("❗️ --instance-id is required for 'start'")
            return
        start_instance(ec2, args.instance_id)

    elif args.action == 'stop':
        if not args.instance_id:
            print("❗️ --instance-id is required for 'stop'")
            return
        stop_instance(ec2, args.instance_id)

    elif args.action == 'terminate':
        if not args.instance_id:
            print("❗️ --instance-id is required for 'terminate'")
            return
        terminate_instance(ec2, args.instance_id)

    elif args.action == 'list':
        list_instances(ec2)

    else:
        print("❌ Invalid action.")
        sys.exit(1)

if __name__ == "__main__":
    main()