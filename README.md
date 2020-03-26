# ansible role for go-carbon

Ansible Role for [go-carbon](https://github.com/lomik/go-carbon).
> Golang implementation of Graphite/Carbon server with classic architecture: Agent -> Cache -> Persister

## configure

define your own *storage schemas*:

```
go_carbon_storage_schema:
  test:
    pattern: '^test\.'
    retentions: '5m:30d'
```

define your own *storage aggregation*:
```
go_carbon_storage_aggregation
  count:
    pattern: '\.count$'
    xFilesFactor: 0
    aggregationMethod: sum
```

or you use the defaults under `vars/main.yml`

## clean up older whisper data

I use a small (with my modifications) Script from [unixe.de](https://www.unixe.de/whisper-daten-aufraeumen/).

(There you will find more useful tips around the topic of monitoring.

**This page is highly recommended, which is what I am doing with it.**)

You should make sure that a cron-daemon is installed.
For *RedHat* based systems `cronie` can be used.
For *Debian* based systems `cron` is available.

You can set the cron-daemon over `go_carbon_used_cron_daemon`.

**Support for systemd is currently not planned.**

To active this feature set `go_carbon_clean_data_enabled` to `True`


## example configuration

```
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


```
- hosts: monitoring
  gather_facts: true
  become: true
  environment:
    NETRC: ''
  roles:
    - role: go-carbon
```
