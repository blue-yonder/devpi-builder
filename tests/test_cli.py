# coding=utf-8

import xml.etree.ElementTree as ET

import pytest

from mock import patch
from devpi_plumber.server import TestServer
from devpi_plumber.client import DevpiClient, DevpiClientError

import devpi_builder
from devpi_builder.cli import main
from devpi_builder import wheeler


USER = 'user'
INDEX = 'user/wheels'
PURE_INDEX = 'user/packages'
PASSWORD = 'secret'

USERS = {
    USER: {'password': PASSWORD},
}
INDICES = {
    INDEX: {'bases': ''},
    PURE_INDEX: {'bases': ''},
}


@pytest.yield_fixture()
def devpi():
    with TestServer(USERS, INDICES) as _devpi:
        yield _devpi


def _package_version_exists(client, index, package, version):
    client.use(index)
    spec = "{}=={}".format(package, version)
    packages = client.list(spec)
    return wheeler.has_compatible_wheel(packages)


def test_basic(devpi):
    main(['tests/fixture/sample_simple.txt', devpi.url + '/' + INDEX,
          '--user={}'.format(USER), '--password={}'.format(PASSWORD)])
    assert _package_version_exists(devpi, INDEX, 'progressbar', '2.2')


def test_read_environment(devpi, monkeypatch):
    monkeypatch.setenv('DEVPI_USER', USER)
    monkeypatch.setenv('DEVPI_PASSWORD', PASSWORD)
    main(['tests/fixture/sample_simple.txt', devpi.url + '/' + INDEX])
    assert _package_version_exists(devpi, INDEX, 'progressbar', '2.2')


def test_prompt_user_pass(devpi, monkeypatch):
    monkeypatch.setattr('devpi_builder.cli.input', lambda x: USER, raising=False)
    monkeypatch.setattr('getpass.getpass', lambda x: PASSWORD)

    main(['tests/fixture/sample_simple.txt', devpi.url + '/' + INDEX])
    assert _package_version_exists(devpi, INDEX, 'progressbar', '2.2')


def test_batch_mode(devpi, monkeypatch):
    with patch('devpi_builder.cli.input') as mock_build:
        with pytest.raises(DevpiClientError):
            main(['tests/fixture/sample_simple.txt', devpi.url + '/' + INDEX, '--batch'])
        assert not mock_build.called


def test_with_blacklist(devpi):
    main(['tests/fixture/sample_simple.txt', devpi.url + '/' + INDEX,
          '--user={}'.format(USER),
          '--password={}'.format(PASSWORD),
          '--blacklist={}'.format('tests/fixture/sample_no_version.txt')])

    assert not _package_version_exists(devpi, INDEX, 'progressbar', '2.2')
    assert _package_version_exists(devpi, INDEX, 'six', '1.7.3')


def test_multiple_versions(devpi):
    main(['tests/fixture/sample_multiple_versions.txt', devpi.url + '/' + INDEX,
          '--user={}'.format(USER), '--password={}'.format(PASSWORD)])

    assert _package_version_exists(devpi, INDEX, 'progressbar', '2.1')
    assert _package_version_exists(devpi, INDEX, 'progressbar', '2.2')


def test_reupload_is_safe(devpi):
    main(['tests/fixture/sample_simple.txt', devpi.url + '/' + INDEX,
          '--user={}'.format(USER), '--password={}'.format(PASSWORD)])
    main(['tests/fixture/sample_multiple_versions.txt', devpi.url + '/' + INDEX,
          '--user={}'.format(USER), '--password={}'.format(PASSWORD)])

    assert _package_version_exists(devpi, INDEX, 'progressbar', '2.1')
    assert _package_version_exists(devpi, INDEX, 'progressbar', '2.2')
    assert _package_version_exists(devpi, INDEX, 'six', '1.7.3')


def test_continue_on_failed(devpi):
    main(['tests/fixture/sample_continue_on_failed.txt', devpi.url + '/' + INDEX,
          '--user={}'.format(USER), '--password={}'.format(PASSWORD)])
    assert _package_version_exists(devpi, INDEX, 'progressbar', '2.2')


def test_different_styles(devpi):
    main(['tests/fixture/sample_different_styles.txt', devpi.url + '/' + INDEX,
          '--user={}'.format(USER), '--password={}'.format(PASSWORD)])

    assert _package_version_exists(devpi, INDEX, 'pygments', '1.6')
    assert _package_version_exists(devpi, INDEX, 'Pygments', '1.6')
    assert _package_version_exists(devpi, INDEX, 'Django', '1.6.5')
    assert _package_version_exists(devpi, INDEX, 'django', '1.6.5')


def test_not_built_if_on_pure(devpi):
    """
    Verify that packages are not built and re-uploaded if they are already on the pure index.
    """
    with DevpiClient(devpi.server_url + '/' + PURE_INDEX,
                     USER,
                     PASSWORD) as pure_client:
        pure_client.upload('tests/fixture/pure_package/dist/test_package-0.1.dev1-py2.py3-none-any.whl')

        with patch.object(
                wheeler.Builder, 'build', autospec=True, side_effect=Exception('Should not build!')
        ) as mock_build:
            main(['tests/fixture/sample_test_package.txt', devpi.url + '/' + INDEX,
                  '--user={}'.format(USER),
                  '--password={}'.format(PASSWORD), '--pure-index={}'.format(pure_client.url)])
            assert not mock_build.called


def test_fills_proper_index(devpi):
    """
    Verify that pure packages are uploaded to the pure index non-pure packages are uploaded to the normal index.
    """
    main([
        'tests/fixture/sample_pure_and_non-pure.txt',
        devpi.url + '/' + INDEX,
        '--user={}'.format(USER),
        '--password={}'.format(PASSWORD),
        '--pure-index={}'.format(devpi.url + '/' + PURE_INDEX)
    ])

    assert _package_version_exists(devpi, PURE_INDEX, 'progressbar', '2.2')
    assert not _package_version_exists(devpi, PURE_INDEX, 'PyYAML', '3.10')

    assert not _package_version_exists(devpi, INDEX, 'progressbar', '2.2')
    assert _package_version_exists(devpi, INDEX, 'PyYAML', '3.10')


def _assert_test_case(root_element, result_tag_type, expected_element_name):
    xpath = './/testcase/{}/..'.format(result_tag_type)
    matched_nodes = root_element.findall(xpath)
    assert len(matched_nodes) == 1
    assert matched_nodes[0].attrib['name'] == expected_element_name


def _assert_junit_xml_content(junit_filename, run_id=None):
    run_id_str = ' ({})'.format(run_id) if run_id else ''

    root = ET.parse(junit_filename)
    ET.dump(root)

    _assert_test_case(root, 'failure', 'package-that-hopefully-not-exists 99.999' + run_id_str)
    _assert_test_case(root, 'skipped', 'test-package 0.1.dev1' + run_id_str)

    pb_elems = root.findall(".//testcase[@name='progressbar 2.2{}']".format(run_id_str))
    assert len(pb_elems) == 1
    pb_elem = pb_elems[0]
    assert pb_elem.find('failure') is None
    assert pb_elem.find('error') is None
    assert pb_elem.find('skipped') is None


def test_reports_junit_xml(devpi, tmpdir):
    with DevpiClient(devpi.server_url + '/' + INDEX,
                     USER,
                     PASSWORD) as client:
        client.upload('tests/fixture/pure_package/dist/test_package-0.1.dev1-py2.py3-none-any.whl')

    junit_filename = str(tmpdir.join('junit.xml'))
    main(['tests/fixture/sample_junit.txt', devpi.url + '/' + INDEX,
          '--user={}'.format(USER),
          '--password={}'.format(PASSWORD), '--junit-xml', junit_filename])

    _assert_junit_xml_content(junit_filename)


def test_run_id(devpi, tmpdir):
    RUN_ID = 'my_run_id'

    with DevpiClient(devpi.server_url + '/' + INDEX,
                     USER, PASSWORD) as client:
        client.upload('tests/fixture/pure_package/dist/test_package-0.1.dev1-py2.py3-none-any.whl')

    junit_filename = str(tmpdir.join('junit.xml'))
    main([
        'tests/fixture/sample_junit.txt',
        devpi.url + '/' + INDEX,
        '--user={}'.format(USER),
        '--password={}'.format(PASSWORD),
        '--junit-xml', junit_filename,
        '--run-id', RUN_ID
    ])

    _assert_junit_xml_content(junit_filename, RUN_ID)


def test_dry_run(devpi, tmpdir):
    """
    Test that a dry run produces the same ``junit.xml`` as a run without dry-run but does not modify the server
    state.
    """
    with DevpiClient(devpi.server_url + '/' + INDEX,
                     USER, PASSWORD) as client:
        client.upload('tests/fixture/pure_package/dist/test_package-0.1.dev1-py2.py3-none-any.whl')

    junit_filename = str(tmpdir.join('junit.xml'))
    main([
        'tests/fixture/sample_junit.txt',
        devpi.url + '/' + INDEX,
        '--user={}'.format(USER),
        '--password={}'.format(PASSWORD),
        '--junit-xml', junit_filename,
        '--dry-run',
    ])

    _assert_junit_xml_content(junit_filename)

    assert not _package_version_exists(devpi, INDEX, 'progressbar', '2.2')


def test_passes_client_cert():
    """
    Verify that packages are not built and re-uploaded if they are already on the pure index.
    """
    PURE_INDEX='pure_index'
    with patch('devpi_builder.cli.DevpiClient') as client:
        main(['tests/fixture/sample_test_package.txt', INDEX,
              '--user={}'.format(USER),
              '--password={}'.format(PASSWORD),
              '--pure-index={}'.format(PURE_INDEX),
              '--client-cert=some.crt'])

        client.assert_any_call(INDEX, USER, PASSWORD, client_cert='some.crt')
        client.assert_any_call(PURE_INDEX, USER, PASSWORD, client_cert='some.crt')
        assert len(client.call_args_list) == 2  # Check that no further instances have been created
