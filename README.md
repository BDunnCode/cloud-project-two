# 📦 Project Overview

This project builds off of an AWS built-from-scratch VPC project that can be investigated at either of these links, this will be particularly relevant for things like installing WSL (Windows Subsystem for Linux), AWS CLI configuration, etc.:

![Github Repository](https://github.com/BDunnCode/cloud-project-one)

![Google Doc](https://docs.google.com/document/d/1Zi_B9YA5hGCHOYtDKuRSE3fleQ5vksCFnkMuWVaqTjk/edit?usp=sharing)

It includes the following sections:

- Project Overview
- Process & Steps
- Post Exercise Reflections


# 🛠️ Tools Used
- AWS Console
- WSL (Window Subsystem for Linux)
- WSL Ubuntu Bash Shell 
- AWS CLI
- Git / Github
- Visual Studio Code
- Python Virtual Environment

# 🔧 Process & Steps

## Prerequisites

### Download and Install Python 3

- Go to https://www.python.org/downloads/
- Left click “Download Python 3.X.X”
- Run the installer
- Check the box that says:
“Add Python 3.x to PATH”
- Click “Install Now” (recommended).
- The installer will set up Python and pip (Python’s package manager).
- Once it finishes, you’ll see a “Setup was successful” message.

- To verify Python installed correctly, open your command prompt and type:

```bash
python -–version
```
or 

```bash
python3 -–version  
```

if you see “Python 3.X.X” it was set up successfully.

- For pip, once again in the command prompt, type: 

```bash
pip -–version  
```

and look for 
a similar response to verify a successfully set up.

### Create a Python Virtual Environment

- Install python3 virtual environment using:

```bash
sudo apt install python3-env
```

- Then type the following command:

```bash 
python3 -m venv ~/.venvs/cloud-scripts
```

### Activate the Environment

- Input the command: 

```bash
source `/.venvs/cloud-scripts/bin/activate
```

### Install boto3

- In the command line, type:

```bash 
pip install boto3
```

### Optional: Auto-activate for convenience

- Edit your .bashrc file. Type:

```bash 
nano ~/.bashrc
```

This will open the nano word editor inside of your shell.

- Using the arrow keys, scroll down to the bottom of the .bashrc file
and input:

```bash
source ~/.venvs/cloud-scripts/bin/activate
```

- Reload the shell using:

```bash
source ~/.bashrc
```

This will make it so that the python3 virtual environment will automatically open upon starting your bash shell. If you want to prevent this from happening, simply open the file and remove “source ~/.venvs/cloud-scripts/bin/activate”. 

If you’d like to exit the virtual environment temporarily, but keep the auto-activation on shell start-up, type:

```bash
deactivate
```

Now you’re ready to start using python scripts via boto3.

# Interacting with AWS VPC via Python and boto3

You should be able to reuse a lot of what was already built in project 1, but you may have deleted some components. If you see you are missing necessary components, consult project 1 for their recreation. That said, we will still repeat a few of the steps from the last project in Python.

## Getting the latest Linux AMI with Python and boto3

We’re getting to the get ID of the latest AMI first, and then use that ID to create a new EC2 instance. Copy the command below:

```bash
import boto3

def get_amazon_linux_2_ami():
	ec2 = boto3.client('ec2')

	response = ec2.describe_images(
    	Owners=['amazon'],
    	Filters=[
        	{'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},
        	{'Name': 'state', 'Values': ['available']},
        	{'Name': 'architecture', 'Values': ['x86_64']},
        	{'Name': 'root-device-type', 'Values': ['ebs']},
        	{'Name': 'virtualization-type', 'Values': ['hvm']}
    	]
	)

	# Sort by CreationDate descending to get the latest one
	images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
	latest_ami = images[0]
	print(f"Latest Amazon Linux 2 AMI ID: {latest_ami['ImageId']}")
	print(f"Name: {latest_ami['Name']}")
	print(f"Creation Date: {latest_ami['CreationDate']}")

if __name__ == "__main__":
	get_amazon_linux_2_ami()
```

