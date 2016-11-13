import os.path
import glob
from zipfile import ZipFile, ZIP_DEFLATED

from make_lambda_package import fsutil


def make_archive(
        paths,
        repo_source_files=None,
        local_source_files=None,
        deps_file=None):
    fsutil.rm_p(paths.zip_path)
    with ZipFile(paths.zip_path, 'w', ZIP_DEFLATED) as f:
        if repo_source_files:
            _add_repo_files(f, paths, repo_source_files)
        if local_source_files:
            _add_local_files(f, local_source_files)
        if deps_file:
            _add_deps(f, paths, deps_file)


def _add_local_files(zipfile, local_source_files):
    for (source, dest) in local_source_files:
        zipfile.write(source, dest)


def _add_repo_files(zipfile, paths, repo_source_files):
    with fsutil.chdir(paths.src_dir):
        for path in glob.glob(repo_source_files):
            zipfile.write(path)


def _add_deps(zipfile, paths, deps_file):
    site_packages_path = os.path.join(
        paths.build_dir, 'env', 'lib', 'python2.7', 'site-packages')
    with fsutil.chdir(site_packages_path), open(deps_file) as f:
        for line in f:
            if line.startswith(os.pardir):
                continue
            zipfile.write(line.strip())
