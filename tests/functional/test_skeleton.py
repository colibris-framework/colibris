
import os
import pathlib
import shutil


def test_start_project_default_skeleton(colibris_env):
    colibris_env.chdir_projects()
    colibris_env.run_cmd('colibris-start-project test-start-project')

    assert 'test-start-project' in os.listdir('.')
    assert 'setup.py' in os.listdir('test-start-project')
    assert 'teststartproject' in os.listdir('test-start-project')

    os.chdir('test-start-project')
    assert 'settings.py' in os.listdir('teststartproject')
    assert 'manage.py' in os.listdir('teststartproject')
    assert 'migrations' in os.listdir('teststartproject')
    assert 'tests' in os.listdir('teststartproject')


def test_start_project_custom_skeleton(colibris_env):
    default_skeleton_dir = os.path.join(colibris_env.colibris_dir, 'colibris', 'skeleton')
    custom_skeleton_dir = os.path.join(colibris_env.projects_dir, 'custom-skeleton')

    shutil.copytree(default_skeleton_dir, custom_skeleton_dir)
    pathlib.Path(custom_skeleton_dir, 'custom-file.txt').touch()

    colibris_env.chdir_projects()
    colibris_env.run_cmd('colibris-start-project test-custom-project --skeleton {skeleton}'
                         .format(skeleton=custom_skeleton_dir))

    assert 'test-custom-project' in os.listdir('.')
    assert 'testcustomproject' in os.listdir('test-custom-project')
    assert 'custom-file.txt' in os.listdir('test-custom-project')

    os.chdir('test-custom-project')
