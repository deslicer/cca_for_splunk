# deslicer.splunk.linux

This role prepares Linux servers with the settings required to run Splunk as a service as a non-privileged user.

## Overview

The role handles:
- User and group configuration for Splunk
- Systemd service configuration with cgroup support
- Firewall configuration (firewalld)
- System limits (ulimits)
- Polkit rules for service management
- THP (Transparent Huge Pages) disabling
- SELinux configuration
- NTP configuration with Chrony
- OS patching and updates

### Customization

Options exist to control which tasks should be executed and to add multiple custom roles to configure the server as needed.

## Requirements

### Supported Operating Systems
- RHEL 8, 9
- CentOS Stream 8, 9
- Amazon Linux 2023
- Ubuntu 22.04, 24.04
- Debian 11, 12

### Prerequisites
- Mount point for `splunk_path` on all Splunk servers (separate filesystem recommended)
- On Cluster Index peers: additional mount points for `splunk_volume_path_hot` and `splunk_volume_path_cold`
- Initial account with SUDO ALL access for setup

## Role Variables

### group_vars/all/linux
| Variable | Description |
|----------|-------------|
| `external_bootstrap_pre_roles` | Custom roles to inject early in bootstrap |
| `external_bootstrap_roles` | Custom roles to inject in middle of bootstrap |
| `external_bootstrap_post_roles` | Custom roles to inject late in bootstrap |
| `cca_splunk_manager_user` | Manager user for Splunk servers |
| `cca_splunk_manager_user_uid` | Manager user UID |
| `cca_splunk_manager_user_dir` | Manager user home directory |
| `cca_splunk_manager_group_name` | Manager user group name |
| `cca_splunk_manager_gid` | Manager user GID |
| `splunk_user` | Name of Splunk user (normally `splunk`) |
| `splunk_user_uid` | Splunk user UID |
| `splunk_user_dir` | Splunk user home (same as `splunk_path`) |
| `splunk_user_group_name` | Splunk user group name |
| `splunk_user_gid` | Splunk user GID |
| `cca_baseline_software` | Baseline software needed by CCA (rsync, git, etc.) |

### Control Variables
The `control.linux_configuration` dictionary controls which tasks are executed:

| Variable | Default | Description |
|----------|---------|-------------|
| `splunk_user` | `true` | Configure Splunk user |
| `configure_firewall` | `false` | Configure firewalld |
| `disable_firewall` | `false` | Disable firewalld |
| `server_hardening` | `true` | Configure base hardening |
| `baseline_software` | `true` | Install baseline software |
| `splunk_limits` | `true` | Configure ulimits |
| `splunk_version` | `true` | Get Splunk version |
| `splunk_service` | `true` | Configure systemd service |
| `splunk_polkit` | `true` | Configure polkit rules |
| `thp` | `true` | Disable THP |
| `selinux` | `true` | Configure SELinux |
| `sudoers` | `true` | Configure sudoers |
| `configure_ntp` | `false` | Configure NTP with Chrony |

## Usage

### Include the Role

```yaml
- name: Configure Linux server for Splunk
  ansible.builtin.include_role:
    name: deslicer.splunk.linux
```

### Include Specific Tasks

```yaml
- name: Reboot server if needed
  ansible.builtin.include_role:
    name: deslicer.splunk.linux
    tasks_from: server_reboot_handler.yml
```

## Tasks

### Main Tasks (main.yml)
| Task | Description |
|------|-------------|
| `get_facts.yml` | Gather host facts and set variables |
| `validate_supported_os_versions.yml` | Validate OS against supported versions |
| `include_external_pre_roles.yml` | Execute external roles at beginning |
| `configure_splunk_user.yml` | Configure Splunk user |
| `include_external_roles.yml` | Execute external roles in middle |
| `dot_bootstrap.yml` | Mark server as bootstrapped |
| `configure_firewall.yml` | Configure internal firewall |
| `configure_server_hardening.yml` | Base server hardening |
| `configure_splunk_limits.yml` | Set ulimits for Splunk user |
| `configure_splunk_service.yml` | Configure systemd service |
| `configure_polkit.yml` | Install and configure polkit |
| `configure_thp.yml` | Disable Transparent Huge Pages |
| `configure_selinux.yml` | Configure SELinux state |
| `configure_sudoers.yml` | Configure sudo rights |
| `include_external_post_roles.yml` | Execute external roles at end |
| `configure_fs_rights.yml` | Ensure owner on Splunk directories |
| `configure_ntp.yml` | Configure NTP with Chrony |

### Standalone Tasks
| Task | Description |
|------|-------------|
| `check_pending_actions.yml` | Check for pending reboot or service restart |
| `server_reboot_handler.yml` | Reboot server and wait for return |
| `set_reboot_flag.yml` | Set flag to trigger reboot |
| `standalone_reboot.yml` | Reboot server and cleanup state file |
| `validate_available_disk_space.yml` | Validate disk space for operations |

### Firewalld Tasks (firewalld/)
| Task | Description |
|------|-------------|
| `ensure_firewalld.yml` | Install/upgrade firewalld |
| `configure_firewalld.yml` | Configure firewalld for Splunk |
| `disable_firewalld.yml` | Disable firewalld service |

### Systemd Tasks (systemd/)
| Task | Description |
|------|-------------|
| `main.yml` | Main systemd configuration entry |
| `manage_cgroup_version.yml` | Manage cgroup version for Splunk compatibility |
| `manage_cgroup_v1.yml` | Configure cgroup v1 for older Splunk versions |
| `manage_cgroup_v2.yml` | Configure cgroup v2 for Splunk 9.4+ |
| `splunkd_service.yml` | Template Splunkd.service file |
| `thp_service.yml` | Configure systemd service to disable THP |

### Polkit Tasks (polkit/)
| Task | Description |
|------|-------------|
| `apt/ensure_polkit.yml` | Install polkit on Debian-based systems |
| `dnf/ensure_polkit.yml` | Install polkit with dnf |
| `yum/ensure_polkit.yml` | Install polkit with yum |
| `polkit_rules.yml` | Configure polkit rules for RPM-based systems |
| `policykit-1_rules.yml` | Configure polkit rules for Debian-based systems |

### NTP Tasks (ntp/)
| Task | Description |
|------|-------------|
| `apt/install_chrony.yml` | Install Chrony on Debian-based systems |
| `dnf/install_chrony.yml` | Install Chrony with dnf |
| `yum/install_chrony.yml` | Install Chrony with yum |
| `ensure_chrony.yml` | Enable and start Chrony service |
| `configure_chrony.yml` | Configure Chrony settings |

### Package Tasks (package/)
| Task | Description |
|------|-------------|
| `apt/configure_baseline_software.yml` | Install baseline software with apt |
| `dnf/configure_baseline_software.yml` | Install baseline software with dnf |
| `yum/configure_baseline_software.yml` | Install baseline software with yum |

### Update Tasks (update/)
| Task | Description |
|------|-------------|
| `apt/check_for_os_updates.yml` | Check for OS updates with apt |
| `apt/os_update.yml` | Apply OS updates with apt |
| `dnf/check_for_os_updates.yml` | Check for OS updates with dnf |
| `dnf/os_update.yml` | Apply OS updates with dnf |
| `yum/check_for_os_updates.yml` | Check for OS updates with yum |
| `yum/os_update.yml` | Apply OS updates with yum |

## Vars

OS-dependent variables that can be overridden:

| File | Description |
|------|-------------|
| `default.yml` | Default variables |
| `Amazon-2.yml` | Specific variables for Amazon Linux 2 |

## Dependencies

None

## License and Attribution

This role is derived from [cca_for_splunk](https://github.com/innovationfleet/cca_for_splunk),
originally developed by Innovation Fleet.

**Original License:** MIT License - Copyright (c) 2024 Innovation Fleet

This role has been adapted for use with the Deslicer Automation Platform by Deslicer AB.

**Copyright (c) 2024 Innovation Fleet**
**Modifications Copyright (c) 2025 Deslicer AB**
