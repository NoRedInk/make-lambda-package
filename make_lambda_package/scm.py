import os.path
import subprocess

from make_lambda_package import fsutil


def fetch_repo(git_url, git_ref, to_dir):
    if os.path.isdir(to_dir):
        with fsutil.chdir(to_dir):
            subprocess.check_call(['git', 'fetch'])
    else:
        fsutil.mkdir_p(to_dir)
        subprocess.check_call(['git', 'clone', git_url, to_dir])

    with fsutil.chdir(to_dir):
        subprocess.check_call(['git', 'checkout', git_ref])

        maybe_remote_branch = 'origin/{}'.format(git_ref)
        show_ref_retcode = subprocess.call(
            ['git', 'show-ref', maybe_remote_branch])
        if show_ref_retcode == 0:
            subprocess.check_call(['git', 'reset', '--hard', maybe_remote_branch])
