# Deslicer Splunk Collection

Ansible collection for Splunk Enterprise deployment and management.

## Description

This collection provides roles for:
- **core**: Splunk configuration, user management, cluster operations
- **enterprise**: Splunk Enterprise installation and upgrades
- **linux**: Linux server preparation for Splunk

## Requirements

- Ansible >= 2.18
- Python >= 3.11

## Installation

```bash
ansible-galaxy collection install deslicer.splunk
```

Or from a tarball:

```bash
ansible-galaxy collection install deslicer-splunk-1.0.0.tar.gz
```

## Usage

### Using Roles

```yaml
- hosts: splunk_servers
  collections:
    - deslicer.splunk
  roles:
    - core
    - enterprise
    - linux
```

Or with fully qualified names:

```yaml
- hosts: splunk_servers
  roles:
    - deslicer.splunk.core
    - deslicer.splunk.enterprise
    - deslicer.splunk.linux
```

### Including Tasks

```yaml
- name: Login to Splunk
  ansible.builtin.include_role:
    name: deslicer.splunk.core
    tasks_from: splunk_login.yml
```

## Roles

### deslicer.splunk.core

Core Splunk operations including:
- User management
- Cluster bundle management
- Search head cluster operations
- Splunk service control

### deslicer.splunk.enterprise

Splunk Enterprise installation and upgrades:
- Initial installation
- Rolling upgrades
- Version management

### deslicer.splunk.linux

Linux server preparation:
- User/group setup
- Systemd service configuration
- Firewall configuration
- THP disabling
- Polkit rules

## License and Attribution

This collection is derived from [cca_for_splunk](https://github.com/innovationfleet/cca_for_splunk),
originally developed by Innovation Fleet.

**Original License:** MIT License - Copyright (c) 2024 Innovation Fleet

This collection has been adapted for use with the Deslicer Automation Platform by Deslicer AB.

**Copyright (c) 2024 Innovation Fleet**
**Modifications Copyright (c) 2026 Deslicer AB**

Licensed under the MIT License. See [LICENSE](LICENSE) for details.
