import subprocess
import json

def filter_ec2_instances():
    # Run the AWS CLI command and store the output in a variable
    output = subprocess.check_output(["aws", "ec2", "describe-instances", "--region", "us-east-1"], universal_newlines=True)

    # Convert the output to a JSON object
    instances = json.loads(output)

    # Extract the desired parameters and store them in a list
    filtered_instances = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            filtered_instance = {
                'ImageId': instance.get('ImageId', ''),
                'InstanceId': instance.get('InstanceId', ''),
                'InstanceType': instance.get('InstanceType', ''),
                'KeyName': instance.get('KeyName', ''),
                'SecurityGroups': instance.get('SecurityGroups', []),
                'Tags': instance.get('Tags', []),
                'Placement': instance.get('Placement', {}),
                'IamInstanceProfile': instance.get('IamInstanceProfile', {})
            }
            filtered_instances.append(filtered_instance)

    # Write the filtered instances to a file
    with open("ec2machine.txt", "w") as f:
        for instance in filtered_instances:
            f.write(json.dumps(instance, indent=4) + "\n")

if __name__ == "__main__":
    filter_ec2_instances()