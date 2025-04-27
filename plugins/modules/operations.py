#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: operations

version_added: 1.0.0
author:
    - Lacrif
short_description: This is my test module
description: 
    - This is my longer description explaining my test module.
options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.api:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.api:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.api:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.errors import AnsibleError
from ansible.module_utils.basic import AnsibleModule

from ..module_utils.base import (itop_argument_spec)
from ..module_utils.api import ItopApi

def run_module():
    # define available arguments/parameters a user can pass to the module
    argument_spec = itop_argument_spec()

    # the AnsibleModule object will be our abstraction working with Ansible
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    
    try:
        itop_api = ItopApi(
            module.params['url'],
            module.params['username'],
            module.params['password'],
            module.params['verify']
        )
        itop_data = itop_api.list_operations()

        module.exit_json(changed=False, objects=itop_data)
    except AnsibleError as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()
