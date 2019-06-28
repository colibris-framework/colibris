
import os


def test_manage_make_migrations(test_project):
    test_project.run_cmd('testproject/manage.py makemigrations initial')

    assert '001_initial.py' in os.listdir('testproject/migrations')


def test_manage_migrate(test_project):
    test_project.run_cmd('testproject/manage.py makemigrations initial')
    test_project.run_cmd('testproject/manage.py migrate')

    test_project.run_cmd('sqlite3 testproject.db .tables | grep user')
