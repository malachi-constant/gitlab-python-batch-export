import os
import json
import gitlab
import time
import argparse

# functions
def get_group_ids():
    ''' get list of gitlab group ids '''
    groups = gl.groups.list()

    group_ids = []
    print("[*] getting group ids")
    for group in groups:
        group_ids.append(group.id)
        print(f"name: {group.name}, id: {group.id}")

    return group_ids

def get_project_ids(group_id):
    ''' get list of gitlab project ids based off a group id'''
    group = gl.groups.get(group_id)
    projects = group.projects.list()

    project_ids = []
    print("[*] getting project ids")
    for project in projects:
        project_ids.append(project.id)
        print(f"name: {project.name}, id: {project.id}")

    return project_ids

def export_project(project_id, group_id, output_path):
    # Create the export
    group = gl.groups.get(group_id)
    project = gl.projects.get(project_id)
    print(f"[*] exporting project: {project.name}")
    export = project.exports.create()

    # Wait for the 'finished' status
    export.refresh()
    while export.export_status != 'finished':
        print(f"[*] waiting for export of project: {project.name}...")
        time.sleep(1)
        export.refresh()

    current_path = os.getcwd()
    filename = f"{current_path}/{output_path}/group_{group.name}_project_{project.name}_export.tgz"
    print(f"[*] export completed, downloading to {filename}...")

    # Download the result
    with open(filename, 'wb') as file:
        export.download(streamed=True, action=file.write)

    print(f"[*] download completed")

def export_group(group_id, output_path):
    group = gl.groups.get(group_id)
    print(f"[*] exporting group: {group.name}")
    export = group.exports.create()

    # Wait for the export to finish
    time.sleep(3)
    current_path = os.getcwd()
    filename = f"{current_path}/{output_path}/group_{group.name}_export.tgz"
    print(f"[*] export completed, downloading to {filename}...")

    # Download the result
    with open(filename, 'wb') as file:
        export.download(streamed=True, action=file.write)

def create_output_directories(output_path):

    directories = output_path.split("/")
    print(f"[*] creating directories: {directories}")
    for i in range(len(directories)):
        if len(directories) == 1:
            directory = "".join(directories[0:i+1])
        else:
            directory = "/".join(directories[0:i+1])
        print(f"[*] creating: {directory}")
        try:
            os.mkdir(directory)
        except Exception as e:
            print(f"!{e}")


# program arguments
parser = argparse.ArgumentParser(description='gitlab batch export')
parser.add_argument('--token','-t', dest='token', required=False,help='specify a gitlab access token')
parser.add_argument('--url','-u', dest='url', required=False, default='https://gitlab.com',help='specify a gitlab api url')
parser.add_argument('--output-path','-o', dest='output_path', required=False, default='exports',help='specify an output path for exports')
args = parser.parse_args()

# globals
gitlab_token = args.token
gitlab_url = args.url
output_path = args.output_path
gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)

# logic
print('[*] gitlab batch export engine...')
create_output_directories(output_path)

group_ids = get_group_ids()

for group_id in group_ids:
    print(f"[*] listing projects in group: {group_id}")
    project_ids = get_project_ids(group_id)

    for project_id in project_ids:
        export_project(project_id, group_id, output_path)

    export_group(group_id, output_path)
