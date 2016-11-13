import subprocess

from make_lambda_package import scm


def test_fetch_and_refetch(tmpdir):
    origin = tmpdir.mkdir('origin')
    with origin.as_cwd():
        subprocess.check_call(['git', 'init'])
        subprocess.check_call(['git', 'config', 'user.email', 'make-lambda-package@example.com'])
        subprocess.check_call(['git', 'config', 'user.name', 'make-lambda-package'])

    first_sha = make_commit(origin, 'initial commit')
    second_sha = make_commit(origin, 'second commit')

    clone = tmpdir.join('clone')
    scm.fetch_repo(str(origin), first_sha, str(clone))

    # checks out the specified sha

    with clone.as_cwd():
        cloned_sha = get_current_head_sha()
        assert cloned_sha == first_sha

    # fetches the latest commits

    third_sha = make_commit(origin, 'third commit')
    scm.fetch_repo(str(origin), third_sha, str(clone))

    with clone.as_cwd():
        refetched_sha = get_current_head_sha()
        assert refetched_sha == third_sha

    # resets to the remote branch

    with origin.as_cwd():
        subprocess.check_call(['git', 'branch', 'v1.0.0', second_sha])

    with clone.as_cwd():
        subprocess.check_call(['git', 'branch', 'v1.0.0', third_sha])

    scm.fetch_repo(str(origin), 'v1.0.0', str(clone))

    with clone.as_cwd():
        refetched_sha = get_current_head_sha()
        assert refetched_sha == second_sha

    # handles new tag

    with origin.as_cwd():
        subprocess.check_call(['git', 'tag', 'v0.1.0', first_sha])

    scm.fetch_repo(str(origin), 'v0.1.0', str(clone))

    with clone.as_cwd():
        refetched_sha = get_current_head_sha()
        assert refetched_sha == first_sha


def make_commit(repo_dir, content):
    with repo_dir.as_cwd():
        repo_dir.join('readme.txt').write(content)
        subprocess.check_call(['git', 'add', 'readme.txt'])
        subprocess.check_call(['git', 'commit', '-m', content])
        return get_current_head_sha()


def get_current_head_sha():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
