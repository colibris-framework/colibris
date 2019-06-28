
import argparse
import atexit
import os
import re
import shutil
import subprocess
import tempfile


PACKAGE_NAME_PLACEHOLDER = '__packagename__'
PROJECT_NAME_PLACEHOLDER = '__projectname__'
IGNORE_PATTERNS = ['.git']

tmp_dir = None


def cleanup():
    if tmp_dir:
        tmp_dir.cleanup()


def get_template_dir(template):
    global tmp_dir

    if template is None:  # Use default template skeleton
        return os.path.join(os.path.dirname(__file__), 'skeleton')

    elif template.startswith('git@') or template.startswith('http:') or template.startswith('https:'):
        tmp_dir = tempfile.TemporaryDirectory()
        cmd = ['git', 'clone', template, tmp_dir.name]

        subprocess.check_call(cmd)

        return tmp_dir.name

    else:  # Assuming local directory
        return template


def start_project():
    atexit.register(cleanup)

    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='The project name (e.g. my-project)', type=str)
    parser.add_argument('--template', help='An optional template (can be a local dir or a git repo)',
                        type=str, required=False)

    args = parser.parse_args()

    project_name = args.name
    package_name = re.sub('[^a-z0-9_]', '', project_name).lower()

    template_dir = get_template_dir(args.template)

    shutil.copytree(template_dir, project_name, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))

    old_package_name = '{}/{}'.format(project_name, PACKAGE_NAME_PLACEHOLDER)
    new_package_name = '{}/{}'.format(project_name, package_name)

    shutil.move(old_package_name, new_package_name)

    rename_command = 'find {} -type f | xargs sed -i "s/{}/{}/g"'

    os.system(rename_command.format(project_name, PACKAGE_NAME_PLACEHOLDER, package_name))
    os.system(rename_command.format(project_name, PROJECT_NAME_PLACEHOLDER, project_name))

    print('project {} is ready'.format(project_name))
