import argparse
import os
import re
import shutil

TMP_TEMPLATE_PATH = '/tmp/colibris-template-repo'
MAIN_PACKAGE_NAME = '__packagename__'


def start_project():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='The project name', type=str)
    parser.add_argument('--template', help='The template repo', type=str, required=False)
    args = parser.parse_args()

    project_name = args.name
    package_name = re.sub('[^a-z0-9_]', '', project_name).lower()

    if args.template is None:
        skeleton_dir = os.path.join(os.path.dirname(__file__), 'skeleton')
    else:
        if os.path.exists(TMP_TEMPLATE_PATH):
            shutil.rmtree(TMP_TEMPLATE_PATH)

        os.system("git clone {} {}".format(args.template, TMP_TEMPLATE_PATH))
        skeleton_dir = TMP_TEMPLATE_PATH

    shutil.copytree(skeleton_dir, project_name, ignore=shutil.ignore_patterns('.git'))

    old_package_name = '{}/{}'.format(project_name, MAIN_PACKAGE_NAME)
    new_package_name = '{}/{}'.format(project_name, package_name)

    shutil.move(old_package_name, new_package_name)

    rename_command = 'find {} -type f | xargs sed -i "s/{}/{}/g"'

    os.system(rename_command.format(project_name, '__packagename__', package_name))
    os.system(rename_command.format(project_name, '__projectname__', project_name))

    print('project {} is ready'.format(project_name))
