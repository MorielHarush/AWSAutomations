import subprocess
import json

def run_command(region):
    command = "aws ec2 describe-instances --region " + region
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print("Error:", error.decode())
    return output.decode()

# with open("Regions.txt") as f:
#     regions = f.read().splitlines()

regions = ['us-east-2', 'us-east-1', 'us-west-1', 'us-west-2', 'af-south-1', 'ap-east-1', 'ap-south-2',
           'ap-southeast-3', 'ap-southeast-4', 'ap-south-1',
           'ap-northeast-3', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1',
           'eu-central-1', 'eu-west-1', 'eu-west-2',
           'eu-south-1', 'eu-west-3', 'eu-south-2', 'eu-central-2', 'me-south-1', 'me-central-1', 'sa-east-1',
           'us-gov-west-1']
print("Starting EC2 ALL Regions Enumeration")
with open("output.txt", "w") as output_file:
    for region in regions:
        output = run_command(region)
        if output:
            data = json.loads(output)
            for reservation in data["Reservations"]:
                for instance in reservation["Instances"]:
                    instance_id = instance["InstanceId"]
                    availability_zone = instance["Placement"]["AvailabilityZone"]
                    tags = instance.get("Tags", [])
                    tags_str = ", ".join([f"{tag['Key']}: {tag['Value']}" for tag in tags])

                    output_file.write(f"InstanceId: {instance_id}\n")
                    output_file.write(f"AvailabilityZone: {availability_zone}\n")
                    output_file.write(f"Tags: {tags_str}\n")
                    output_file.write("\n")