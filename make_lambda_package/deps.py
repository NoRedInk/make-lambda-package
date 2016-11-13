import os.path
import subprocess
import pip


DOCKER_BUILD_SCRIPT = '''
set -x

cd "{docker_build_dir}"

if [ ! -d env ]; then
    virtualenv env
fi
source env/bin/activate
pip install pip-tools

cd "{docker_src_dir}"

pip-sync {requirements_file}

rm -f "{docker_build_dir}/{deps_file}"
packages=({package_names})
for package in ${{packages[@]}}; do
    if pip show $package | grep 'Location: {docker_build_dir}'; then
        pip show -f $package | sed -e '1,/^Files:/d' >> "{docker_build_dir}/{deps_file}"
    fi
done
'''


def build_deps(paths, requirements_file):
    requirements = pip.req.parse_requirements(
        os.path.join(paths.src_dir, requirements_file), session=True)
    package_names = [req.name for req in requirements]
    deps_file = 'deps.txt'

    context = dict(
        docker_build_dir='/var/task/build/',
        docker_src_dir='/var/task/src/',
        build_dir=paths.build_dir,
        src_dir=paths.src_dir,
        requirements_file=requirements_file,
        package_names=' '.join(package_names),
        deps_file=deps_file
    )
    build_script = DOCKER_BUILD_SCRIPT.format(**context)

    command = [
        'docker', 'run',
        '-v', '{build_dir}:{docker_build_dir}'.format(**context),
        '-v', '{src_dir}:{docker_src_dir}'.format(**context),
        'lambci/lambda:build-python2.7',
        'bash', '-c', build_script,
    ]
    subprocess.check_call(command)

    return os.path.join(paths.build_dir, deps_file)
