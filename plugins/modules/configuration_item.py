#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: configuration_item

version_added: 1.0.0
author:
  - Lacrif

short_description: Create/update/delete iTop configuration item

description: 
  - Create/update/delete iTop configuration item.
  - For more information, refer to the iTop configuration item management documentation at
    U(https://www.itophub.io/wiki/page?id=2_4_0:datamodel:itop-config-mgmt).

seealso:
  - module: community.itop.configuration_item

options:
    class_name:
        description:
            - Configuration item class.
        type: str
        default: 'Server'
    output_fields:
        description:
            - List of table columns to be included as hostvars.
        default: '*'
        type: str
    comment:
        description:
            - Add a comment.
        default: ''
        type: str
    state:
        description:
            - State of the configuration items.
            - On C(present), it will create if host does not exist or update the host if the associated data is different.
            - On C(absent) will remove a host if it exists.
        choices: ["present", "absent"]
        default: "present"
        type: str
    key:
        description:
            - OQL filter item.
        type: dict
    fields:
        description:
            - Data configuration item.
        type: dict  
'''

EXAMPLES = r'''
- name: 'Create first configuration items'
  community.itop.configuration_item:
    class_name: 'VirtualMachine'
    output_fields: ''
    comment: 'Create VirtualMachine'
    fields:
        org_id: "SELECT Organization WHERE name = \"Demo\"",
        virtualhost_id: "SELECT Farm WHERE name = \"Cluster1\"",
        name: "VM10",
        description: "VM 10 !!"
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
        output_fields=dict(type='str', default='*'),
        comment=dict(type='str', required=True),
        fields=dict(type='dict'),
        state=dict(type="str", default='present', choices=['present', 'absent']),
        key=dict(type='dict'),
        page=dict(type='int', default=1),
        limit=dict(type='int', default=0),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False
    )

    changed = True

    try:
        itop_api = ItopApi(
            module.params['url'],
            module.params['username'],
            module.params['password'],
            module.params['verify']
        )

        if module.params['state'] == "absent":
            itop_data = itop_api.core_delete(
                module.params['class_name'],
                module.params['comment'],
                module.params['key']
            )

            if not itop_data['objects']:
                changed = False
            
            module.exit_json(changed=changed, objects=itop_data['objects'])
        else:
            if module.params['key']:
                itop_data = itop_api.core_update(
                    module.params['class_name'],
                    module.params['output_fields'],
                    module.params['comment'],
                    module.params['fields'],
                    module.params['key']
                )
            else:
                itop_data = itop_api.core_create(
                    module.params['class_name'],
                    module.params['output_fields'],
                    module.params['comment'],
                    module.params['fields']
                )

            module.exit_json(changed=changed, objects=itop_data['objects'])
        
    except AnsibleError as e:
        module.fail_json(msg=str(e))

def main():
    run_module()

if __name__ == '__main__':
    main()
