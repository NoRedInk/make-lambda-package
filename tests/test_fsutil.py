import os.path

from make_lambda_package import fsutil


def test_mkdir_p(tmpdir):
    with tmpdir.as_cwd():
        fsutil.mkdir_p('foo/bar')
        assert os.path.isdir('foo/bar')

        # make sure it doesn't error on second invocation
        fsutil.mkdir_p('foo/bar')
        assert os.path.isdir('foo/bar')


def test_rm_p(tmpdir):
    with tmpdir.as_cwd():
        assert not os.path.isfile('foo')

        fsutil.rm_p('foo')
        assert not os.path.isfile('foo')

        tmpdir.join('foo').write('')
        assert os.path.isfile('foo')

        fsutil.rm_p('foo')
        assert not os.path.isfile('foo')


def test_parse_path_or_url_commit_like():
    git_url = 'https://github.com/ento/ento.git'
    assert fsutil.parse_path_or_url(git_url).ref == 'master'
    assert fsutil.parse_path_or_url(git_url + '#').ref == 'master'
    assert fsutil.parse_path_or_url(git_url + '#f0a1b2').ref == 'f0a1b2'


def test_decide_paths_for_local_source(tmpdir):
    scm_source = fsutil.parse_path_or_url('.')
    with tmpdir.as_cwd():
        paths = fsutil.decide_paths(scm_source)
        assert paths.src_dir == tmpdir
        assert paths.build_dir == tmpdir.join('build')
        assert paths.dist_dir == tmpdir.join('dist')
        assert os.path.dirname(paths.zip_path) == tmpdir.join('dist')

        paths = fsutil.decide_paths(scm_source, work_dir='deploy')
        work_dir = tmpdir.join('deploy')
        assert paths.src_dir == tmpdir
        assert paths.build_dir == work_dir.join('build')
        assert paths.dist_dir == work_dir.join('dist')
        assert os.path.dirname(paths.zip_path) == work_dir.join('dist')


def test_decide_paths_for_github_url(tmpdir):
    git_url = 'https://github.com/ento/ento.git'
    scm_source = fsutil.parse_path_or_url(git_url)
    with tmpdir.as_cwd():
        paths = fsutil.decide_paths(scm_source)
        work_dir = tmpdir.join('vendor')
        assert paths.src_dir == work_dir.join('src', 'ento', 'ento')
        assert paths.build_dir == work_dir.join('build', 'ento', 'ento')
        assert paths.dist_dir == work_dir.join('dist')
        assert paths.zip_path == work_dir.join('dist', 'ento-ento.zip')

        paths = fsutil.decide_paths(scm_source, work_dir='deploy')
        work_dir = tmpdir.join('deploy')
        assert paths.src_dir == work_dir.join('src', 'ento', 'ento')
        assert paths.build_dir == work_dir.join('build', 'ento', 'ento')
        assert paths.dist_dir == work_dir.join('dist')
        assert paths.zip_path == work_dir.join('dist', 'ento-ento.zip')
