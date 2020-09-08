
import json
import os
import requests
import time


def test_manage_make_migrations(test_project):
    test_project.run_cmd('testproject/manage.py db create initial')

    assert '001_initial.py' in os.listdir('testproject/migrations')


def test_manage_migrate(test_project):
    test_project.run_cmd('testproject/manage.py db create initial')
    test_project.run_cmd('testproject/manage.py db migrate')
    test_project.run_cmd('sqlite3 testproject.db .tables | grep user')


def test_manage_runserver(test_project):
    test_project.run_cmd('testproject/manage.py db create initial')
    test_project.run_cmd('testproject/manage.py db migrate')

    process = test_project.run_popen('testproject/manage.py runserver')
    time.sleep(2)  # Wait for the server to start

    response = requests.get('http://localhost:8888/health')

    try:
        assert response.status_code == 200
        assert json.loads(response.text) == 'healthy'

    finally:
        process.kill()
        time.sleep(2)  # Wait for the server to stop
