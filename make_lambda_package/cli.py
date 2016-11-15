import os
import subprocess
import click

from make_lambda_package import archive
from make_lambda_package import deps
from make_lambda_package import fsutil
from make_lambda_package import scm


@click.command('make-lambda-package')
@click.argument('source',
                metavar='<path_or_url>')
@click.option('--repo-source-files',
              metavar='<glob_pattern_in_source>',
              help='Source files to package.')
@click.option('--requirements-file',
              metavar='<path_in_source>',
              help='Dependencies to package.')
@click.option('--local-source-file',
              metavar='<path_from_cwd> <path_in_zip>',
              multiple=True,
              type=(click.Path(exists=True, dir_okay=False), str),
              help='Files in the current working directory to package. Useful for config files.')
@click.option('--work-dir',
              metavar='<output_directory>',
              type=click.Path(exists=False, file_okay=False, writable=True),
              help='Where to store intermediary files and the zipped package. ')
def main(
        source,
        repo_source_files,
        requirements_file,
        local_source_file,
        work_dir):
    """
    Bundle up a deployment package for AWS Lambda.

    From your local filesystem:

    \b
        $ make-lambda-package .
        ...
        dist/lambda-package.zip

    Or from a remote git repository:

    \b
        $ make-lambda-package https://github.com/NoRedInk/make-lambda-package.git
        ...
        vendor/dist/NoRedInk-make-lambda-package.zip

    Use # fragment to specify a commit or a branch:

    \b
        $ make-lambda-package https://github.com/NoRedInk/make-lambda-package.git#v1.0.0

    Dependencies specified with --requirements-file will built using a docker container
    that replicates AWS Lambda's execution environment, so that extension modules
    are correctly packaged.

    When packaging a local source, --work-dir defaults to `.`:

    \b
    * ./build will hold a virtualenv for building dependencies if specified.
    * ./dist is where the zipped package will be saved

    When packaging a remote source, --work-dir defaults to `./vendor`.
    """
    scm_source = fsutil.parse_path_or_url(source)
    paths = fsutil.decide_paths(scm_source, work_dir)

    if requirements_file:
        with open(os.devnull, 'w') as devnull:
            docker_retcode = subprocess.call(['docker', '--help'], stdout=devnull)
        if docker_retcode != 0:
            raise click.UsageError(
                "`docker` command doesn't seem to be available. "
                "It's required to package dependencies.")

    if not (requirements_file or repo_source_files or local_source_file):
        click.secho(
            'Warning: without --repo-source-files, --requirements-file, '
            'or --local-source-file, nothing will be included in the zip file. '
            'Assuming you have good reasons to do this and proceeding.',
            fg='yellow')

    fsutil.ensure_dirs(paths)

    if isinstance(scm_source, fsutil.RemoteSource):
        click.echo('Fetching repo..')
        scm.fetch_repo(scm_source.url, scm_source.ref, paths.src_dir)

    deps_file = None
    if requirements_file:
        click.echo('Building deps..')
        deps_file = deps.build_deps(paths, requirements_file)

    click.echo('Creating zip file..')
    archive.make_archive(
        paths,
        repo_source_files,
        local_source_file,
        deps_file)

    click.echo(os.path.relpath(paths.zip_path, os.getcwd()))


if __name__ == '__main__':
    main()
