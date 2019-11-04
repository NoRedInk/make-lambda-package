"""
Bundle up deployment packages for AWS Lambda.
"""
from setuptools import find_packages, setup

setup(
    name='make-lambda-package',
    version='1.1.0',
    url='https://github.com/NoRedInk/make-lambda-package',
    license='BSD-3-Clause',
    author='Marica Odagaki',
    author_email='marica@noredink.com',
    description='Bundle up deployment packages for AWS Lambda.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'click',
        'pip',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'make-lambda-package = make_lambda_package.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Software Distribution',
    ]
)
