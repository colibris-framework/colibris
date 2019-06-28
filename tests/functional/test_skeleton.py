
import os


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
    colibris_env.chdir_projects()
    colibris_env.run_cmd('colibris-start-project --template {}/tests/functional/dummy-skeleton test-custom-project '
                         .format(colibris_env.colibris_dir))

    assert 'test-custom-project' in os.listdir('.')
    assert 'testcustomproject' in os.listdir('test-custom-project')

    os.chdir('test-custom-project')
