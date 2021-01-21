#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# Copyright: (c) 2020, Guy Knights <contact@guyknights.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
---
module: dkron_job
short_description: Create a Dkron job
description:
- Create a Dkron job.
options:
  endpoint:
    description:
      - The IP or hostname of a node in the cluster.
    type: str
    required: true
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
  job_name:
    description:
      - Name of job to create.
    type: string
    required: true
  display_name:
    description:
      - Alternate name of job to create.
    type: string 
  schedule:
    description:
      - Job schedule in 'Dkron' cron format (https://dkron.io/usage/cron-spec/).
      - Not required if the 'toggle' parameter is set to true.
    type: string
    required: true (false if 'toggle' is set to true)
  timezone:
    description:
      - Timezone for job execution.
    type: string
    default: UTC
  owner:
    description:
      - Name of job owner.
    type: string
  owner_email:
    description:
      - Email of job owner.
    type: string
  disabled:
    description:
      - Whether to disable the job when it's created.
    type: bool
    default: false
  tags:
    description:
      - Tags to apply to the job (https://dkron.io/usage/target-nodes-spec/).
    type: dict
  metadata:
    description
      - Metadata to apply to job (https://dkron.io/usage/metatags/).
    type: dict
  retries:
    description:
      - Number of times the job should retry execution on failure.
    type:int
  parent_job:
    description:
      - Name of parent job that this job depends on.
    type: string
  run_on_create:
    description:
      - Run the job immediately after creation.
    type: bool
    default: false
  file_processor:
    description:
      - Dkron file processor configuration (https://dkron.io/usage/processors/file/).
    type: dict
    suboptions:
      log_dir:
        description:
          - Path to the location where the log files will be saved.
        type: string
      forward:
        description:
          - Forward log output to the next processor.
        type: bool
  log_processor:
    description:
      - Dkron log processor configuration (https://dkron.io/usage/processors/log/).
    type: dict
    suboptions:
      forward:
        description:
          - Forward the output to the next processor.
        type: bool
  syslog_processor:
    description:
      - Dkron syslog processor configuration (https://dkron.io/usage/processors/syslog/).
    type: dict
    suboptions:
      forward:
        description:
          - Forward the output to the next processor.
        type: bool
  concurrency:
    description:
      - Allow concurrent job executions.
    type: bool
    default: true
  shell_executor:
    description:
      - Dkron shell executor configuration (https://dkron.io/usage/executors/shell/).
      - Mutually exclusive with http_executor.
    type: dict
    suboptions:
      command:
        description:
          - Shell command to be run.
        type: string
        required: true
      env:
        description:
          - Variables to set in shell environment.
        type: dict
      cwd:
        description:
          - Working directory in which command will be executed.
        type: string
  http_executor:
    description:
      - Dkron HTTP executor configuration (https://dkron.io/usage/executors/http/).
      - Mutually exclusive with shell_executor.
    type: dict
    suboptions:
      method:
        description:
          - HTTP request method (in uppercase).
        type: string
        choices:
          - GET
          - POST
      url:
        description:
          - Request URL.
        type: string
      headers:
        description:
          - HTTP headers.
        type: dict
      body:
        description:
          - POST request body.
        type: string
      timeout:
        description:
          - Request timeout.
        type: int
      expect_code:
        description:
          - HTTP response code to expect.
        type: string
      expect_body:
        description:
          - Response body to expect (supports regexes).
        type: string
      debug:
        description:
          - Enable debug log output.
        type: bool
      tls_verify:
        description:
          - Disable verification of remote SSL cert (if cert required).
        type: bool
        default: true
      tls_cert:
        description:
          - Path to PEM file containing the client cert (if cert required).
        type: string
      tls_key:
        description:
          - Path to PEM file containing the client cert private key (if cert required).
        type: string     
      tls_ca:
        description:
          - Path to PEM file containing certs to use as root CAs (if cert required)
        type: string
  overwrite:
    description:
      - Overwrite the job configuration if it already exists.
      - If this is set to true, a job of the same name exists and the job configuration you pass is the same as the existing configuration, this module will still report the job status as changed.
    type: bool
    default: true
  toggle:
    description:
      - If set to true and job with the same name exists, this will enable/disable the job.
      - If toggle is set the only other parameter required is job_name.
    type: bool
    default: false
  state:
    description:
      - Whether to create/update the job ('present') or remove the job ('absent')
    type: str
    default: present

seealso:
- module: knightsg.dkron.dkron_job_info
- module: knightsg.dkron.dkron_cluster_info

author:
- Guy Knights (contact@guyknights.com)

'''

EXAMPLES = r'''
- name: Create a basic shell executor job that runs on nodes with a specific tag set and retry value
  knightsg.dkron.dkron_job_info:
    endpoint: 192.168.1.1
    job_name: mytestjob1
    displayname: my_alt_job_name_1
    schedule: '0 */10 * * * *'
    timezone: UTC
    owner: 'John Smith'
    owner_email: jsmith@example.com
    tags:
      my_example_tag: somevalue
      my_defined_region: eu1
    retries: 3
    shell_executor
      command: '/bin/sh echo "Hello ${MY_FIRST_NAME} ${MY_LAST_NAME}!"'
      env: 'MYNAME=John,MY_LAST_NAME=Smith"
      cwd: '/home/jsmith'

'''

RETURN = r'''
configuration:
  description: Copy of job configuration (for reference).
  returned: always
  type: complex
  contains: see Dkron usage documentation for complete breakdown of returned values (https://dkron.io/usage/)
  sample: { 
    "name": "mytestjob1",
    "displayname": "my_alt_job_name_1",
    "schedule": "0 */10 * * * *",
    "timezone"": "UTC",
    "owner": "John Smith"
  }
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
        job_name=dict(type='str', required=True),
        display_name=dict(type='str', required=False),
        schedule=dict(type='str', required=False),
        timezone=dict(type='str', required=False, default='UTC'),
        owner=dict(type='str', required=False),
        owner_email=dict(type='str', required=False),
        disabled=dict(type='bool', required=False, default=False),
        tags=dict(type='dict', required=False),
        metadata=dict(type='dict', required=False),
        retries=dict(type='int', required=False, default=0),
        parent_job=dict(type='str', required=False),
        run_on_create=dict(type='bool', required=False, default=False),
        file_processor=dict(type='dict', required=False),
        log_processor=dict(type='dict', required=False),
        syslog_processor=dict(type='dict', required=False),
        concurrency=dict(type='bool', required=False, default=True),
        shell_executor=dict(type='dict', required=False),
        http_executor=dict(type='dict', required=False),
        overwrite=dict(type='bool', required=False, default=True),
        toggle=dict(type='bool', required=False, default=False),
        state=dict(type='str', required=False, default='present')
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

    if module.params['state'] == 'present':

        if not module.params['toggle'] and not module.params['schedule']:
            module.fail_json(msg="Module requires schedule parameter specified unless toggle=true.")

        # Construct job object from parameters
        basic_params = [
          'displayname',
          'schedule',
          'timezone',
          'owner',
          'owner_email',
          'disabled',
          'tags',
          'metadata',
          'retries',
          'parent_job'
        ]

        job_config = {
            'name': module.params['job_name']
        }

        # Add basic parameters directly to job config
        for param in module.params:
          if module.params[param] and param in basic_params:
            job_config[param] = module.params[param]

        # Construct complex parameters and add to job config
        if module.params['concurrency']:
            job_config['concurrency'] = 'allow'
        else:
            job_config['concurrency'] = 'forbid'

        if module.params['file_processor'] or module.params['log_processor'] or module.params['syslog_processor']:
            job_config['processors'] = {}

            if module.params['file_processor']:
              job_config['processors']['files'] = module.params['file_processor']

            if module.params['log_processor']:
              job_config['processors']['log'] = module.params['log_processor']

            if module.params['syslog_processor']:
              job_config['processors']['syslog'] = module.params['syslog_processor']

        if module.params['shell_executor']:
            job_config['executor'] = 'shell'
            job_config['executor_config'] = module.params['shell_executor']

        elif module.params['http_executor']:
            job_config['executor'] = 'http'
            job_config['executor_config'] = module.params['http_executor']

        else:
            module.fail_json(msg="Module requires shell_executor or http_executor parameter specified.")

        # Do create/update
        data, changed = api.upsert_job(job_config)

        if data:
            result['data'] = data
        else:
            result['failed'] = True

        result['changed'] = changed

  else:
    # Delete the job
    pass
    
  module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()