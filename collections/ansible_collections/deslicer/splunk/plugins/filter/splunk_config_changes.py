# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Innovation Fleet
# Copyright: (c) 2026, Deslicer AB
# MIT License (see LICENSE)

"""Splunk configuration changes analyzer filter plugin."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
name: analyze_splunk_changes
short_description: Analyze Splunk configuration changes and determine required actions
version_added: "0.1.0"
description:
  - Analyzes a list of Splunk configuration change results and determines what actions are needed.
  - Detects if splunkd restart, deployment server reload, deployer push, or cluster manager push is required.
  - Uses path patterns to categorize changes by their target (local config, deployment-apps, shcluster, master-apps).
positional: results
options:
  results:
    description:
      - List of configuration change results, each containing 'changed' and 'path' keys.
    type: list
    elements: dict
    required: true
  rolling_restart_pending:
    description:
      - Whether a rolling restart is already pending.
    type: bool
    default: false
  splunkd_restart_pending:
    description:
      - Whether a splunkd restart is already pending.
    type: bool
    default: false
  force_splunkd_restart:
    description:
      - Force splunkd restart regardless of changes.
    type: bool
    default: false
  force_bundle_push:
    description:
      - Force deployer bundle push regardless of changes.
    type: bool
    default: false
author:
  - Roger Lindquist (@rlinq)
  - Deslicer AB
'''

EXAMPLES = r'''
# Analyze configuration changes
- name: Analyze what actions are needed
  ansible.builtin.set_fact:
    required_actions: "{{ config_results | deslicer.splunk.analyze_splunk_changes }}"

# With additional flags
- name: Analyze changes with force restart
  ansible.builtin.set_fact:
    required_actions: >-
      {{ config_results | deslicer.splunk.analyze_splunk_changes(
           rolling_restart_pending=true,
           force_splunkd_restart=true
         ) }}

# Example input:
# config_results:
#   - changed: true
#     path: /opt/splunk/etc/system/local/server.conf
#   - changed: true
#     path: /opt/splunk/etc/deployment-apps/my_app/local/inputs.conf
#   - changed: false
#     path: /opt/splunk/etc/apps/search/local/props.conf
'''

RETURN = r'''
_value:
  description: Dictionary of required actions based on configuration changes.
  type: dict
  contains:
    splunkd_restart_pending:
      description: Whether splunkd restart is needed for local config changes.
      type: bool
    deploymentserver_reload:
      description: Whether deployment server reload is needed.
      type: bool
    deployer_push:
      description: Whether search head cluster deployer push is needed.
      type: bool
    cluster_manager_push:
      description: Whether cluster manager bundle push is needed.
      type: bool
    splunkd_restart:
      description: Whether rolling restart was requested (only present if rolling_restart_pending=true).
      type: bool
'''

import re


def analyze_splunk_changes(results, rolling_restart_pending=False, splunkd_restart_pending=False,
                           force_splunkd_restart=False, force_bundle_push=False):
    """Analyze Splunk configuration changes and determine required actions.

    Args:
        results: List of configuration change results with 'changed' and 'path' keys.
        rolling_restart_pending: Whether a rolling restart is already pending.
        splunkd_restart_pending: Whether a splunkd restart is already pending.
        force_splunkd_restart: Force splunkd restart regardless of changes.
        force_bundle_push: Force deployer bundle push regardless of changes.

    Returns:
        Dictionary of required actions.
    """
    actions = {
        'splunkd_restart_pending': force_splunkd_restart or splunkd_restart_pending,
        'deploymentserver_reload': False,
        'deployer_push': force_bundle_push,
        'cluster_manager_push': False,
    }

    if rolling_restart_pending:
        actions['splunkd_restart'] = True

    for item in results:
        if item['changed']:
            path = item.get('path', '')
            if bool(re.search('.*/etc/(?!deployment-apps|shcluster|master-apps|manager-apps).*?$', path)):
                actions['splunkd_restart_pending'] = True
            elif 'deployment-apps' in path:
                actions['deploymentserver_reload'] = True
            elif 'shcluster' in path:
                actions['deployer_push'] = True
            elif 'master-apps' in path or 'manager-apps' in path:
                actions['cluster_manager_push'] = True

    return actions


class FilterModule(object):
    """Ansible filter plugin for analyzing Splunk configuration changes."""

    def filters(self):
        """Return the filter plugin mapping."""
        return {
            'analyze_splunk_changes': analyze_splunk_changes
        }
