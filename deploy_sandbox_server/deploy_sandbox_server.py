#!/usr/bin/env python3

from typing import Optional
import typer

import jenkins

from config import USERNAME, HOST, TOKEN, REPO_NAME_TO_JOB_NAME, REPO_ROOT_PATH
import utils

from enum import Enum

typer_app = typer.Typer()


class App(str, Enum):
    glow_forum = "glow_forum"
    bryo = "bryo"
    kaylee = "kaylee"
    emma = "emma"
    lexie = "lexie"
    noah = "noah"
    zoe = "zoe"
    suso = "suso"
    admin = "internal_tools"


def get_jenkins_server():
    assert HOST, 'Please define HOST in config.py'
    assert USERNAME, 'Please define USERNAME in config.py'
    assert TOKEN, 'Please define TOKEN in config.py'
    return jenkins.Jenkins(HOST, username=USERNAME, password=TOKEN)


@typer_app.command()
def deploy(
        app: Optional[App] = None,
        branch: Optional[str] = None,
        slack: Optional[str] = '',
        upgrade_db: bool = False,
        merge_dev_branch: bool = True):
    server = get_jenkins_server()

    if not app:
        app = App(utils.get_repo_name())

    job = REPO_NAME_TO_JOB_NAME.get(app.value, None)
    assert job, f'{app.value} is not defined in REPO_NAME_TO_JOB_NAME'

    git_branch = branch
    if not git_branch:
        git_branch = get_deploy_branch(app.value)

    if slack:
        users = slack.split(',')
        valid_users = []
        for user in users:
            if 'logan' in user and 'logan.wang' not in user:
                valid_users.append('@logan.wang')
            elif '@' not in user and '#' not in user and '!' not in user:
                valid_users.append('@' + user)
            else:
                valid_users.append(user)

        slack = ','.join(valid_users)
    print(app, app == App.admin)
    if app == App.admin:
        parameters = {
            'branch': git_branch,
            'tag': '',
            'admindash-www': True,
            'delay': 0,
        }
        print(
            f'Start deploy {app.value}, branch: {git_branch}, admindash-www')
    else:
        parameters = {
            'branch': git_branch,
            'tag': '',
            'upgradeDB': upgrade_db,
            'targetServers': 'dragon',
            'mergeDevBranch': merge_dev_branch,
            'devBranch': 'dragon-develop',
            'slack': slack,
            'delay': 0,
        }
        print(
            f'Start deploy {app.value}, branch: {git_branch}, upgradeDB: {upgrade_db}, mergeDevBranch: {merge_dev_branch}')
        if slack:
            print(f'will slack to {slack} after finished')
    return server.build_job(job, parameters=parameters, token=None)


def get_deploy_branch(code_name) -> str:
    repo_path = f'{REPO_ROOT_PATH}/{code_name}'
    return utils.current_branch_of_repo(repo_path)


if __name__ == '__main__':
    typer_app()
