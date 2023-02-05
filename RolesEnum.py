import subprocess
import json


def run_command(username):
    command = "aws iam list-roles --profile " + username
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print("Error:", error.decode())
    return output.decode()


username = input("Enter your AWS profile name: ")
output = run_command(username)
print("Roles.txt is Ready!")

if output:
    data = json.loads(output)
    with open("Roles.txt", "w") as roles_file:
        for role in data["Roles"]:
            role_name = role["RoleName"]
            role_id = role["RoleId"]
            description = role.get("Description", "")
            arn = role["Arn"]
            statement = role["AssumeRolePolicyDocument"]["Statement"]
            statement_str = ", ".join([f"{key}: {value}" for dic in statement for key, value in dic.items()])
            roles_file.write(f"RoleName: {role_name}\n")
            roles_file.write(f"RoleId: {role_id}\n")
            roles_file.write(f"Description: {description}\n")
            roles_file.write(f"Arn: {arn}\n")
            roles_file.write(f"Statement: {statement_str}\n")
            roles_file.write("\n")
