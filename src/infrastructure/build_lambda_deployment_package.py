import subprocess
import shlex
import sys
from typing import List


def __run_command(argstr: str) -> int:
    return subprocess.run(shlex.split(argstr.strip(), posix=False)).returncode


def main():
    extra_indexes: List[str] = sys.argv[1:]
    print('Extra indexes:\n', '\n'.join(extra_indexes))
    __run_command('rm -rf .build')
    __run_command('mkdir .build')
    __run_command('cp -r src .build')
    requirements = str(subprocess.check_output('pipenv run pip freeze'.split()), 'utf-8')
    print('requirements:')
    print(requirements)
    with open('.build/requirements.txt', 'w+') as requirements_file:
        requirements_file.writelines(requirements)
    install_command = 'pip install -r .build/requirements.txt -t .build --compile'
    for extra_index in extra_indexes:
        install_command += ' --extra-index-url %s' % extra_index
    __run_command(install_command)


if __name__ == '__main__':
    main()
