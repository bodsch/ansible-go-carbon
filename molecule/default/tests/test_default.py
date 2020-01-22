import pytest
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def get_vars(host):
    defaults_files = "file=../../defaults/main.yml name=role_defaults"
    vars_files = "file=../../vars/main.yml name=role_vars"

    ansible_vars = host.ansible(
        "include_vars",
        defaults_files)["ansible_facts"]["role_defaults"]

    ansible_vars.update(host.ansible(
        "include_vars",
        vars_files)["ansible_facts"]["role_vars"])

    print(ansible_vars)

    return ansible_vars


def test_whisper_directory(host, get_vars):
    dir = host.file(get_vars['go_carbon_whisper_data_directory'])
    assert dir.exists
    assert dir.is_directory


@pytest.mark.parametrize("dirs", [
    "/etc/go-carbon",
    "/var/log/go-carbon"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/etc/go-carbon/go-carbon.conf",
    "/etc/go-carbon/storage-aggregation.conf",
    "/etc/go-carbon/storage-schemas.conf",
    "/lib/systemd/system/go-carbon.service"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_user(host):
    assert host.group("carbon").exists
    assert host.user("carbon").exists
    assert "carbon" in host.user("carbon").groups
    assert host.user("carbon").shell == "/sbin/nologin"
    assert host.user("carbon").home == "/home/graphite"
