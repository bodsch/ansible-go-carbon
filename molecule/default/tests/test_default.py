
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
import pytest
import os
import testinfra.utils.ansible_runner

import pprint
pp = pprint.PrettyPrinter()

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def base_directory():
    cwd = os.getcwd()
    pp.pprint(cwd)
    pp.pprint(os.listdir(cwd))

    if('group_vars' in os.listdir(cwd)):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = "molecule/{}".format(os.environ.get('MOLECULE_SCENARIO_NAME'))

    return directory, molecule_directory


@pytest.fixture()
def get_vars(host):
    """

    """
    base_dir, molecule_dir = base_directory()

    pp.pprint(" => '{}' / '{}'".format(base_dir, molecule_dir))

    file_defaults = "file={}/defaults/main.yml name=role_defaults".format(base_dir)
    file_vars = "file={}/vars/main.yml name=role_vars".format(base_dir)
    file_molecule = "file={}/group_vars/all/vars.yml name=test_vars".format(molecule_dir)

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result

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


def test_carbon_config(host, get_vars):
    config_file = "/etc/go-carbon/go-carbon.conf"
    content = host.file(config_file).content_string
    assert 'data-dir = "{}"'.format(get_vars.get('go_carbon_whisper_data_directory')) in content


def test_storage_schemas(host):

    config_file = "/etc/go-carbon/storage-schemas.conf"
    content = host.file(config_file).content_string

    assert '[test]' in content
    assert 'retentions = 5m:30d' in content


def test_user(host):
    assert host.group("carbon").exists
    assert host.user("carbon").exists
    assert "carbon" in host.user("carbon").groups
    assert host.user("carbon").shell == "/sbin/nologin"
    assert host.user("carbon").home == "/home/graphite"


def test_solr_service(host):
    service = host.service("go-carbon")

    # if( service.__class__.__name__ != 'SysvService' ):
    assert service.is_enabled
    assert service.is_running


@pytest.mark.parametrize("ports", [
    '0.0.0.0:8081',
    '0.0.0.0:2003',
    '0.0.0.0:7002',
    '0.0.0.0:7003'
])
def test_open_port(host, ports):
    for i in host.socket.get_listening_sockets():
        print(i)

    solr = host.socket("tcp://{}".format(ports))
    assert solr.is_listening
