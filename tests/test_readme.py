import os.path
import update_readme


def test_readme_help_is_up_to_date(tmpdir):
    repo_root = os.path.join(os.path.dirname(__file__), os.pardir)
    current_readme_path = os.path.join(repo_root, 'README.md')
    with open(current_readme_path) as f:
        old_readme = f.read()

    source_path = os.path.join(repo_root, 'README.in')
    dest_path = tmpdir.join('README.md')
    update_readme.main([None, source_path, str(dest_path)])

    with open(str(dest_path)) as f:
        new_readme = f.read()

    assert new_readme == old_readme
