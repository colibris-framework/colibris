
import os


def test_manage_make_migrations(test_project):
    test_project.run_cmd('testproject/manage.py makemigrations initial')

    assert '001_initial.py' in os.listdir('testproject/migrations')
