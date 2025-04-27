#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: configuration_item_info

version_added: 1.0.0
author:
  - Lacrif

short_description: List iTop configuration item

description: 
  - Retrieve information about the iTop configuration items.
  - For more information, refer to the iTop configuration item management documentation at
    U(https://www.itophub.io/wiki/page?id=2_4_0:datamodel:itop-config-mgmt).

seealso:
  - module: community.itop.configuration_item_info

options:
    class_name:
        description:
            - Configuration item class.
        type: str
        default: 'Server'
    key:
        description:
            - query OQL.
        type: str
        default: 'SELECT Server'
    output_fields:
        description:
            - List of table columns to be included as hostvars.
        type: str
        default: '*'
    limit:
        description:
            - Amount of results to return (default: 0 = no limit)
        type: int
        default: 0
    page:
        description:
            - Page number to return (cannot be < 1)
        type: int
        default: 1
'''

EXAMPLES = r'''
- name: 'Retrieve 2 first configuration items'
  community.itop.configuration_item_info:
    class_name: 'Server'
    key: 'SELECT Server'
    output_fields: 'name, osfamily_name, status'
    page: 1
    limit: 2
  register: api_servers
'''

from ansible.errors import AnsibleError
from ansible.module_utils.basic import AnsibleModule

from ..module_utils.base import (itop_argument_spec)
from ..module_utils.api import ItopApi

def run_module():
    # define available arguments/parameters a user can pass to the module
    argument_spec = itop_argument_spec()
    argument_spec.update(
        class_name=dict(type='str', required=True),
        key=dict(type='str', required=True),
        output_fields=dict(type='str', default='*'),
        page=dict(type='int', default=1),
        limit=dict(type='int', default=0)
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False
    )
    
    try:
        itop_api = ItopApi(
            module.params['url'],
            module.params['username'],
            module.params['password'],
            module.params['verify']
        )
        itop_data = itop_api.core_get(
            module.params['class_name'],
            module.params['key'],
            module.params['output_fields'],
            module.params['page'],
            module.params['limit']
        )

        module.exit_json(changed=False, objects=itop_data['objects'])
    except AnsibleError as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()
