#!/usr/bin/env python
import os
import sys
import subprocess
import textwrap


def main(argv=[]):
    source = 'README.in'
    dest = 'README.md'

    if len(argv) > 2:
        source = argv[1]
        dest = argv[2]

    command = 'make-lambda-package --help'
    help_text = subprocess.check_output(command, shell=True).decode('utf-8')
    indent = ' ' * 4
    indented = '\n'.join(
        indent + line if line else line
        for line in help_text.splitlines())

    with open(source) as f:
        template = f.read()

    with open(dest, 'w') as f:
        f.write(template.format(indented_help_text=indented))


if __name__ == '__main__':
    main(sys.argv)
