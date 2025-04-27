#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import env_fallback

def itop_argument_spec():
    return dict(
        url=dict(
            type='str', 
            required=True, 
            fallback=(env_fallback, ["ITOP_URL"])
        ),
        username=dict(
            type='str', 
            required=True, 
            fallback=(env_fallback, ["ITOP_USERNAME"])
        ),
        password=dict(
            type='str', 
            required=True, 
            fallback=(env_fallback, ["ITOP_PASSWORD"])
        ),
        verify=dict(
            type='str', 
            required=True, 
            fallback=(env_fallback, ["ITOP_VERIFY"])
        )
    )