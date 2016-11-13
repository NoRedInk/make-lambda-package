from zipfile import ZipFile
import py.path

from make_lambda_package import archive
from make_lambda_package import fsutil


def test_repo_and_local_source_files(tmpdir):
    with tmpdir.as_cwd():
        scm_source = fsutil.parse_path_or_url('https://gist.github.com/hello.git')
        paths = fsutil.decide_paths(scm_source)
        fsutil.ensure_dirs(paths)
        fsutil.mkdir_p(paths.src_dir)

        with py.path.local(paths.src_dir).as_cwd():
            py.path.local().join('hello.txt').write('repo')

        # this should not be added to the archive
        py.path.local().join('hello.txt').write('local')

        archive.make_archive(paths, repo_source_files='hello.txt')

        with ZipFile(paths.zip_path) as zipfile:
            with zipfile.open('hello.txt') as f:
                assert f.read().decode('utf-8') == 'repo'

        archive.make_archive(paths, local_source_files=[('hello.txt', 'dest.txt')])

        with ZipFile(paths.zip_path) as zipfile:
            with zipfile.open('dest.txt') as f:
                assert f.read().decode('utf-8') == 'local'


def test_deps_file(tmpdir):
    with tmpdir.as_cwd():
        scm_source = fsutil.parse_path_or_url('https://gist.github.com/hello.git')
        paths = fsutil.decide_paths(scm_source)
        fsutil.ensure_dirs(paths)

        site_packages_path = py.path.local(paths.build_dir).join(
            'env', 'lib', 'python2.7', 'site-packages')

        fsutil.mkdir_p(str(site_packages_path))

        site_packages_path.mkdir('mypackage').join('hello.txt').write('hello')

        deps_file = py.path.local('deps.txt')
        deps_file.write('\n'.join(['mypackage/hello.txt', '../ghost']))

        archive.make_archive(paths, deps_file=str(deps_file))

        with ZipFile(paths.zip_path) as zipfile:
            assert len(zipfile.namelist()) == 1
            with zipfile.open('mypackage/hello.txt') as f:
                assert f.read().decode('utf-8') == 'hello'
