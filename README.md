
# Ansible Role:  `go-carbon`

Ansible role to install and configure [go-carbon](https://github.com/go-graphite/go-carbon).

> Golang implementation of Graphite/Carbon server with classic architecture: Agent -> Cache -> Persister



[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-go-carbon/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-go-carbon)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-go-carbon)][releases]

[ci]: https://github.com/bodsch/ansible-go-carbon/actions
[issues]: https://github.com/bodsch/ansible-go-carbon/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-go-carbon/releases


## configure

define your own *storage schemas*:

```yaml
go_carbon_storage_schema:
  test:
    pattern: '^test\.'
    retentions: '5m:30d'
```

define your own *storage aggregation*:

```yaml
go_carbon_storage_aggregation:
  count:
    pattern: '\.count$'
    xFilesFactor: 0
    aggregationMethod: sum
```

You can use also the defaults under [`vars/main.yml`](vars/main.yml)


## clean up older whisper data

I use a small (with my modifications) Script from [Marianne Spiller](https://github.com/sysadmama) / [unixe.de](https://www.unixe.de/whisper-daten-aufraeumen/)

(There you will find more useful tips around the topic of monitoring.

**This page is highly recommended, which is what I am doing with it.**)

- You should make sure that a cron-daemon is installed.
- For *RedHat* based systems `cronie` can be used.
- For *Debian* based systems `cron` is available.

You can set the cron-daemon over `go_carbon_used_cron_daemon`.

**Support for systemd is currently not planned.**

To active this feature set `go_carbon_clean_data_enabled` to `true`


## example configuration

```yaml
go_carbon_whisper_data_directory: /opt/graphite/whisper

go_carbon_storage_schema:
  telegraf:
    # 1 Host and 1 Metric produce: 105.51 Kilobytes
    pattern: '^telegraf\.'
    retentions: '10s:2d,1m:6h,5m:30d'
  grafana:
    # 1 Host and 1 Metric produce: 556.94 Kilobytes
    pattern: '^grafana\.'
    retentions: '1m:15d,5m:30d,15m:120d,1h:240d'
  icinga2:
    # 1 Host and 1 Metric produce: 556.94 Kilobytes
    pattern: '^icinga2\.'
    retentions: '1m:15d,5m:30d,15m:120d,1h:240d'
```

## example playbook

```yaml
- hosts: monitoring
  gather_facts: true
  become: true
  environment:
    NETRC: ''

  roles:
    - role: go-carbon
```

## tests

You can use a set of test:

### default

```bash
tox -e py39-ansible29 -- molecule test -s default
```

### letest version from github

```bash
tox -e py39-ansible29 -- molecule test -s latest
```

### latest version with automatic clean of older whisper data

```bash
tox -e py39-ansible29 -- molecule test -s latest-with-clean-data
```

### named version

```bash
tox -e py39-ansible29 -- molecule test -s version-0.14
```
