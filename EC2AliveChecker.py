import subprocess
import json

regionname = input("Enter Region: ")
profilename = input("Enter Profile Name: ")
def filter_ec2_instances():
    # Run the AWS CLI command and store the output in a variable
    output = subprocess.check_output(["aws", "ec2", "describe-instances", "--region", regionname, "--profile", profilename], universal_newlines=True)

    # Convert the output to a JSON object
    instances = json.loads(output)

    # Extract the desired parameters and store them in a list
    filtered_instances = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            filtered_instance = {
                'State': instance.get('State', ''),
                'Association': instance['NetworkInterfaces'][0].get('Association', {})
            }
            filtered_instances.append(filtered_instance)

    # Write the filtered instances to a file
    with open("ActuallyRunningInstances.txt", "w") as f:
        for instance in filtered_instances:
            f.write(json.dumps(instance, indent=4) + "\n")

if __name__ == "__main__":
    filter_ec2_instances()
    print("[*] The file ActuallyRunningInstances.txt is ready ! ")