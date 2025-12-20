# deslicer.splunk.core

This role is a central part of the collection as it holds tasks to check statuses, control notification handlers, and manage Splunk configuration settings.

## Overview

Splunk configuration settings are the main reason why you would want to automate your Splunk Infrastructure. This role provides tasks for initial setup and continuous management of Splunk settings, including SSL certificates and performance tuning.

DRY (Don't repeat yourself) has been an important design philosophy. With so many options to configure in Splunk, we have introduced 3 levels of settings: General, Group, and Host level. These levels are a perfect match between Ansible and Splunk.

**Important:** Settings are not squashed together. Playbook tasks start with configuring general settings, then group settings, and finally host settings. Be careful not to configure conflicting values on different levels.

All settings are managed with the Ansible `ini_file` module. To remove a setting or Splunk stanza, set the state to `absent` and run playbooks against all affected servers before removing from configuration.

## Configuration Levels

### General Level
Settings that apply across all types of Splunk instances.
Location: `environments/ENVIRONMENT_NAME/group_vars/all/general_settings`

### Group Level
Settings specific to an Ansible group (e.g., Splunk role).
Location: `environments/ENVIRONMENT_NAME/group_vars/GROUP_VARS` files

### Host Level
Host-specific settings, useful for cleanup of deprecated or incorrect values.
Location: `environments/ENVIRONMENT_NAME/host_vars/INVENTORY_HOSTNAME` files

## Requirements

When Splunk is already installed, the `splunk.secret` file checksum must match the variable `cca_splunk_secret_sha256` defined in `environments/ENVIRONMENT_NAME/group_vars/all/cca_splunk_secrets`.

## Role Variables

### group_vars/all/cca_splunk_secrets
| Variable | Description |
|----------|-------------|
| `cca_splunk_admin_user` | Configured name for Splunk admin user |
| `cca_splunk_admin_password_hash` | Hashed admin user password |
| `cca_splunk_admin_email` | Admin user email |
| `cca_splunk_local_users` | Additional users to add to local passwd file |
| `cca_splunk_secret` | Splunk secret file stored in Ansible vault |

### group_vars/all/env_specific
| Variable | Description |
|----------|-------------|
| `cca_splunk_extension_licenses` | List of license files to deploy to license manager |
| `preflight_command_retries` | Number of retries for Cluster preflight checks |

### group_vars/all/default
| Variable | Description |
|----------|-------------|
| `dot_managed_by_ansible` | Hidden state file to mark a CCA managed host |
| `file_managed_by_ansible` | Text string added to managed Splunk .conf files |
| `hide_password` | Default `true`, suppress log output where defined |
| `invalid_config_regex` | Invalid characters to search for when validating settings |
| `splunk_path` | Install path for Splunk Enterprise |

### Configurable Variables
| Variable | Description |
|----------|-------------|
| `cca_wait_for_connection_timeout` | Connection timeout value |
| `cluster_bundle_status_command_retries` | Bundle status retries |
| `cluster_peer_rolling_restart_preflight_retries` | Preflight retries |
| `wait_time_cluster_peers_report` | Wait time for cluster peer report |
| `prompt_rolling_restart` | Prompt for user confirmation on rolling restart (default: `false`) |

## Usage

### Include the Role

```yaml
- name: Configure Splunk settings
  ansible.builtin.include_role:
    name: deslicer.splunk.core
```

### Include Specific Tasks

```yaml
- name: Login to Splunk
  ansible.builtin.include_role:
    name: deslicer.splunk.core
    tasks_from: splunk_login.yml
```

## Tasks

### Main Tasks (main.yml)
| Task | Description |
|------|-------------|
| `check_init.yml` | Checks if instance has .ansible_managed file |
| `check_splunk_secret.yml` | Checks and validates splunk.secret file |
| `local_users.yml` | Adds local users to Splunk instance |
| `get_splunk_version.yml` | Gets current Splunk version |
| `precheck_settings.yml` | Scans for invalid characters before applying settings |
| `set_splunk_general_settings.yml` | Sets general Splunk .conf settings |
| `set_splunk_group_settings.yml` | Sets group Splunk .conf settings |
| `set_splunk_host_settings.yml` | Sets host Splunk .conf settings |
| `add_license.yml` | Configures Splunk license files |

### Standalone Tasks
| Task | Description |
|------|-------------|
| `add_search_peers.yml` | Add search peers to monitoring console |
| `apply_cluster_bundle.yml` | Validates and applies cluster bundle |
| `apply_shcluster_bundle.yml` | Applies shcluster bundle on deployer |
| `check_pending_actions.yml` | Checks for pending actions stored as state files |
| `check_preflight_status.yml` | Check Pre-flight status of Cluster Manager |
| `cleanup_shcluster_rolling_restart_file.yml` | Remove state file after shcluster rolling restart |
| `cluster_peer_rolling_restart.yml` | Performs rolling restart of index cluster |
| `get_certificate_status.yml` | Get SSL certificate status |
| `get_splunk_status.yml` | Get running status of Splunk |
| `get_splunk_version.yml` | Get installed Splunk version |
| `notify_splunk.yml` | Call notification handlers based on settings scope |
| `precheck_upgrade_status.yml` | Assert status before starting upgrade |
| `restart_splunkd.yml` | Restart Splunk process |
| `shcluster_members_rolling_restart.yml` | Perform rolling restart of Search head members |
| `splunk_login.yml` | Login to Splunk CLI for authenticated commands |
| `splunk_logout.yml` | Log out from authenticated sessions |
| `wait_for_connection.yml` | Wait until host is reachable |

### Cluster Tasks (cluster/)
| Task | Description |
|------|-------------|
| `get_cluster_status.yml` | Collect Splunk version and cluster status |
| `precheck_upgrade_status.yml` | Assert cluster status before upgrade |
| `splunk_offline.yml` | Stops Splunk process with offline command |

### Search Head Cluster Tasks (shcluster/)
| Task | Description |
|------|-------------|
| `bootstrap_search_head_captain.yml` | Bootstrap search head cluster captain |
| `check_captain_init_status.yml` | Check captain initialization status |
| `check_cluster_member_status.yml` | Check cluster member status |
| `get_shcluster_status.yml` | Collect shcluster status from member nodes |
| `kvstore_engine_upgrade_readiness.yml` | Check KVStore engine upgrade readiness |
| `kvstore_migration_readiness.yml` | Check KVStore migration readiness |
| `migrate_kvstore_engine.yml` | Migrate KVStore engine |
| `precheck_upgrade_status.yml` | Assert shcluster status before upgrade |
| `upgrade_kvstore_engine_version.yml` | Upgrade KVStore engine version |
| `wait_for_shcluster.yml` | Wait for shcluster to stabilize |

### Update Tasks (update/)
| Task | Description |
|------|-------------|
| `main_start.yml` | Start Splunk based on server role |
| `main_stop.yml` | Stop Splunk based on server role |
| `start_splunk.yml` | Start and enable Splunk service |
| `stop_splunk.yml` | Stop and disable Splunk service |
| `start_splunk_on_index_peers.yml` | Start Splunk on cluster peers with maintenance mode |
| `stop_splunk_on_index_peers.yml` | Stop Splunk on cluster peers with maintenance mode |
| `start_splunk_on_searchhead_member.yml` | Start Splunk on search head members |
| `stop_splunk_on_searchhead_member.yml` | Stop Splunk on search head members |
| `enable_maintenance_mode.yml` | Enable maintenance mode on cluster manager |
| `disable_maintenance_mode.yml` | Disable maintenance mode on cluster manager |
| `ensure_shcluster_captaincy.yml` | Ensure proper captaincy before operations |
| `get_adjecent_searchhead_member.yml` | Get adjacent search head member |
| `set_shcluster_captain.yml` | Set search head cluster captain |

## Dependencies

- deslicer.splunk.ssl-certificates (optional, for certificate management)

## License and Attribution

This role is derived from [cca_for_splunk](https://github.com/innovationfleet/cca_for_splunk),
originally developed by Innovation Fleet.

**Original License:** MIT License - Copyright (c) 2024 Innovation Fleet

This role has been adapted for use with the Deslicer Automation Platform by Deslicer AB.

**Copyright (c) 2024 Innovation Fleet**
**Modifications Copyright (c) 2025 Deslicer AB**
