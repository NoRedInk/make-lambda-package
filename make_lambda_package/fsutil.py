import os
import errno
import contextlib
from collections import namedtuple
from six.moves import urllib


Paths = namedtuple('Paths', 'src_dir build_dir dist_dir zip_path')
LocalSource = namedtuple('LocalSource', 'path')
RemoteSource = namedtuple('RemoteSource', 'url ref repo_dir')  # assumes git


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def rm_p(path):
    try:
        os.unlink(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.ENOENT:
            pass
        else:
            raise


@contextlib.contextmanager
def chdir(path):
    curdir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(curdir)


def parse_path_or_url(path_or_url):  # -> Union[LocalSource, RemoteSource]
    parse_result = urllib.parse.urlparse(path_or_url)
    if parse_result.scheme in ('', 'file'):
        return LocalSource(path_or_url)
    else:
        ref = parse_result.fragment or 'master'
        repo_dir = os.path.splitext(parse_result.path[1:])[0]
        return RemoteSource(path_or_url, ref, repo_dir)


def decide_paths(scm_source, work_dir=None):
    cwd = os.getcwd()
    if isinstance(scm_source, LocalSource):
        work_dir = os.path.abspath(work_dir or cwd)
        src_dir = os.path.abspath(scm_source.path)

        dist_dir = os.path.join(work_dir, 'dist')
        return Paths(
            src_dir=src_dir,
            build_dir=os.path.join(work_dir, 'build'),
            dist_dir=dist_dir,
            zip_path=os.path.join(dist_dir, 'lambda-package.zip'))
    else:
        work_dir = os.path.abspath(os.path.join(cwd, work_dir or 'vendor'))

        dist_dir = os.path.join(work_dir, 'dist')
        zip_path = os.path.join(
            dist_dir, scm_source.repo_dir.replace('/', '-') + '.zip')
        return Paths(
            src_dir=os.path.join(work_dir, 'src', scm_source.repo_dir),
            build_dir=os.path.join(work_dir, 'build', scm_source.repo_dir),
            dist_dir=dist_dir,
            zip_path=zip_path)


def ensure_dirs(paths):
    mkdir_p(paths.build_dir)
    mkdir_p(paths.dist_dir)
