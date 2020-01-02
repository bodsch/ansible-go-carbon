import pytest
import os
import yaml
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def AnsibleDefaults():
    with open("../../defaults/main.yml", 'r') as stream:
        return yaml.load(stream)


@pytest.mark.parametrize("dirs", [
    "/srv/graphite/whisper",
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
