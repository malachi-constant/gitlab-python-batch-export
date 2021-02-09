# gitlab-python-batch-export

## prerequisites
- python3
- argparse
- python-gitlab (https://github.com/python-gitlab/python-gitlab
  )
## usage
```
> python gitlab-export-batch.py -h
usage: gitlab-export-batch.py [-h] [--token TOKEN] [--url URL]
                              [--output-path OUTPUT_PATH]

gitlab batch export

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN, -t TOKEN
                        specify a gitlab access token
  --url URL, -u URL     specify a gitlab api url
  --output-path OUTPUT_PATH, -o OUTPUT_PATH
                        specify an output path for exports
```

### example output
```
> python gitlab-export-batch.py -t HIDINGMYTOKEN
[*] gitlab batch export engine...
[*] creating directories: ['exports']
[*] creating: exports
[*] getting group ids
name: clevertime-blue, id: 10929507
name: this, id: 10929498
[*] listing projects in group: 10929507
[*] getting project ids
name: terraform, id: 24295699
[*] exporting project: terraform
[*] waiting for export of project: terraform...
[*] export completed, downloading to /Users/hansonlu/temp/gitlab-export-batch/exports/group_clevertime-blue_project_terraform_export.tgz...
[*] download completed
[*] exporting group: clevertime-blue
[*] export completed, downloading to /Users/hansonlu/temp/gitlab-export-batch/exports/group_clevertime-blue_export.tgz...
[*] listing projects in group: 10929498
[*] getting project ids
[*] exporting group: this
[*] export completed, downloading to /Users/hansonlu/temp/gitlab-export-batch/exports/group_this_export.tgz...
```
