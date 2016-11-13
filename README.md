# make_lambda_package

Bundle up Python deployment packages for AWS Lambda, including
source code, configs, and dependencies with extension modules.


# Installation

If you don't use `pipsi`, you're missing out.
Here are [installation instructions](https://github.com/mitsuhiko/pipsi#readme).

Simply run:

    $ pipsi install .


Packaging dependencies requires [the `docker` command](https://www.docker.com/)
to be in your `$PATH`.


# Usage

To use it:

    $ make-lambda-package --help
    Usage: make-lambda-package [OPTIONS] <path_or_url>

      Bundle up a deployment package for AWS Lambda.

      From your local filesystem:

          $ make-lambda-package .
          ...
          dist/lambda-package.zip

      Or from a remote git repository:

          $ make-lambda-package https://github.com/NoRedInk/make-lambda-package.git
          ...
          vendor/dist/NoRedInk-make-lambda-package.zip

      Use # fragment to specify a commit or a branch:

          $ make-lambda-package https://github.com/NoRedInk/make-lambda-package.git#v1.0.0

      Dependencies specified with --requirements-file will built using a docker
      container that replicates AWS Lambda's execution environment, so that
      extension modules are correctly packaged.

      When packaging a local source, --work-dir defaults to `.`:

      * ./build will hold a virtualenv for building dependencies if specified.
      * ./dist is where the zipped package will be saved

      When packaging a remote source, --work-dir defaults to `./vendor`.

    Options:
      --repo-source-files <glob_pattern_in_source>
                                      Source files to package.
      --requirements-file <path_in_source>
                                      Dependencies to package.
      --local-source-file <path_from_cwd> <path_in_zip>
                                      Files in the current working directory to
                                      package. Useful for config files.
      --work-dir <output_directory>   Where to store intermediary files and the
                                      zipped package.
      --help                          Show this message and exit.
