# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Innovation Fleet
# Copyright: (c) 2026, Deslicer AB
# MIT License (see LICENSE)

"""Splunk configuration flatten filter plugin."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
name: splunk_conf_flatten
short_description: Flatten Splunk configuration data structure
version_added: "0.1.0"
description:
  - Takes a nested Splunk configuration structure and flattens it into a list of individual settings.
  - Each setting includes path, section, option, value, state, and comment.
positional: conf_groups
options:
  conf_groups:
    description:
      - List of configuration groups containing filepath, filename, and sections with options.
    type: list
    elements: dict
    required: true
author:
  - Roger Lindquist (@rlinq)
  - Deslicer AB
'''

EXAMPLES = r'''
# Flatten Splunk configuration data
- name: Flatten configuration settings
  ansible.builtin.set_fact:
    flat_config: "{{ splunk_conf_settings | deslicer.splunk.splunk_conf_flatten }}"

# Example input structure:
# splunk_conf_settings:
#   - filepath: /opt/splunk/etc/system/local
#     filename: server.conf
#     sections:
#       - section: general
#         options:
#           - option: serverName
#             value: my-splunk-server
#           - option: pass4SymmKey
#             value: $7$encrypted
#             state: present
'''

RETURN = r'''
_value:
  description: List of flattened configuration entries.
  type: list
  elements: dict
  contains:
    path:
      description: Full path to the configuration file.
      type: str
    section:
      description: Configuration section name.
      type: str
    option:
      description: Configuration option name.
      type: str
    value:
      description: Configuration option value.
      type: str
    state:
      description: State of the option (present/absent).
      type: str
    comment:
      description: Optional comment for the option.
      type: str
'''

from ansible.errors import AnsibleFilterError


def splunk_conf_flatten(conf_groups):
    """Flatten Splunk configuration data structure.

    Args:
        conf_groups: List of configuration groups with filepath, filename, and sections.

    Returns:
        List of flattened configuration entries.

    Raises:
        AnsibleFilterError: If there's an error processing the configuration data.
    """
    try:
        flattened_data = []
        for group in conf_groups:
            filepath = group.get('filepath')
            filename = group.get('filename')
            for section in group.get('sections', []):
                section_name = section.get('section')
                if section_name != '':
                    for option in section.get('options', []):
                        flattened_data.append({
                            'path': filepath + '/' + filename,
                            'section': section_name,
                            'option': option.get('option'),
                            'value': option.get('value'),
                            'state': option.get('state', 'present'),
                            'comment': option.get('comment', ''),
                        })
        return flattened_data
    except Exception as e:
        raise AnsibleFilterError('Error flattening configuration data: {}'.format(e))


class FilterModule(object):
    """Ansible filter plugin for flattening Splunk configuration data."""

    def filters(self):
        """Return the filter plugin mapping."""
        return {
            'splunk_conf_flatten': splunk_conf_flatten
        }
