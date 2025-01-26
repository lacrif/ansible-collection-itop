# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
name: itop_inventory
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
        aliases: [ url ]
    user:
        description:
            - Itop user name.
        required: true
        type: str
    password:
        description:
            - Itop user password.
        required: true
        type: str
'''

EXAMPLES = r'''
# Connect to itop
plugin: community.itop.itop_inventory
url: 'http://localhost/webservices/rest.php?version=1.3'
user: 'admin'
password: 'admin'
'''

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin
import requests
import json

class InventoryModule(BaseInventoryPlugin):
    NAME = 'community.itop.itop_inventory'

    def getServer(self, inventory, url, user, password):
        try:
            payload = {
                "operation": "core/get",
                "class": "Server",
                "key": "SELECT Server"
            }
            encoded_data = json.dumps(payload)
            response = requests.post(   
                url, 
                verify=False, 
                data={
                    'auth_user': user, 
                    'auth_pwd': password,
                    'json_data': encoded_data
                }
            )

            itop_data = response.json()

            inventory.add_group('server')

            for server in itop_data['objects']:
                obj_Host = inventory.add_host(host=itop_data['objects'][server]['fields']['name'], group='server')
                inventory.set_variable(obj_Host, 'ansible_host', itop_data['objects'][server]['fields']['managementip'])
                for k in itop_data['objects'][server]['fields']:
                    inventory.set_variable(obj_Host, k, itop_data['objects'][server]['fields'][k])

        except Exception as e:
            raise AnsibleParserError("Invalid data from string, could not parse: %s" % to_native(e))

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(
            inventory,
            loader,
            path,
            cache=cache
        )

        self._read_config_data(path)
        
        self.getServer(
            self.inventory,
            self.get_option('url'),
            self.get_option('user'),
            self.get_option('password')
        )
