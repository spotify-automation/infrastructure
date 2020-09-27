import subprocess
import shlex


def __run_command(argstr: str) -> int:
    return subprocess.run(shlex.split(argstr.strip(), posix=False)).returncode


def main():
    __run_command('rm -rf .build')
    __run_command('mkdir .build')
    __run_command('cp -r src .build')
    requirements = str(subprocess.check_output('pipenv run pip freeze'.split()), 'utf-8')
    print('requirements:')
    print(requirements)
    with open('.build/requirements.txt', 'w+') as requirements_file:
        requirements_file.writelines(requirements.splitlines())
    __run_command('pip install -r .build/requirements.txt -t .build --compile')


if __name__ == '__main__':
    main()
