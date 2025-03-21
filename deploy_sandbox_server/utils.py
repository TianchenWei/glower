import os
import subprocess
from contextlib import contextmanager


def get_repo_root():
    _, root_dir = shell_command('git rev-parse --show-toplevel')
    return root_dir[0].decode('utf8').strip().rstrip('/')


def current_branch():
    _, branch = shell_command(r"git branch --no-color | grep '^\*'")
    branch_name = branch[0]
    try:
        branch_name = branch_name.decode('utf8')
    except AttributeError:
        pass
    return branch_name.replace('* ', '').strip()


@contextmanager
def cd(directory):
    original_cwd = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(original_cwd)


def get_repo_name() -> str:
    retcode, url = shell_command('git config --get remote.origin.url')
    if retcode:
        return ''

    origin_url = url[0].decode('utf8').strip()

    # NOTE: Usually remote.origin.url is set with SSH form: git@github.com:upwlabs/emma
    #   but it's possible to be with HTTPS form:
    #   https://github.com/upwlabs/internal_tools.git
    #   Need to normalize both into same format.
    repo_name = origin_url\
        .replace('https://github.com/upwlabs/', '')\
        .replace('git@github.com:upwlabs/', '')\
        .replace('.git', '')

    return repo_name


def current_branch_of_repo(repo_root_path: str) -> str:
    with cd(repo_root_path):
        return current_branch()


def shell_command(command, capture_stderr=False):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.stdout.readlines()
    err_output = p.stderr.readlines()
    retcode = p.wait()
    if capture_stderr:
        return retcode, output, err_output,
    else:
        return retcode, output