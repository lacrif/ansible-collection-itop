# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
name: itop_inventory
extends_documentation_fragment:
    - constructed
version_added: 1.0.0
author:
    - Lacrif
short_description: Itop Inventory Plugin
description:
    - Itop Inventory plugin
    - All vars from itop are prefixed with itop_
options:
    plugin:
        description: Name of the plugin
        required: true
        choices: ['community.itop.itop_inventory']
    url:
        description:
            - URL of Itop server, with protocol (http or https).
              C(url) is an alias for C(server_url).
        required: true
        type: str
    username:
        description:
            - Itop user name.
        required: true
        type: str 
    password:
        description:
            - Itop user password.
        required: true
        type: str
    verify:
        description:
            - SSL Certificate.
        type: str
        default: ''
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
# Connect to itop
plugin: community.itop.itop_inventory
url: 'http://localhost/webservices/rest.php?version=1.3'
username: 'admin'
password: 'admin'
'''

from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ..module_utils.api import ItopApi

class InventoryModule(BaseInventoryPlugin, Constructable):
    NAME = 'community.itop.itop_inventory'

    def verify_file(self, path):
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(("itop.yaml", "itop.yml")):
                return True
            self.display.vvv(
                'Skipping due to inventory source not ending in "itop.yaml" nor "itop.yml"'
            )
        return False

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(
            inventory,
            loader,
            path,
            cache=cache
        )

        self._read_config_data(path)
        
        url = self.get_option('url')
        username = self.get_option('username')
        password = self.get_option('password')
        verify = self.get_option('verify')       
        class_name = self.get_option('class_name')
        key = self.get_option('key')
        output_fields = self.get_option('output_fields')
        page = self.get_option('page')
        limit = self.get_option('limit')
        
        itop_api = ItopApi(
            url,
            username,
            password,
            verify
        )

        itop_data = itop_api.core_get(
            class_name,
            key,
            output_fields,
            page,
            limit
        )
    
        for server in itop_data['objects']:
            inventory_hostname = itop_data['objects'][server]['fields']['name']

            obj_Host = inventory.add_host(host=inventory_hostname, group='all')

            for k in itop_data['objects'][server]['fields']:
                inventory.set_variable(obj_Host, k, itop_data['objects'][server]['fields'][k])
                
            # Get variables for compose
            variables = self.inventory.hosts[inventory_hostname].get_vars()

            # Set composed variables
            self._set_composite_vars(
                self.get_option('compose'),
                variables,
                inventory_hostname,
                self.get_option('strict'),
            )

            # Add host to composed groups
            self._add_host_to_composed_groups(
                self.get_option('groups'),
                variables,
                inventory_hostname,
                self.get_option('strict'),
            )

            # Add host to keyed groups
            self._add_host_to_keyed_groups(
                self.get_option('keyed_groups'),
                variables,
                inventory_hostname,
                self.get_option('strict'),
            )