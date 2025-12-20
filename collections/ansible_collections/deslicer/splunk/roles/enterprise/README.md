# deslicer.splunk.enterprise

Start, stop, install, and upgrade Splunk Enterprise. Manage cluster-specific commands for rolling upgrades.

This role supports Ansible check mode and will run through all tasks and validate everything possible without actually performing the upgrade.

## Requirements

Splunk tgz file needs to be stored in the infrastructure directory at `splunk/var/images/` where they will be matched by the `splunk_enterprise_version` specified in the hosts inventory file.

## Role Variables

### group_vars/hosts
| Variable | Description |
|----------|-------------|
| `splunk_enterprise_version` | Set the desired version of Splunk Enterprise |

### group_vars/all/cca_splunk_secrets
| Variable | Description |
|----------|-------------|
| `splunk_cli_user` | Splunk CLI user (can differ from admin user) |
| `splunk_cli_user_password` | Splunk CLI user password |

### group_vars/all/default
| Variable | Description |
|----------|-------------|
| `hide_password` | Suppress password output in logs |
| `splunk_path` | Install path for Splunk Enterprise |
| `start_command` | Command to start Splunk and accept license |
| `stop_command` | Command to stop Splunk |
| `cca_splunk_var_tmp` | Temp directory for CCA and Splunk files |
| `systemd_enterprise_name` | Name of systemd service for Splunk |

### group_vars/all/linux
| Variable | Description |
|----------|-------------|
| `splunk_user` | Defines the Splunk user |

### Configurable Variables
| Variable | Description |
|----------|-------------|
| `synchronize_module_use_ssh_args` | Set synchronize arguments |
| `download_from_remote_file_storage` | Enable remote file download instead of staging |

## Usage

### Include the Role

```yaml
- name: Ensure Splunk is installed
  ansible.builtin.include_role:
    name: deslicer.splunk.enterprise
```

### Include Specific Tasks

```yaml
- name: Initialize cluster upgrade
  ansible.builtin.include_role:
    name: deslicer.splunk.enterprise
    tasks_from: cluster/init_upgrade.yml
```

## Tasks

### Main Tasks (main.yml)
| Task | Description |
|------|-------------|
| `splunk_status.yml` | Checks status of Splunk and sets upgrade flag |
| `stage_install_files.yml` | Copy files from CCA manager to Splunk servers |
| `download_install_files.yml` | Download install files from remote storage |
| `ensure_splunk_version.yml` | Stop Splunk, extract tar, remove redundant files, start Splunk |
| `ensure_splunk_status_started.yml` | Start Splunk from command line |
| `ansible_managed.yml` | Mark host as managed by Ansible |

### Standalone Tasks
| Task | Description |
|------|-------------|
| `kvstore_upgrade_status.yml` | Check KVStore upgrade status during upgrades |
| `shcluster_upgrade_handler.yml` | Select shcluster upgrade task based on upgrade method |

### Cluster Tasks (cluster/)
| Task | Description |
|------|-------------|
| `init_upgrade.yml` | Start rolling upgrade of Splunk Index Cluster |
| `finalize_upgrade.yml` | Finalize rolling upgrade of Splunk Index Cluster |

### Search Head Cluster Tasks (shcluster/)
| Task | Description |
|------|-------------|
| `init_upgrade.yml` | Start rolling upgrade on Search Head Member |
| `shcluster_rolling_upgrade.yml` | Execute rolling upgrade of a search head member |
| `finalize_upgrade.yml` | Finalize rolling upgrade of Splunk Search Head Members |

## Files

| File | Description |
|------|-------------|
| `bin/splunk_upgrade_cleanup.sh` | Helper script to cleanup files from older versions |
| `dat/untracked_files_splunk_VERSION_Linux.diff` | Diff files per Linux version for cleanup |

## Dependencies

- deslicer.splunk.core

## License and Attribution

This role is derived from [cca_for_splunk](https://github.com/innovationfleet/cca_for_splunk),
originally developed by Innovation Fleet.

**Original License:** MIT License - Copyright (c) 2024 Innovation Fleet

This role has been adapted for use with the Deslicer Automation Platform by Deslicer AB.

**Copyright (c) 2024 Innovation Fleet**
**Modifications Copyright (c) 2025 Deslicer AB**
