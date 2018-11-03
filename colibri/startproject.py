
import os
import re
import shutil


def start_project():
    project_name = os.path.basename(os.getcwd())
    package_name = re.sub('[^a-z0-9_]', '', project_name).lower()
    skeleton_dir = os.path.join(os.path.dirname(__file__), 'skeleton')

    for entry in os.listdir(skeleton_dir):
        full_path = os.path.join(skeleton_dir, entry)
        if os.path.isdir(full_path):
            shutil.copytree(full_path, entry)

        else:
            shutil.copy(full_path, '.')

        os.system('find {} -type f | xargs sed -i "s/__packagename__/{}/g"'.format(entry, package_name))

    os.rename('projectpackage', package_name)

    print('project {} is ready'.format(project_name))
