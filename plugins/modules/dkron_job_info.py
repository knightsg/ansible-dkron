#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# Copyright: (c) 2020, Guy Knights <contact@guyknights.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: dkron_job_info
short_description: Gathers information about jobs in a Dkron cluster
description:
- Gathers information about jobs in a Dkron cluster.
options:
  endpoint:
    description:
      - The IP or hostname of a node in the cluster.
    type: str
  port:
    description:
      - The port used to connect to the cluster node.
    type: int
    default: 8080
  username:
    description:
      - The username, if the cluster is protected by a reverse proxy with basic authentication.
    type: str
  password:
    description:
      - The password, if the cluster is protected by a reverse proxy with basic authentication.
    type: str
  use_ssl:
    descrption:
      - Use HTTPS to connect to the cluster node instead of HTTP.
    type: bool
  job_names:
    description:
      - Name (or list of names) of job to query.
      - Will query all jobs if omitted.
    type: list
    aliases:
      - job_name
  limit_history:
    description
      - Limit the history returned for each job to the amount specified by this parameter (eg. 5)
      - Will return full history for each job if omitted.
    type: int

seealso:
- module: knightsg.dkron.dkron_job
- module: knightsg.dkron.dkron_cluster_info

author:
- Guy Knights (contact@guyknights.com)

'''

EXAMPLES = r'''
- name: Get config and full history for all defined jobs
  knightsg.dkron.dkron_job_info:
    endpoint: 192.168.1.1

- name: Get config and full history for a list of jobs from secured cluster
  knightsg.dkron.dkron_job_info:
    endpoint: myclusterendpoint.com
    use_ssl: true
    username: myusername
    password: mypassword
    job_names:
      - my_job_1
      - my_job_2
      - my_job_3

- name: Get config for all defined jobs but limit history to last execution only
  knightsg.dkron.dkron_job_info:
    endpoint: 192.168.1.1
    limit_history: 1

'''

RETURN = r'''
configuration:
  description: Job configuration as returned by the Dkron cluster API (https://dkron.io/api/).
  returned: always
  type: dict
  sample: { "concurrency": "allow", "dependent_jobs": null, "disabled": false, "displayname": "", "error_count": 0, "executor": "shell", "executor_config": { "command": "/bin/true" }, "last_error": null, "last_success": "2020-11-14T17:32:15.010781048Z", "metadata": null, "name": "job", "next": "2020-11-14T17:33:15Z", "owner": "guy", "owner_email": "someone@example.com", "parent_job": "", "processors": {}, "retries": 0, "schedule": "@every 1m", "status": "success", "success_count": 185, "tags": { "server": "true:1" }, "timezone": ""}
  contains: see Dkron usage documentation for complete breakdown of returned values (https://dkron.io/usage/)
history:
  description: List of job executions with result status.
  returned: always
  type: dict
  sample: { "attempt": 1, "finished_at": "2020-11-14T17:32:15.010781048Z", "group": 1605375135000263778, "job_name": "job", "node_name": "myhostname", "started_at": "2020-11-14T17:32:15.007570195Z", "success": true }
  
'''

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.knightsg.dkron.plugins.module_utils.dkron import DkronAPI

def run_module():
    module_args = dict(
        endpoint=dict(type='str', required=True),
        port=dict(type='int', required=False, default=8080),
        username=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        use_ssl=dict(type='bool', required=False, default=False),
        job_names=dict(type='list', required=False, aliases=['job_name']),
        limit_history=dict(type='int', required=False)
    )

    result = dict(
        changed=False,
        failed=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    api = DkronAPI(module)

    data, changed = api.get_job_info()

    if data:
        result['data'] = data
    else:
        result['failed'] = True

    result['changed'] = changed
    
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()