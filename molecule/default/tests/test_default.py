import os
import re
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('file, content', [
    ("/etc/hosts", "127.0.1.1 www.example.com www"),
    ("/etc/hostname", "www.example.com")
])
def test_files(host, file, content):
    file = host.file(file)

    assert file.exists
    assert file.contains(content)


def test_hostname_command(host):
    cmd = host.check_output("/usr/bin/hostname -f")

    assert re.match("^www.example.com$", cmd)
