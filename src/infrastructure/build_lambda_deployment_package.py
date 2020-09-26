import subprocess
import shlex


def __run_command(argstr: str) -> int:
    return subprocess.run(shlex.split(argstr.strip(), posix=False)).returncode


def main():
    __run_command('rm -rf .build')
    __run_command('mkdir .build')
    __run_command('cp -r src .build')
    __run_command('pipenv run pip freeze > .build/requirements.txt')
    __run_command('pip install -r .build/requirements.txt -t .build --compile')


if __name__ == '__main__':
    main()
