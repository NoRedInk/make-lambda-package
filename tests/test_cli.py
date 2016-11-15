import pytest
import os
import subprocess
from zipfile import ZipFile
from click.testing import CliRunner
from make_lambda_package import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_with_no_source_options(tmpdir, runner):
    cwd = os.getcwd()
    work_dir = tmpdir.join('deploy_package')
    args = [
        cwd,
        '--work-dir', str(work_dir),
    ]

    with tmpdir.as_cwd():
        result = runner.invoke(cli.main, args)
        assert not result.exception, result.output
        assert result.exit_code == 0, result.output

        zip_path = work_dir.join('dist', 'lambda-package.zip')
        assert zip_path.isfile(), result.output

        with ZipFile(str(zip_path)) as zipfile:
            namelist = zipfile.namelist()
            assert len(list(namelist)) == 0

        assert 'Warning' in result.output


def test_with_all_source_options(tmpdir, runner):
    cwd = os.getcwd()
    work_dir = tmpdir.join('deploy_package')
    args = [
        cwd,
        '--repo-source-files', 'make_lambda_package/*.py',
        '--requirements-file', 'requirements.txt',
        '--local-source-file', 'hello.txt', 'world.txt',
        '--work-dir', str(work_dir),
    ]

    with tmpdir.as_cwd():
        tmpdir.join('hello.txt').write('secret')
        result = runner.invoke(cli.main, args)
        assert not result.exception, result.output
        assert result.exit_code == 0, result.output

        zip_path = work_dir.join('dist', 'lambda-package.zip')
        assert zip_path.isfile(), result.output

        with ZipFile(str(zip_path)) as zipfile:
            namelist = zipfile.namelist()
            assert len(list(filter(lambda name: 'click' in name, namelist))) > 0
            assert 'world.txt' in namelist
            assert 'make_lambda_package/cli.py' in namelist


def test_fail_if_no_docker_command(tmpdir, mocker, runner):
    with tmpdir.as_cwd():
        mocked_call = mocker.patch.object(subprocess, 'call', return_value=1)
        args = ['.', '--requirements-file', 'requirements.txt']
        result = runner.invoke(cli.main, args)
        assert result.exception, result.output
        assert result.exit_code == 2, result.output

        assert mocked_call.call_count == 1
        assert mocked_call.call_args[0][0][0] == 'docker'
